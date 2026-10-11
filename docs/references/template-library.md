> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../INDEX.md).

# FennecLib UI 模板库参考

> 当前 FennecLib API + 旧名→新名映射 + 使用模式

---

## 一、当前 FennecLib API

### AI 行为框架

| 类 | 包 | 说明 |
|---|---|---|
| WeightedPicker | `com.fennecmomo.fenneclib.behavior` | 加权随机行为容器 |
| WeightedChildBehavior | `com.fennecmomo.fenneclib.behavior` | 加权子行为基类 |

### UI 组件

| 组件 | 包 | 说明 |
|------|-----|------|
| ConfirmPopupMenu | `template.Data` | 确认弹窗：`open(player, title, info, leftLbl, leftCmd, rightLbl, rightCmd)` |
| GenericContainerMenu | `template.Data` | 容器菜单基类（动态行列布局、Shift转移） |
| GenericContainerScreen | `template.UI` | 容器屏幕基类（暗底+面板+边框+标题） |
| ContentList | `template.List` | 可滚动条目列表（虚拟滚动+内置ScrollBar） |
| ButtonListItem | `template.List` | 按钮条目（纯按钮/文本+按钮/纯文本三模式） |
| InputListItem | `template.List` | 输入框条目 |
| StateBar | `template.Bar` | 状态条（Label:Value:Bar，支持RATIO/INTEGER/EXP格式） |
| ScrollBar | `template.Bar` | 虚拟滚动条组件 |
| IListItem | `template.Interface` | 列表条目接口（activate/deactivate） |
| IBar | `template.Interface` | 进度条渲染器接口（`IBar.DEFAULT` 内置三色渲染） |

---

## 二、旧名 → 新名映射表

| 旧名（lordling template） | 新名（FennecLib） |
|---|---|
| `C_Container` | `GenericContainerMenu` |
| `S_Container` | `GenericContainerScreen` |
| `W_EntryList` | `ContentList` |
| `W_StatBar` | `StateBar` |
| `W_TextBtn` | `ButtonListItem`（文本+按钮模式） |
| `W_BtnEntry` | `ButtonListItem`（纯按钮模式） |
| `W_InputEntry` | `InputListItem` |
| `W_Scrollbar` | `ScrollBar` |
| `I_Entry` | `IListItem` |
| `R_Bar` | `IBar` |

---

## 三、使用模式

### activate/deactivate 显隐管理

复合控件的子控件独立注册给 Screen，父 `visible=false` 不传播。必须通过接口方法统一管理。

### ContentList + IListItem 模式

```java
ContentList list = new ContentList(this::addRenderableWidget, x, y, w, h, rowH);
list.setEntries(List.of(entry1, entry2, ...));
// Plain Screen 必须手动转发鼠标事件
public boolean mouseDragged(MouseButtonEvent e, double dx, double dy) {
    return list.mouseDragged(e, dx, dy) || super.mouseDragged(e, dx, dy);
}
```

### adder 回调模式

所有组件最后一个参数是 `Consumer<AbstractWidget> adder`（传 `this::addRenderableWidget`），构造函数末尾调 `adder.accept(this)` 注册。不注册不渲染。

### 常见陷阱

- 父控件 `visible=false` 不传播到独立注册的子控件 → 走 activate/deactivate
- 不手搓进度条 → 用 StateBar + IBar.DEFAULT
- Plain Screen mouseDragged/mouseScrolled 必须转发给 ContentList
- FrameLayout 设尺寸用 setMinDimensions(w,h)，无 setWidth
- StringWidget 无 setColor → 用 `Component.withStyle(Style.EMPTY.withColor(rgb))`
