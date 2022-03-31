from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, DATETIME
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# mysql需要設定使用者名稱:密碼@端口/資料庫名稱
# mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
engine_url = "mysql+pymysql://root:Jwander1098@127.0.0.1:3306/sql_test"
# 若將參數 echo 設為 True，會將所有執行的過程輸出到 cmd or terminal 上
engine = create_engine(engine_url, echo=True)

# 設定資料表結構
class Test(Base):
    __tablename__ = "test"
    # Column 建立一個欄位，此處設定id為主鍵，並自動遞增
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(55))
    time = Column(DATETIME)

# 建立資料表
def create_table():
    Base.metadata.create_all(engine)

# 刪除資料表
def drop_table():
    Base.metadata.drop_all(engine)

# 建立操作實體
def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

if __name__ == '__main__':
    drop_table()
    create_table()