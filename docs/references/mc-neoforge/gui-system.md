> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../INDEX.md).

# GUI 系统参考

> 综合 Screen / Container / Layout / Widget / 滚动 / 渲染管线

---

## 一、两种 Screen 模式

| | AbstractContainerScreen | Plain Screen |
|---|---|---|
| 继承 | `AbstractContainerScreen<MyMenu>` | `Screen` |
| 背景 | 暗底 + 灰面板 + 描边 + 槽位精灵 | 仅暗底 `0xBB000000` |
| 用途 | 有槽位的界面 | 纯信息展示界面 |
| 边距 | 布局公式计算 | `MARGIN_L=20, MARGIN_T=15` |

**Plain Screen 必须加 `extractBackground()` 空实现** — 防止 MC 画默认泥土背景。

---

## 二、渲染管线

```
extractRenderStateWithTooltipAndSubtitles
  ├─ extractBackground              ← 自定义面板/暗底
  └─ extractRenderState
       └─ extractContents
            ├─ Screen.extractRenderState  ← 渲染所有 Widget！
            ├─ translate(leftPos, topPos)
            ├─ extractLabels
            └─ extractSlots
```

**致命陷阱：双重渲染** — `extractContents` 内部调 `Screen.extractRenderState`。不要同时调 `super.extractRenderState` + `extractContents`。

正确做法：手动 translate + 只调需要的子步骤，最后 `super.extractRenderState` 一次。

---

## 三、布局系统

```java
// LinearLayout
LinearLayout layout = new LinearLayout(x, y, LinearLayout.Orientation.VERTICAL);
layout.spacing(2);
layout.arrangeElements();  // 必须调用

// GridLayout
GridLayout grid = new GridLayout(10, 10);
grid.columnSpacing(4).rowSpacing(4);
grid.arrangeElements();

// FrameLayout
FrameLayout frame = new FrameLayout(10, 10, 200, 100);
frame.addChild(widget, LayoutSettings.align(0.5F, 0.5F));  // 居中
frame.arrangeElements();
```

---

## 四、Widget 控件 API 变更（26.x）

| 旧 API | 26.x |
|---|---|
| `renderWidget(g, mx, my, pt)` | `extractWidgetRenderState(g, mx, my, pt)` |
| `mouseClicked(double, double, int)` | `mouseClicked(MouseButtonEvent, boolean)` |
| `mouseReleased(double, double, int)` | `mouseReleased(MouseButtonEvent)` |
| `onDrag(...)` | **已删除** |
| `updateWidgetNarration(NarrationElementOutput)` | **必须实现** |

### MouseButtonEvent

`event.button()` — 0=左键, 1=右键, 2=中键

---

## 五、虚拟滚动

数据全在内存，每帧只渲染可见窗口。不是"滚动 UI"，是"切换渲染范围"。

```java
totalRows = 数据总数
visibleRows = 面板高度 / 行高
maxScroll = totalRows - visibleRows
rowOffset = scrollbar.currentScroll

for (i = 0; i < visibleRows && offset + i < total; i++)
    画 data[offset + i]
```

### TaskScrollbar

MC 26.x 无原生 Scrollbar，需自写 AbstractWidget。鼠标滚轮响应（含相邻列表区域），拖拽滑块，thumb 大小按比例。

**Plain Screen 需手动转发 mouseDragged 到 scrollbar。**

---

## 六、常见陷阱

1. **addSlot 是 protected** — 必须传 `Consumer<Slot>`（`this::addSlot`）
2. **双重渲染** — 不要同时调 super.extractRenderState + extractContents
3. **Plain Screen 必须加 extractBackground 空实现**
4. **客户端线程打开 Menu 陷阱** — 单机 lambda 跑在客户端线程，用 `server.execute(() -> sp.openMenu(...))`
5. **Font.width 接受 Component 不是 String**
6. **颜色：`0xFF404040`** — 6 位裸十六进制 = alpha 0 = 透明，必须写 8 位 ARGB
7. **extractLabels 已预平移** — 不要内部再加 leftPos/topPos
