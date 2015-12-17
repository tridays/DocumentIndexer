# 文档索引器

## 具体内容
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

## 系统结构
![](https://github.com/UCASExcited/DocumentIndexer/blob/master/resource/system_architecture.png)
