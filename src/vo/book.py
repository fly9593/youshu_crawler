from sqlalchemy import Column, Integer, String, Double, DateTime, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'youshu_book'
    book_id = Column(BigInteger, primary_key=True)
    book_name = Column(String(255))
    book_author = Column(String(255))
    book_url = Column(String(255))
    book_word_count = Column(String(255))
    book_status = Column(String(255))
    # 优书网书籍信息更新时间
    book_update_time = Column(String(255))
    book_score = Column(Float)
    book_score_count = Column(Integer)
    book_tag = Column(String(255))
    # 数据库更新时间
    update_time = Column(DateTime)

    def __repr__(self):
        return (
            "Book("
            "book_id={}, "
            "book_name={}, "
            "book_author={}, "
            "book_url={}, "
            "book_word_count={}, "
            "book_status={}, "
            "book_update_time={}, "
            "book_score={}, "
            "book_score_count={}, "
            "book_tag={}, "
            "update_time={}"
            ")".format(
                self.book_id,
                self.book_name,
                self.book_author,
                self.book_url,
                self.book_word_count,
                self.book_status,
                self.book_update_time,
                self.book_score,
                self.book_score_count,
                self.book_tag,
                self.update_time
            )
        )

    def info_check(self):
        # 字段为空
        if not self.book_name:
            raise ValueError("Book name cannot be null or empty")
        if not self.book_author:
            raise ValueError("Book author cannot be null or empty")
        if not self.book_url:
            raise ValueError("Book URL cannot be null or empty")
        if not self.book_word_count:
            raise ValueError("Book word count cannot be null or empty")
        if not self.book_status:
            raise ValueError("Book status cannot be null or empty")
        if not self.book_update_time:
            raise ValueError("Book update time cannot be null or empty")
        if self.book_score is None:
            raise ValueError("Book score cannot be null")
        if self.book_score_count is None:
            raise ValueError("Book score count cannot be null")
        if not self.book_tag:
            raise ValueError("Book tag cannot be null or empty")
        if not self.update_time:
            raise ValueError("Update time cannot be null")

        # Check for '万字' or '字' in book_word_count
        if '万字' not in self.book_word_count and '字' not in self.book_word_count:
            raise ValueError("Book word count must contain '万字' or '字'")

        # 评分小于0，但是评分人数大于0
        if self.book_score < 0 and self.book_score_count > 0:
            raise ValueError("评分异常，评分小于0，但是评分人数大于0")

        # 评分人数小于0，但是评分大于0
        if self.book_score_count < 0 and self.book_score > 0:
            raise ValueError("评分异常，评分人数小于0，但是评分大于0")
