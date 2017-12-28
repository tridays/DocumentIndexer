# document-indexer

## 任务

基本要求：构建词典和倒排索引

- 实现 Single-pass In-memory Indexing
- 实现倒排索引的 Gamma 或 VB 编码压缩 / 解压
- 实现词典的单一字符串形式压缩 / 解压，任意数据结构（如哈希表、 B 树等）
- 实现关键字的查找，命令行中 Print 给定关键字的倒排记录表
- 给出以下语料统计量：词项数量，文档数量，词条数量，文档平均长度（词 条数量）
- 编程语言不限，但必须提交代码和说明文档

对停用词去除、词干还原等无要求，但应实现最基本的词条化功能

- 例如：将所有非字母和非数字字符转换为空格，不考虑纯数字词项

## 环境要求

- Python 3.6 (for typing hits)
- Unix-like OS

## 运行

```sh
$ ./run.sh
```

## 代码结构

所有代码置于 `src` 包下。

- `__main__.py` 程序入口
- `binutils.py` 对 int 和 bytes 的互转函数
- `compression.py` 单一字符串压缩器
- `document.py` Document 数据结构
- `gamma_encoder.py` Gamma 编码器
- `parser.py` 语料 XML 解析器
- `search_engine.py` 搜索模块
- `spimi_indexer.py` SPIMI 模块
- `term_provider.py` 词项流提供器（对 `Parser` 和 `Tokenizer` 的封装）
- `tokenizer.py` 分词、词项提取器

处理流程为

```
索引构建
source -> Parser -> Tokenizer -> TermProvider -> Spimi-Indexer

搜索
query -> Tokenizer -> SearchEngine
```

## 数据描述

源数据和处理结果置于 `assets` 目录下。

- `trecs/*` 输入文档，共 2 文件 22 篇（1 空）
- `stop_words` 停用词表
- `blocks/*` 分块的索引
- `index/*` 最终索引
