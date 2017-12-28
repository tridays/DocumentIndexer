__author__ = 'xp'

import os
print(os.environ)

import os

from src.term_provider import TermProvider
from src.spimi_indexer import Indexer
from src.search_engine import SearchEngine


assets_dir = os.path.join(os.getcwd(), './assets')

print('使用 SPIMI 算法建立并存储索引..')
provider = TermProvider(os.path.join(assets_dir, 'trecs'), os.path.join(assets_dir, 'stop_words'))
indexer = Indexer(provider, os.path.join(assets_dir, 'blocks'), os.path.join(assets_dir, 'index'))
indexer.build_and_save()


def dump_stat():
    doc_num = len(provider.docs)
    token_num_sum = 0
    term_num_sum = 0
    for doc in provider.docs:
        token_num_sum += doc.token_nums
        term_num_sum += doc.term_nums
    print('统计信息：文档数=%d, 词条数=%d, 词项数=%d, 文档平均长度=%f' % (
        doc_num, token_num_sum, term_num_sum, token_num_sum / doc_num
    ))


print('初始化搜索引擎..')
term_dic, r_indices = indexer.read_global_block()
engine = SearchEngine(provider.docs, term_dic, r_indices)

print("""操作提示:
    1. 搜索: g <word> [<bool-op> <word>]
       例如:
            1. g complexion
            2. g abate | abide
            3. g confirm & consider
    2. 统计: s
    3. 退出: q
""")

while True:
    try:
        cmd = input("请输入:").strip()
    except KeyboardInterrupt:
        break
    if cmd == 'q':
        break
    elif cmd == 's':
        dump_stat()
    elif cmd[:2] == 'g ':
        if len(cmd) < 3:
            print('未输入搜索字符串')
        else:
            try:
                docs = engine.search(cmd[2:])
                if len(docs) == 0:
                    print('未找到匹配结果')
                else:
                    # print('查询结果集:')
                    for i, doc in enumerate(docs):
                        print('docno=', doc.number, '\n', 'title=', doc.title, sep='')
            except ValueError as e:
                print(e.args[0])
    else:
        print('无法识别命令，请重新输入')

print('再见')
