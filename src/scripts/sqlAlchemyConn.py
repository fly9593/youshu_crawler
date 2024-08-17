import logging
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts import logging_config
from scripts.config import Config
from vo.book import Book

# # 设置日志配置
# logging_config.setup_logging()
# # # 使用日志记录器
# logger = logging.getLogger(__name__)


class SQLAlchemyConn(object):
    def __init__(self):
        self.conf = Config()
        url = "mysql+pymysql://{}:{}@{}/{}".format(self.conf.config["mysql"]["user"],
                                                   self.conf.config["mysql"]["password"],
                                                   self.conf.config["mysql"]["host"], "crawler")
        # self.logger = logger
        # self.logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(f"Browser_{threading.get_ident()}")
        # print(url)
        self.logger.info(f"url:{url}")
        self.engine = create_engine(url,
                                    echo=False)
        Session_class = sessionmaker(bind=self.engine)
        self.session = Session_class()

    def insert(self):
        pass

    # 插入或更新
    def insert_or_update_book(self, obj: Book):
        # 根据url进行判断,如果url相同，更新;url不同，插入
        # 添加对书名进行判断
        existing_book = self.session.query(Book).filter_by(book_url=obj.book_url, book_name=obj.book_name).first()
        if existing_book:
            self.logger.info(f"书籍《{obj.book_name}》已存在，更新中......")
            # Update existing book
            existing_book.book_name = obj.book_name
            existing_book.book_author = obj.book_author
            existing_book.book_word_count = obj.book_word_count
            existing_book.book_status = obj.book_status
            existing_book.book_update_time = obj.book_update_time
            existing_book.book_score = obj.book_score
            existing_book.book_score_count = obj.book_score_count
            existing_book.book_tag = obj.book_tag
            existing_book.update_time = obj.update_time
        else:
            # Insert new book
            self.session.add(obj)
        self.session.commit()

    def merge(self, obj: object):

        self.session.merge(obj)
        self.session.commit()
