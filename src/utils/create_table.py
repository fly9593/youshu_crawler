from sqlalchemy import create_engine

from vo.book import Base

# 数据库用户名
user = "root"
# 数据库密码
password = "root"
# 数据库地址
host = "127.0.0.1"
# 数据库名称
database_name = "crawler"

url = "mysql+pymysql://{}:{}@{}/{}".format(user, password, host, database_name)

engine = create_engine(url)

Base.metadata.create_all(engine)
