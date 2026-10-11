# 开发规范

## 注释规范

1. **统一使用 `//` 双斜杠注释**，禁止使用 `/** */` Javadoc 格式
2. 所有以下内容**必须**添加 `//` 注释：
   - 类（说明职责和设计意图）
   - 方法（说明功能、参数含义、返回值）
   - 字段/变量（说明用途，尤其是含义不直观的变量）
   - 大块逻辑（用注释分段，说明每段在做什么）
   - 其他需要解释的地方（如特殊处理、魔数、临时方案等）
3. 参数和返回值格式：
   - 参数：`// 参数名: 说明`
   - 返回值：`// 返回: 说明`
4. 不要写无意义的注释（如 `// 设置名称` 紧跟 `setName()`）

## 魔数规范

1. **禁止在逻辑代码中直接使用数字字面量**，必须提取为命名常量
2. 常量名需明确表达含义，如 `CLOSE_ENOUGH_SQ` 而非 `DIST_25`
5. **函数注释须用叙述性语言**描述其具体功能，而非仅仅列出参数类型（例：「从候选行为中按权重随机选取一个可启动的行为」而非「根据 level 和 maid 选取行为」）

## 代码风格

1. **大括号换行**：类和函数的左大括号 `{` 必须换行（Allman 风格）
   ```java
   // 正确
   public class Foo
   {
       public void bar()
       {
           // ...
       }
   }

   // 错误
   public class Foo {
       public void bar() {
           // ...
       }
   }
   ```
2. **禁止长全限定类名**：代码正文中不得出现 `net.minecraft.world.entity.ai.memory.MemoryModuleType<?>` 这类长串全限定类名，必须在文件顶部通过 `import` 引入；Java 不支持 `import Xxx = some.package.Xxx` 导入别名；频繁出现的复杂类型使用正常 import，必要时通过明确的辅助类型整理
   ```java
   // 正确
   import net.minecraft.world.entity.ai.memory.MemoryModuleType;
   import net.minecraft.world.entity.ai.memory.MemoryStatus;
   ...
   protected Foo(Map<MemoryModuleType<?>, MemoryStatus> map)
   {
       // ...
   }

   // 错误
   protected Foo(Map<net.minecraft.world.entity.ai.memory.MemoryModuleType<?>,
                   net.minecraft.world.entity.ai.memory.MemoryStatus> map)
   {
       // ...
   }
   ```
3. **用分隔线分块组织代码**：类内的方法、字段按职责用 `// ===================== 分区名 =====================` 分隔线分组，使代码结构一目了然
   ```java
   public class Foo
   {
       // ===================== 字段 =====================
       private int count;
       private String name;

       // ===================== 生命周期 =====================
       public void init()
       {
           // ...
       }
       public void dispose()
       {
           // ...
       }

       // ===================== 基类实现 =====================
       @Override
       public void tick()
       {
           // ...
       }
   }
   ```

## UI 规范

1. **禁止用物品槽里的物品图标冒充 UI 元素**：按钮、标签、页码、状态指示等一律不得用"槽位 + 物品栈（如 ARROW/PAPER + CUSTOM_NAME）"来替代，必须使用真正的 GUI 组件（`Button`/`AbstractWidget` 子类）或字体自绘文本
   - 物品槽只用于承载真实物品（背包、仓库内容等）
   - 交互控件走标准控件/菜单按钮通道（如 `clickMenuButton` + `handleInventoryButtonClick`），不得借槽位点击绕路
   ```java
   // 正确：真实按钮 + 字体文本
   this.addRenderableWidget(Button.builder(Component.literal("上一页"), b -> clickPageButton(BUTTON_PREV)).bounds(...).build());
   graphics.centeredText(this.font, pageText, this.imageWidth / 2, PAGE_TEXT_Y, PAGE_TEXT_COLOR);

   // 错误：用槽位物品当按钮/标签
   controls.setItem(BTN_PREV, new ItemStack(Items.ARROW));
   controls.setItem(LABEL_PAGE, new ItemStack(Items.PAPER));
   ```

## API 文档规范

1. **最小暴露原则**：API 文档只记录外部模块可直接调用的公共接口，禁止出现内部类、私有字段、内部注册类及实现细节
2. **层级结构**：
   - `## 大类名`：功能分类（如「AI 行为框架」「UI 模板」）
   - `### 组件名 — 名称`：一句话功能描述，紧跟 `import` 语句声明该类下所有方法所需引用的类
   - `#### 方法名`：一句话作用描述，紧跟方法签名和参数 Markdown 表格
   - 各组件间用 `---` 分隔
3. **参数表格格式**：
   ```markdown
   | 参数 | 含义 |
   |---|---|
   | player | 服务端玩家 |
   | title | 弹窗标题 |
   ```
4. **禁止包含用法示例代码块**：文档只描述接口契约，不展示调用代码
5. **完整示例**：
   ```markdown
   ## 二、UI 模板

   ### ConfirmPopup — 确认弹窗

   服务端发起、客户端渲染的双按钮模态对话框。

   \`\`\`java
   import com.fennecmomo.fenneclib.template.Data.ConfirmPopupData;
   \`\`\`

   #### 调起双按钮确认弹窗

   向指定玩家弹出确认窗口，点击按钮后自动发送命令并关闭。

   \`\`\`java
   public static void open(ServerPlayer player, String title, String info, ...)
   \`\`\`

   | 参数 | 含义 |
   |---|---|
   | player | 服务端玩家 |
   | title | 弹窗标题 |
   | info | 详细信息（空字符串不显示） |

   ---
   ```
