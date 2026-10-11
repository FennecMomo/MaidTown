#!/usr/bin/env python3
"""
批量把 Markdown 文件中 ```java 代码块的 K&R 花括号转为 Allman 风格。

只处理 ```java ... ``` 之间的内容，不动 Markdown 正文和其他语言代码块。

用法：python convert_md_braces.py [目录路径]
默认处理同级 references 目录。
"""

import re, os, sys

# 默认处理同级 references 目录（可用参数指定其他目录）
BASE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIRS = [
    os.path.join(BASE, "..", "references"),
]


def is_brace_only_line(stripped):
    """这行只有 { 以及可选的注释"""
    code_part = stripped.split("//")[0].strip()
    return code_part == "{"


def convert_line_kr_to_allman(line):
    """把单行 K&R 花括号拆成两行。返回行列表。"""
    stripped = line.rstrip()

    # ---- 第一类：} else / } catch / } finally 拆分 ----

    # } else if (...) 或 } else if (...) {
    m = re.match(r"^(\s*)\}\s*else\s+if\s*(\([^)]*\))\s*(\{?)\s*$", stripped)
    if m and not is_brace_only_line(stripped):
        indent = m.group(1)
        cond = m.group(2)
        has_brace = m.group(3) == "{"
        result = [indent + "}\n"]
        if has_brace:
            result.append(indent + "else if " + cond + "\n")
            result.append(indent + "{\n")
        else:
            result.append(indent + "else if " + cond + "\n")
        return result

    # } else 或 } else {
    m = re.match(r"^(\s*)\}\s*else\s*(\{?)\s*$", stripped)
    if m and not is_brace_only_line(stripped):
        indent = m.group(1)
        has_brace = m.group(2) == "{"
        result = [indent + "}\n"]
        if has_brace:
            result.append(indent + "else\n")
            result.append(indent + "{\n")
        else:
            result.append(indent + "else\n")
        return result

    # } catch (...) {
    m = re.match(r"^(\s*)\}\s*catch\s*(\([^)]*\))\s*\{\s*$", stripped)
    if m:
        indent = m.group(1)
        cond = m.group(2)
        return [indent + "}\n", indent + "catch " + cond + "\n", indent + "{\n"]

    # } finally {
    m = re.match(r"^(\s*)\}\s*finally\s*\{\s*$", stripped)
    if m:
        indent = m.group(1)
        return [indent + "}\n", indent + "finally\n", indent + "{\n"]

    # ---- 第二类：行末有 { ----

    if not stripped.endswith("{"):
        return [line]

    if is_brace_only_line(stripped):
        return [line]

    indent = line[: len(line) - len(line.lstrip())]

    # } else if (...) {
    m = re.match(r"^(\s*\}\s*else\s+if\s*\([^)]*\)\s*)\{$", stripped)
    if m:
        before = m.group(1).rstrip()
        return [indent + before + "\n", indent + "{\n"]

    # } else {
    m = re.match(r"^(\s*\}\s*else\s*)\{$", stripped)
    if m:
        before = m.group(1).strip()
        return [indent + before + "\n", indent + "{\n"]

    # } catch (...) {
    m = re.match(r"^(\s*\}\s*catch\s*\([^)]*\)\s*)\{$", stripped)
    if m:
        before = m.group(1).rstrip()
        return [indent + before + "\n", indent + "{\n"]

    # } finally {
    m = re.match(r"^(\s*\}\s*finally\s*)\{$", stripped)
    if m:
        before = m.group(1).strip()
        return [indent + before + "\n", indent + "{\n"]

    # try {
    m = re.match(r"^(\s*try\s*)\{$", stripped)
    if m:
        before = m.group(1).strip()
        return [indent + before + "\n", indent + "{\n"]

    # lambda / switch arrow: -> {
    m = re.match(r"^(.*->\s*)\{$", stripped)
    if m:
        before = m.group(1).rstrip()
        return [indent + before + "\n", indent + "{\n"]

    # 普通行末花括号: xxx {
    before = stripped[:-1].rstrip()
    return [indent + before + "\n", indent + "{\n"]


def convert_java_block(lines):
    """转换一段 Java 代码（行列表）中的 K&R → Allman"""
    result = []
    for line in lines:
        result.extend(convert_line_kr_to_allman(line))
    return result


def process_markdown(filepath):
    """处理单个 Markdown 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 用正则找到所有 ```java ... ``` 代码块（包括未闭合的）
    pattern = re.compile(r"(```java\n)(.*?)(```|$)", re.DOTALL)

    changed = False

    def replace_block(match):
        nonlocal changed
        header = match.group(1)  # ```java\n
        code = match.group(2)    # 代码内容
        footer = match.group(3)  # ```

        code_lines = code.split("\n")
        # 保留末尾空行
        if code_lines and code_lines[-1] == "":
            code_lines = code_lines[:-1]
            trailing_empty = True
        else:
            trailing_empty = False

        # 给每行加 \n 供转换函数使用
        code_lines_with_nl = [l + "\n" for l in code_lines]
        new_lines = convert_java_block(code_lines_with_nl)

        # 去掉 \n
        new_code_lines = [l.rstrip("\n") for l in new_lines]
        if trailing_empty:
            new_code_lines.append("")

        new_code = "\n".join(new_code_lines)
        if new_code != code:
            changed = True
        return header + new_code + footer

    new_content = pattern.sub(replace_block, content)

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


if __name__ == "__main__":
    dirs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_DIRS

    total_files = 0
    changed_files = 0
    for d in dirs:
        d = os.path.normpath(d)
        if not os.path.isdir(d):
            print(f"  [SKIP] {d} (not found)")
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if not f.endswith(".md"):
                    continue
                total_files += 1
                filepath = os.path.join(root, f)
                if process_markdown(filepath):
                    changed_files += 1
                    print(f"  [FIXED] {os.path.relpath(filepath, d)}")

    print(f"\nDone: {changed_files}/{total_files} files changed.")
