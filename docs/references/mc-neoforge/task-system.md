> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# 任务系统参考

> 综合 Task 生命周期 / 伐木流程 / executingTask / ISearchAction
> 说明：本文描述 maidquest / maidtown 的任务系统设计（基于 maidmorework 旧 API `ISearchAction` / `SearchBehavior`）。maidmorework 已重构移除这些 API，maidquest/maidtown 待跟进；本文作为设计参考保留（文中 SearchBehavior 均指旧实现）。

---

## 一、核心设计原则

### Behavior 纯调度，不持数据

Behavior 只持有自身运转状态（导航目标、submitted 标志），**不持任务执行数据**（logs、phase、progress）。

### Task 持有所有执行状态

```java
// Task 基类定义生命周期
public void startExecution(ColonistEntity c, ServerLevel level) {}
public boolean tickExecution(ColonistEntity c, ServerLevel level) { return false; }
public void stopExecution(ColonistEntity c, ServerLevel level) {}
public boolean isDone() { return false; }
```

Task 子类（如 LoggingTask）内部管理私有 Phase 枚举、BFS 方块列表、进度计数等。

---

## 二、Claim → Execute → Submit 三阶段

```
ColonistPicker（加权随机容器）
  TaskClaimBehavior    — 走到板子→评分→接任务
  TaskExecuteBehavior  — 委托 Task.tickExecution 执行
  TaskSubmitBehavior   — 走回板子→submit→奖励
```

| Behavior | 权重 | 条件 |
|---|---|---|
| Claim | 钱越少越高(最大99) | 无任务 + 附近板子有可接任务 |
| Execute | 80 | 有 CLAIMED_TASK + shouldExecute |
| Submit | 90 | 背包物品 ≥ quantity |

### Behavior 侧 TaskExecuteBehavior

```java
start()  → c.executingTask = true + task.startExecution(c, level)
tick()   → task.tickExecution(c, level)
canStillUse() → t.isDone() 为 false
stop()   → c.executingTask = false + task.stopExecution(c, level)
```

---

## 三、伐木 9 步流程

1. **认领** — 走到板子→`board.claimTask(task, c)` → `c.setClaimedTask(task)`
2. **检测** — `checkExtraStartConditions`：有 CLAIMED_TASK
3. **挂检索** — `startExecution` 里 `c.setSearchAction(this::scanRegion)`
4. **游荡检索** — SearchBehavior 并行，逐方块调 `searchAction.search()`
5. **感知完成** — `getSearchAction() == null` → 读 logs/leaves 列表
6. **走路** — 导航到最低原木脚下地面（`lowest.below()`），移速 0.6
7. **砍树** — 每秒一刀，树叶 1 刀破 2，原木 3 刀破 1
8. **DONE** — `currentWork >= totalWork` → `isDone() = true`
9. **提交** — 走回板子→扣背包材料→发奖励→清 CLAIMED_TASK

---

## 四、executingTask 保护机制

```java
// TaskExecuteBehavior
start() → c.executingTask = true;
stop()  → c.executingTask = false;

// TaskSubmitBehavior 第一行检查
checkExtraStartConditions() {
    if (c.executingTask) return false;
}
```

防止砍树到一半 Submit 抢走控制。

---

## 五、shouldStop 反模式

优先用已有字段判断生命周期：

```java
// ✅ 自然字段判断
boolean canStillUse() { return target != null; }

// ❌ 反模式：凭空加 shouldStop
boolean canStillUse() { return !shouldStop; }
```

---

## 六、ISearchAction 检索模式

```java
@FunctionalInterface
public interface ISearchAction {
    boolean search(ServerLevel level, BlockPos center,
                   int halfXZ, int yDown, int yUp, ColonistEntity c);
}
```

Task 设 searchAction → SearchBehavior 调 → 命中返回 true → SearchBehavior 清 action → Task 感知。

---

## 七、常见陷阱

| 陷阱 | 修复 |
|------|------|
| 提交不扣背包→秒完成 | submit() 必须调用 removeFromInventory |
| 执行被 Submit 打断 | 加 executingTask 标志 |
| SEARCHING 阶段 Behavior 被停掉 | tickSearch 空转时返回 true 保活 |
| BFS 结果为空死循环 | 回 SEARCHING 游荡，不要死循环 |
| Claim 只检查"有板子"不检查"有任务" | findNearestBoard 需 filter(hasClaimableTask) |
| 夹 ANALYZING 阶段 | BFS 在 searchAction 里已做完，直接进 WALKING |
| 背包不先堆叠 | 先遍历同种堆叠，再找空格 |
| 导航到原木方块 | 导航到 lowest.below() |
