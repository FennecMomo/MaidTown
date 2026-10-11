> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../INDEX.md).

# 通用代码模式

> 综合背包操作 / 捡东西 / 进食 / 掉落收集

---

## 一、背包物品操作

### 进背包：先堆叠后空格

```java
void addToInventory(Entity e, ItemStack stack) {
    // 1) 先找同种物品堆叠
    for (int i = 0; i < size; i++) {
        ItemStack exist = getItem(i);
        if (ItemStack.isSameItemSameComponents(exist, stack)
                && exist.getCount() < exist.getMaxStackSize()) {
            int add = Math.min(exist.getMaxStackSize() - exist.getCount(), stack.getCount());
            exist.grow(add); setItem(i, exist); stack.shrink(add);
            if (stack.isEmpty()) return;
        }
    }
    // 2) 再找空格
    for (int i = 0; i < size; i++) {
        if (getItem(i).isEmpty()) { setItem(i, stack.copy()); return; }
    }
}
```

### 破坏方块并收集掉落

```java
List<ItemStack> drops = Block.getDrops(state, level, pos, be, entity, tool);
for (ItemStack s : drops) addToInventory(entity, s);
level.destroyBlock(pos, false);  // false = 不掉落
```

### 出背包：按方块类型扣除

用 `BlockItem` + `BlockTags` 匹配类型，比 ItemTags 可靠。

---

## 二、捡东西系统

### 完整流程

1. 每 20 tick 扫描 3 格内掉落物
2. 选最近的 → `getNavigation().moveTo(target, 1.0)` 走过去
3. 达到 1 格内 → `swing(MAIN_HAND)` + 10 tick 冷却
4. 动画结束 → 放入背包（堆叠优先）→ `target.kill(level)` 移除实体

### 导航到达阈值 vs 捡起距离

`Navigation.moveTo()` 约 1.5 格就认为"到了"，捡起需要 ≤1 格。检测导航完成但距离不够时重新发起导航。

### 动画计时器标志位模式

计时器在 `tick()` 每 tick 递减，不在 `% 20` 限频块里减：

```java
// tick() 里每 tick 递减
if (pickupAnimTick > 0) { pickupAnimTick--; if (pickupAnimTick == 0) pickupReady = true; }

// tryPickup 里查标志位（每 20 tick）
if (pickupReady) { pickupReady = false; doPickupItem(...); return; }
```

**通用规则：** 跨异步调度周期的状态传递，必须用 boolean 标志位。

---

## 三、进食系统

### 食物判断

`EntityMaid.isFood(ItemStack)` 硬编码返回 false。直接用 `stack.has(DataComponents.FOOD)`。

### 动画

用 `startUsingItem(hand)`，MC 自动举手→咀嚼→吞咽。

### 一次只放 1 个食物

`stack.split(1)` 只取 1 个，MC 自动消耗。**不放整叠、不手动 shrink。**

### isEating 标志位协程模式

一旦进入进食就吃到饱，不再检查 `< 20`。需要 isEating 标志位。

### Brain Activity 切换打断咀嚼

EntityMaid 内部 Brain 周期性切 Activity，导致所有 WORK behavior 的 stop() 被调。

**修复：** stop() 不做任何清理（不调 stopUsingItem、不退食物），start() 检测状态恢复：

```java
@Override protected void stop(ServerLevel level, Entity c, long time) {
    // 不清理咀嚼状态 — 让 CORE 期间咀嚼继续
}

@Override protected void start(ServerLevel level, Entity c, long time) {
    if (!hand.isEmpty() && hand.has(DataComponents.FOOD)) {
        eating = true;  // Brain 切回，续嚼
        return;
    }
}
```

### 冷却计时陷阱

冷却必须在 `tick()` 里递减，不能在 `% 20` 限频块里减。

---

## 四、受伤打断进食

```java
NeoForge.EVENT_BUS.addListener(LivingDamageEvent.Pre.class, event -> {
    if (event.getEntity() instanceof ColonistEntity ce && ce.isUsingItem()) {
        ce.stopUsingItem();
    }
});
```

---

## 五、三种食物系统对比

| | TLM 女仆 | 居民 |
|---|---|---|
| 食物判断 | IMaidMeal 注册表 | `DataComponents.FOOD` |
| 触发条件 | 生命值 < 最大 | 饥饿值 < 阈值 |
| 食用效果 | 回血 | 加饥饿值 |

原版营养 → 居民饥饿换算：`nutrition * 5`
