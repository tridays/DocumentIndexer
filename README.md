# 文档索引器

## Task
信息检索大作业
编写索引器,构建 Shakespear-Merchant语料索引
基本要求：
* 实现 Single-pass In-memory Indexing
* 实现倒排索引的 Gamma 编码压缩 / 解压
* 实现词典的单一字符串形式压缩 / 解压,任意数据结构(如哈希表、 B 树等)
* 实现关键字的查找,命令行中 Print 给定关键字的倒排记录表
* 给出以下语料统计量:词项数量,文档数量,词条数量,文档平均长度(词条数量)
* 编程语言不限,但必须提交代码和说明文档
* 对停用词去除、词干还原等无要求,但应实现最基本的词条化功能.例如:将所有非字母和非数字字符转换为空格,不考虑纯数字词项

## System structure
![](https://github.com/UCASExcited/DocumentIndexer/blob/master/resource/system_architecture.png)

## Data information
* /data/document/ shakespeare-merchant 文档，总共22篇文档
* /data/index_block single-pass in-memory indexing 算法执行过程中生成的临时索引块, 每块默认大小为5000个<term, doc_id>项.
* /data/index 文档最终建立的索引, 文档索引采用了Gama编码, 索引原始大小?, 压缩后?, 压缩率达到了?(采用二进制bit位方式存储, 所以以文本方式读取为乱码).
* /data/stop_words 停用词表

## Code information


## Reference
* [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/): a Python package for parsing HTML and XML documents 
* [NLTK](http://www.nltk.org/): a leading platform for building Python programs to work with human language data.
* [Rejex](https://docs.python.org/2/library/re.html): Python regular expression operations

