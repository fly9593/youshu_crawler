# 说明
优书网爬虫  

用于爬取优书网书库信息，可以导到数据库里面按照评分和评分人数排序  

没有做爬取书籍评论的部分，暂时没这个需求  

查看书库不需要登录，所以不需要cookie,cookie.dat那个文件空着也没事

这里提供的是谷歌浏览器驱动，版本号：127.0.6533.88。如果版本号不一致，请访问：
https://googlechromelabs.github.io/chrome-for-testing/  

如果用的是其他浏览器，请自行搜索驱动并修改browser.py文件  

代码仅供个人学习使用，严禁修改config.ini文件中的base_url为优书网首页地址，并运行main.py或setup.py文件

进行上述错误操作可能导致的各种法律风险作者概不负责 

另外，除非您时间很多，否则请不要单线程运行该代码

由于作者水平有限，该代码属于那种......完全视各种编程规范为无物，想到哪里写到哪里，怎么方便怎么来，一边跑一边测试还一边改的绿皮代码，若要修改，希望您能保持一颗纯真而平静的内心  

如果您看到这里，祝您生活愉快


# 文件结构
```plaintext
|-- resources/
  |-- result/
    |-- youshu_book.sql         # 建表语句
  |-- chromedriver.exe          # 谷歌浏览器驱动
  |-- config.ini                # 配置文件
  |-- cookie.dat                # 里面放cookie数据，暂时没有用到
|-- src/
  |-- html/
    |-- example.html            # 优书网书库html示例代码
  |-- scripts/
    |-- browser.py              # 爬虫代码
    |-- config.py               # configparser配置类
    |-- logging_config.py       # logging配置文件
    |-- sqlAlchemyConn.py       # 包含操作数据库的一些方法
  |-- utils/                    # 包含一些好用的工具
    |-- get_cookie.py           # 用于获取cookie
    |-- show_file_tree_md.py    # 用于在控制台打印像左边一样的结构树
  |-- vo/
    |-- book.py                 # 实体类，顺带一提，可以使用sqlalchemy自动创建表
  |-- __init__.py
  |-- main.py                   # 单线程运行入口，可以从命令行接受两个参数，可以通过控制台或者pycharm开多个窗口实现伪多线程
  |-- setup.py                  # 单线程运行入口，在脚本中修改两个参数
|-- README.md                   # 说明文件
```


# 数据库设计
表：youshu_book

| 名称               | 类型       | 说明          |
|------------------|----------|-------------|
| book_id          | INT      | id          |
| book_name        | VARCHAR  | 书名          |
| book_author      | VARCHAR  | 作者          |
| book_url         | VARCHAR  | url         |
| book_word_count  | VARCHAR  | 字数（单位：万字）   |
| book_status      | VARCHAR  | 更新状态        |
| book_update_time | VARCHAR  | 优书网书籍信息更新时间 |
| book_score       | DOUBLE   | 评分          |
| book_score_count | INT      | 评分人数        |
| book_tag         | VARCHAR  | 标签          |
| update_time      | DATETIME | 数据库更新时间     |
