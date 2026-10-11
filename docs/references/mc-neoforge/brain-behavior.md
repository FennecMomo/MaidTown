> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# Brain 行为系统参考

> 综合 Behavior 生命周期 / Picker 调度 / Activity 切换 / 搜索模式现状

---

## 一、行为生命周期核心陷阱：canStillUse 在 tick() 前被检查

MC Brain 的 `Behavior.tickOrStop()` 流程：

```
tickOrStop → timedOut? → doStop
           → !canStillUse? → doStop  ← 先查这个！
           → tick()
```

**start() 设 IDLE 状态→canStillUse 立刻 false→tick 永远走不到→死循环。**

正确做法：`start()` 里直接做完所有初始化，让 `canStillUse` 立即返回 true。

```java
// ✅ start() 直接进入可用状态
void start(level, c, time) {
    submitted = false;
    target = findTarget(c);
    if (target == null) submitted = true;  // 没目标立即标记结束
}
boolean canStillUse(level, c, time) { return !submitted; }
```

---

## 二、超时陷阱：默认 60 tick（3秒）

`Behavior(Map)` 默认 `maxDuration=60`。长导航行为 3 秒被强制停止→重新 pick→无限循环。

```java
// ❌ 默认 60 tick 超时
super(Map.of());

// ✅ 禁用超时
super(Map.of(), Integer.MAX_VALUE);
```

---

## 三、WeightedPicker + WeightedChildBehavior

Picker 串行调度：挑一个子行为→跑完→停→重新加权挑下一个。同一时间只有一个子行为在跑。

```java
// Picker 必须自己检查子行为结束！
void tick(level, entity, time) {
    if (current == null) return;
    current.update(level, entity, time);
    if (!current.canContinue(level, entity, time)) {  // ← 关键
        current.end(level, entity, time);
        current = null;
    }
}
```

### 子行为互斥：权重+条件实现优先级

高优行为就绪时，低优行为的 `canStart` 返回 false、`getWeight` 返回 0：

```java
// Execute：背包够了就让位给 Submit
checkExtraStartConditions() { return !isTaskComplete(c) && hasTask(); }
getWeight() { return isTaskComplete(c) ? 0 : 80; }

// Submit：背包够时独占
checkExtraStartConditions() { return hasTask() && isTaskComplete(c); }
getWeight() { return isTaskComplete(c) ? 90 : 0; }
```

---

## 四、Activity 切换

`MaidUpdateActivityFromSchedule` 行为**必须挂在 CORE activity**。挂在 WORK = 死循环（WORK 没激活→行为不执行→不调用切换→WORK 永远不激活）。

---

## 五、搜索模式现状（maidmorework）

旧版独立 `SearchBehavior`（+ `ISearchAction` 委托）已随重构移除，当前两种搜索模式：

- **砍树**：`ChopBehavior` 内置个人搜索（`searchPersonalTargets`），受 Home 半径限制，节流 `PERSONAL_SEARCH_CD_TICKS`
- **矿井**：`MineCenterBehavior` 不做搜索，向矿井中心请求派活（中心从任务池取距女仆最近的坐标）

实现新任务时不要照搬旧 `SearchBehavior` 示例（`setSearchTarget` / `searchResult` 等 API 当前代码未使用）。

---

## 六、常见陷阱速查

| 症状 | 原因 | 修复 |
|------|------|------|
| 行为永远不执行，无限循环 | start() 设了 canStillUse 不通过的状态 | start() 里设好全部初始状态 |
| 长导航 3 秒被杀 | 默认 maxDuration=60 | super(Map.of(), Integer.MAX_VALUE) |
| Picker 不切换子行为 | tick() 没检查 canContinue() | 每 tick 检查并置 null |
| 执行被 Submit 打断 | 缺 executingTask 标志 | checkExtraStartConditions 第一行检查 |
| 所有 WORK 行为不执行 | Activity 切换挂错位置 | MaidUpdateActivityFromSchedule 必须挂 CORE |
| 导航到方块卡住 | 目标在空中/被包围 | 导航到最低方块脚下 low.below() |
