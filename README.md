# Simple Markdown

使用Python实现了简单的markdown解析器, 支持title, 列表, 链接, 代码段等几种格式.

## 实现方法

采用最基本的编译器前端做法, 通过lexer分析文法, 通过parser分析语法, parser生成的语法树, 通过markdown类型将其转化为html文本.

## 使用方法

提供了一个main.py脚本用于调用当前工具, 使用说明如下:

```
usage: main.py [-h] -i INPUT [-o OUTPUT]

Simple Markdown Parser

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input markdown type file
  -o OUTPUT, --output OUTPUT
                        output html file
```

示例如下:

```
python main.py -i README.md -o readme.html
```

如果没有提供-o参数, 程序将转换结果输出到标准输出中.
