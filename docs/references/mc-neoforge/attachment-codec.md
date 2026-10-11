> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# Attachment 持久化与 Codec 参考

> 综合 Attachment 系统 / 多态 Codec / 序列化陷阱

---

## 一、Attachment 基本模式

```java
public static final Supplier<AttachmentType<Task>> CLAIMED_TASK =
    ATTACHMENT_TYPES.register("claimed_task",
        () -> AttachmentType.builder(() -> Task.EMPTY)        // 哨兵默认值
            .serialize(Task.CODEC.fieldOf("claimedTask"))     // NBT 持久化
            .sync(ByteBufCodecs.fromCodecWithRegistries(Task.CODEC))  // 网络同步
            .build());
```

### 哨兵模式（Sentinel Pattern）

```java
public static final UUID EMPTY_UUID = new UUID(0, 0);
public static final Task EMPTY = new Task(EMPTY_UUID, ...);

public boolean isPresent() {
    return !EMPTY_UUID.equals(id);  // ✅ 用业务值判断
}
```

**致命陷阱：`isPresent()` 不能用引用比较**

```java
// ❌ 反序列化创建新实例，this != EMPTY 永远为 true
public boolean isPresent() { return this != EMPTY; }
```

### 必须加 `.sync()` 才能同步到客户端

不加 sync → 客户端永远读 EMPTY。

### StreamCodec 生成

```java
public static final StreamCodec<RegistryFriendlyByteBuf, TaskRecord> STREAM_CODEC =
    ByteBufCodecs.fromCodecWithRegistries(CODEC);
```

---

## 二、Empty ItemStack Crash

`ItemStack.STREAM_CODEC` 拒绝空栈，`ItemStack.CODEC` 静默丢数据。

**必须用 `ItemStack.OPTIONAL_STREAM_CODEC` 和 `ItemStack.OPTIONAL_CODEC`**。

`grow()` 就地修改不触发 Attachment 同步 → 需调 entity 的 setter。

---

## 三、多态 Codec

### 核心模式

```java
public abstract class Task {
    public abstract String type();  // dispatch key

    public static final Codec<Task> CODEC = Codec.STRING.dispatch(
        Task::type,
        type -> switch (type) {
            case "logging"  -> LoggingTask.MAP_CODEC;
            case "mining"   -> MiningTask.MAP_CODEC;
            default -> throw ...
        }
    );
}
```

### 关键词陷阱

| 陷阱 | 说明 |
|------|------|
| dispatch 需要 MapCodec 不是 Codec | `RecordCodecBuilder.mapCodec()` 返回 MapCodec，`.codec()` 导出 Codec |
| group() 参数类型 | 必须完整链 `.fieldOf().forGetter()`，不能裸 MapCodec |
| record 不能继承 | 用抽象类 + 子类 |
| 多态 Codec 缺失→子类信息丢失 | 必须用 kind() dispatch，否则 instanceof 全 false |
| CODEC 必须 public | BlockEntity 跨包访问 |

---

## 四、BlockEntity 持久化

```java
@Override protected void saveAdditional(ValueOutput output) {
    super.saveAdditional(output);
    output.store("Tasks", Task.CODEC.listOf(), List.copyOf(tasks));
}

@Override protected void loadAdditional(ValueInput input) {
    super.loadAdditional(input);
    tasks.clear();
    input.read("Tasks", Task.CODEC.listOf()).ifPresent(tasks::addAll);
}
```

**参数是 `ValueOutput/ValueInput`，不是 CompoundTag。**
