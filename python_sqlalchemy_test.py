import datetime
from python_sqlalchemy_main import create_session
from python_sqlalchemy_main import Test

# 引入在python_sqlalchemy_main建立的操作實體
session = create_session()

# A.1. 插入單筆資料到test表格中
# 要儲存的資料
datas = {
    "name": "Jasper",
    "time": datetime.datetime.now(),
 }
try:
    session.add(Test(**datas))
    session.commit()
except Exception as e:
    print(e.__class__.__name__)
    print(str(e))
finally:
    session.close()

# A.2. 插入多筆資料到test表格中
# 將資料以串列的型態包起來並利用 session.add_all()
datas = [
    Test(name="Nick", time=datetime.datetime.now()),
    Test(name="John", time=datetime.datetime.now())
]

try:
    session.add_all(datas)
    session.commit()
except Exception as e:
    print(e.__class__.__name__)
    print(str(e))
finally:
    session.close()

# B. 修改資料
datas = {"name": "andy"}

try:
    # session.query(Test): 表示針對 Test 這個資料結構中的資料表進行查詢
    # .filter_by(id=1): 表示利用 ORM 進行資料篩選，選到指定資料
    # .update(datas) 在id=1的欄位更新指定的資料
    session.query(Test).filter_by(id=1).update(datas)
    session.commit()
except Exception as e:
    print(e.__class__.__name__)
    print(str(e))
finally:
    session.close()

# C. 刪除資料
# 原理同 update()，只是 delete() 並不需要傳入參數
try:
    session.query(Test).filter_by(id=1).delete()
    session.commit()
except Exception as e:
    print(e.__class__.__name__)
    print(str(e))
finally:
    session.close()