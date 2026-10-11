> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# MaidTown — MC/NeoForge 注册系统参考

> 综合 blocks / items / entities / events / registries / resources 六份参考文档

---

## 一、DeferredRegister 注册体系

`DeferredRegister` 是 NeoForge 推荐的注册方式，封装了 `RegisterEvent`。每个方块/物品在游戏中只有一个单例实例。

### 通用模式

```java
public static final DeferredRegister<MyType> REGISTER =
    DeferredRegister.create(BuiltInRegistries.MY_TYPE, "modid");
public static final Supplier<MyType> MY_OBJECT = REGISTER.register("my_object", () -> new MyType(...));
```

在 Mod 主类构造器中注册：`ModBlocks.BLOCKS.register(modBus);`

### 专用变体速查

| 变体 | 创建方式 | 返回类型 |
|------|---------|---------|
| Blocks | `DeferredRegister.createBlocks("modid")` | `DeferredBlock<T>` |
| Items | `DeferredRegister.createItems("modid")` | `DeferredItem<T>` |
| 通用 | `DeferredRegister.create(registry, "modid")` | `DeferredHolder<R,T>` |

### 查询注册表（注册完成后才能用）

```java
BuiltInRegistries.BLOCK.getValue(Identifier.fromNamespaceAndPath("minecraft", "dirt"));
BuiltInRegistries.BLOCK.getKey(Blocks.DIRT);
```

---

## 二、方块注册

```java
public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("modid");
public static final DeferredBlock<Block> MY_BLOCK = BLOCKS.register("my_block",
    registryName -> new Block(BlockBehaviour.Properties.of()
        .setId(ResourceKey.create(Registries.BLOCK, registryName))
        .destroyTime(2.0f).sound(SoundType.GRAVEL)));
```

### BlockBehaviour.Properties 常用方法

| 方法 | 说明 |
|------|------|
| `setId(ResourceKey)` | **必须设置** |
| `destroyTime(float)` | 破坏时间（石头1.5, 基岩-1） |
| `explosionResistance(float)` | 爆炸抗性 |
| `sound(SoundType)` | 音效 |
| `noOcclusion()` | 不遮挡光照 |
| `requiresCorrectToolForDrops()` | 需要正确工具才掉落 |

### BlockItem 注册

```java
public static final DeferredItem<BlockItem> MY_BLOCK_ITEM = ITEMS.registerSimpleBlockItem(ModBlocks.MY_BLOCK);
```

---

## 三、物品注册

```java
public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems("modid");
public static final DeferredItem<Item> SPECIAL = ITEMS.registerItem("special_item", Item::new,
    props -> props.stacksTo(16).rarity(Rarity.RARE).fireResistant());
```

**重要：** 必须用 `registerItem()` 而非 `register()` — `Item.Properties` 需要构造前 `setId(ResourceKey)`。

### 创造模式标签页

```java
@SubscribeEvent
public static void buildContents(BuildCreativeModeTabContentsEvent event) {
    if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
        event.accept(ModItems.MY_ITEM.get());
    }
}
```

---

## 四、实体注册

```java
public static final DeferredRegister<EntityType<?>> ENTITIES =
    DeferredRegister.create(BuiltInRegistries.ENTITY_TYPE, "modid");
public static final DeferredHolder<EntityType<?>, EntityType<MyEntity>> MY_ENTITY =
    ENTITIES.register("my_entity", () -> EntityType.Builder.of(MyEntity::new, MobCategory.CREATURE)
        .sized(0.6f, 1.8f).build(ResourceKey.create(Registries.ENTITY_TYPE, ...)));
```

**重要：** `EntityType.Builder.build()` 需要 `ResourceKey`，不能只传字符串。

---

## 五、事件系统

### 两个事件总线

| 总线 | 变量 | 说明 |
|------|------|------|
| 游戏总线 | `NeoForge.EVENT_BUS` | 运行时事件 |
| 模组总线 | `IEventBus modBus`（构造器参数） | 生命周期事件 |

### 推荐方式：@EventBusSubscriber（自动发现）

```java
@EventBusSubscriber(modid = "modid")
public class ModEvents {
    @SubscribeEvent
    public static void onLivingJump(LivingEvent.LivingJumpEvent event) {}
}

// 客户端专用 — 注意 MC 26.x 无 bus 参数了
@EventBusSubscriber(value = Dist.CLIENT, modid = "modid")
public class ClientEvents {}
```

### 模组生命周期顺序

构造器 → `FMLConstructModEvent` → `RegisterEvent` → `FMLCommonSetupEvent`（并行）→ `InterModEnqueueEvent` → `InterModProcessEvent` → `FMLLoadCompleteEvent`

---

## 六、常见陷阱

1. **Item 注册必须用 `registerItem()` 而非 `register()`**
2. **Block 构造必须 `setId(ResourceKey)`**
3. **BlockItem 需单独注册，Block 注册必须在 Item 之前**
4. **`SpawnEggItem` 不再接 EntityType 参数** — 用 `props.spawnEgg(entityType)`
5. **`@EventBusSubscriber` 26.x 无 `bus` 参数**
6. **`FMLCommonSetupEvent` 并行触发** — 需主线程用 `event.enqueueWork()`
7. **注册期间不可查询注册表** — 其他模组可能还没注册
