> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).
>
> **2026-10-11 更新：本次重构已决定剔除 TLM 依赖（与目标设计冲突太多）。本文件转为历史技术参考，不再作为新实现的接口依据；仅用于理解旧实现与迁移时的对照。**

# MaidTown — TLM 集成参考

> 综合 EntityMaid 继承 / Brain 决策循环 / IMaidTask API / 拾取系统

---

## 一、入口注册：@LittleMaidExtension

```java
@LittleMaidExtension
public class MaidTownExtension implements ILittleMaid {
    public MaidTownExtension() {}

    @Override public void addMaidTask(TaskManager manager) {
        manager.register(MyTask.INSTANCE);
    }

    @Override public void addExtraMaidBrain(ExtraMaidBrainManager manager) {
        // 注入自定义 Sensor/Memory/AI
    }
}
```

Gradle 依赖：`implementation files('libs/touhoulittlemaid-2.0.0-neoforge+mc26.1.2-snapshot.jar')`

---

## 二、EntityMaid 继承架构

### 继承链

```
TamableAnimal → MaidManagerHost → EntityMaid → ColonistEntity
```

MaidManagerHost 持有约 20 个 Manager（animation, backpack, chatBubble, combat, navigation 等）。

### EntityType 泛型桥接

```java
@SuppressWarnings("unchecked")
public ColonistEntity(EntityType<? extends ColonistEntity> type, Level level) {
    super((EntityType<EntityMaid>) (Object) type, level);
}
```

### 行为抑制

```java
@Override protected void registerGoals() {}  // 不调 super
@Override protected void customServerAiStep(ServerLevel level) {}  // 不调 super
```

### 渲染器

```java
event.registerEntityRenderer(ModEntities.COLONIST.get(), EntityMaidRenderer::new);
```

---

## 三、IMaidTask API

```java
public interface IMaidTask {
    Identifier getUid();                          // 任务唯一 ID
    ItemStack getIcon();                          // UI 图标
    List<Pair<Integer, BehaviorControl<? super EntityMaid>>> createBrainTasks(EntityMaid maid);

    // 控制开关
    default boolean isEnable(EntityMaid maid) { return true; }
    default boolean workPointTask(EntityMaid maid) { return false; }
}
```

---

## 四、Brain / Activity / Schedule

### 三层调度

- **Schedule**：DAY/NIGHT/ALL — 决定当前 Activity
- **Activity**：CORE > PANIC > IDLE/REST > WORK — 互斥状态槽
- **Task（行为包）**：IMaidTask 实现，塞进 WORK 槽

### Activity vs Task 区别

Activity 是互斥状态槽，Task 是带 ID+图标+行为列表的行为包。setTask() 切换到新 Task 后自动 refreshBrain。

### 4 种 Sensor + 12 种 Memory

Sensor 定时扫描 → 结果写入 Memory → Behavior 读取。自定义通过 `IExtraMaidBrain` 注册。

### Brain Tick 调用链

Brain 不在 `Mob.serverAiStep()` 自动 tick。EntityMaid 在 `customServerAiStep(ServerLevel)` 中手动调用 `brain.tick()`。

### 实践架构：Brain（执行引擎）+ 决策树（大脑皮层）

```
customServerAiStep:
  1. 首帧 setSchedule(ALL) → WORK 常开
  2. 每 N tick：决策树判断 → setTask() 切换
  3. brain.tick() → CORE + WORK 执行
```

---

## 五、关键陷阱

1. **EntityType 泛型 cast 是必要的** — Java invariant 泛型
2. **`customServerAiStep` 参数是 `ServerLevel`** — 不是 `Level`
3. **不要调 `super.registerGoals()` / `super.customServerAiStep()`**
4. **SynchedEntityData 不可靠** — 用 Attachment 持久化
5. **构造函数中 Attachment 未加载** — 首帧 tick() 才是初始化时机
6. **Activity 切换行为必须挂在 CORE** — 挂 WORK 会导致死循环
7. **`extraMaidBrainManager` 是 package-private** — 用 `ILittleMaid.addExtraMaidBrain()` 替代
