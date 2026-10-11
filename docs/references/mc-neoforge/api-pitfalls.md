> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# MC 26.x API 常见陷阱速查

---

## 物品

| 陷阱 | 正确做法 |
|------|---------|
| Item 注册用 `register()` 报 NPE | 用 `ITEMS.registerItem("id", props -> new MyItem(props.stacksTo(1)))` |
| SpawnEggItem 不接 EntityType | 用 `new SpawnEggItem(props.spawnEgg(ModEntities.COLONIST.get()))` |
| ItemStack 比较 | `isSameItemSameComponents`（非 `isSameItemSameTags`） |
| 物品模型 | 双路径：`items/xxx.json` + `models/item/xxx.json` |

## 方块

| 陷阱 | 正确做法 |
|------|---------|
| Block 构造缺 ResourceKey | `Properties.of().setId(ResourceKey.create(Registries.BLOCK, id))` |
| BlockEntity 序列化 | `saveAdditional(ValueOutput)` / `loadAdditional(ValueInput)` |
| 方块注册顺序 | ModBlocks 必须在 ModItems 之前注册 |

## 实体

| 陷阱 | 正确做法 |
|------|---------|
| EntityType.Builder.build("id") | `build(ResourceKey.create(Registries.ENTITY_TYPE, Identifier))` |
| onAddedToWorld 不存在 | 用首帧 tick() 模式替代 |
| getDayTime() | `getGameTime()` |
| getRandom() | 返回 `RandomSource` 非 `java.util.Random` |
| VillagerData.setProfession | 改为 `withProfession`（record） |

## GUI / Screen

| 陷阱 | 26.x 变更 |
|------|---------|
| renderBg | `extractBackground` |
| renderSlots | `extractSlots` |
| renderWidget | `extractWidgetRenderState` |
| mouseClicked(x,y,btn) | `mouseClicked(MouseButtonEvent, boolean)` |
| onDrag | 已删除，用 `mouseDragged` |
| updateWidgetNarration | **必须实现** |
| imageWidth/height | **final**，只能构造器设 |
| rebuildWidgets | **protected**，子类同名 private 要改名 |
| 槽位背景 | `blitSprite(RenderPipelines.GUI_TEXTURED, "container/slot", sx-1, sy-1, 18, 18)` |
| 纹理 blit | `blit(RenderPipelines.GUI_TEXTURED, tex, x, y, 0, 0, w, h, 256, 256)` |

## Annotation / 注册

| 陷阱 | 26.x 变更 |
|------|---------|
| @EventBusSubscriber | 无 `bus` 参数 → `@EventBusSubscriber(modid=..., value=Dist.CLIENT)` |
| DeferredRegister | `DeferredRegister.createItems(MODID)` 返回 `Items` 变体才有 `registerItem()` |

## Attachment

| 陷阱 | 说明 |
|------|------|
| 不加 sync → 客户端读 EMPTY | 必须 `.sync(STREAM_CODEC)` |
| isPresent() 引用比较 | 反序列化是新实例 → 用 UUID 全零业务判断 |
| Empty ItemStack Crash | 用 `ItemStack.OPTIONAL_STREAM_CODEC` |
| grow() 不触发同步 | 就地修改后调 setter |

## Codec

| 陷阱 | 说明 |
|------|------|
| dispatch 需要 MapCodec | `RecordCodecBuilder.mapCodec()` → `.codec()` |
| group() 参数 | 必须完整 `.fieldOf().forGetter()` 链 |
| CODEC 可视性 | 必须 `public static final` |
| Enum Codec | `Codec.STRING.xmap(Enum::valueOf, Enum::name)` |

## Chunk / Level

| 陷阱 | 说明 |
|------|------|
| 未加载 Chunk 静默返回 null | `getBlockEntity/getBlockState` 不抛异常 → 必须 `isLoaded(pos)` |
| 单机 openMenu 线程陷阱 | lambda 跑在客户端线程 → 用 `server.execute(() -> sp.openMenu(...))` |
| MutableBlockPos 被重用 | 传 lambda 前 `.immutable()` 固化 |

## Gradle

| 陷阱 | 说明 |
|------|------|
| configuration-cache | 建议设 `false`（MDG 兼容性） |
| ZGC | Windows 上可能导致网络/SSL 异常 |
