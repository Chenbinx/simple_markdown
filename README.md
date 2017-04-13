# Simple Markdown

使用Python实现了简单的markdown解析器, 支持title, 列表, 链接, 代码段等几种格式.

## 实现方法

采用最基本的编译器前端做法, 通过lexer分析文法, 通过parser分析语法, parser生成的语法树, 通过markdown类型将其转化为html文本.
