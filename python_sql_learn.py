import pymysql

# 資料庫參數設定，sql_test為預先建立好空的資料庫
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Jwander1098",
    "db": "sql_test", # 資料庫名稱
    "charset": "utf8"
}

# 基本指令與範例
# 在該資料庫下建立新的表格(設定SID為主鍵，不得重複)
sql_create_table = "CREATE TABLE UserName (SID integer,Last_Name varchar(30)," \
                   "First_Name varchar(30),PRIMARY KEY (SID))"
# 指定欄位上插入新增資料
sql_insert = "INSERT INTO UserName(SID, Last_Name, First_Name) " \
             "VALUES (%s, %s, %s) "
# 取得搜尋結果
sql_select = "SELECT * FROM UserName"
# 結合where取得指定欄位的搜索結果
sql_select_where = "SELECT * FROM UserName WHERE First_Name = %s"
# 修改，如果Last_Name為Lee，則將其First_Name改為Shao。(最好配合主鍵(key)使用)
sql_update = "UPDATE UserName SET First_Name = %s WHERE Last_Name = %s"
# 刪除，刪除指定SID的資料
sql_delete = "DELETE FROM UserName WHERE SID = %s"
# 刪除指定名稱的表格
sql_drop_table = "drop table UserName"

try:
    # 首先建立Connection物件，進入資料庫
    # 1. 讀入字典的方式進入資料庫
    conn = pymysql.connect(**db_settings)
    # 2. 也可以直接寫成單行形式
    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Jwander1098',
    #                      db='sql_test', charset='utf8')
    # 建立操作游標
    cursor = conn.cursor()

    # 執行語法
    try:
        # cursor.execute(sql_drop_table) # 刪除表格
        cursor.execute(sql_create_table) # 建立表格
        cursor.execute(sql_insert, (1, 'Wang', 'Lao'))
        cursor.execute(sql_insert, (2, 'Wang', 'Lao'))
        cursor.execute(sql_insert, (3, 'Chiu', 'Chih'))
        cursor.execute(sql_insert, (4, 'Lee', 'Lao'))

        print("列出表格內所有資料")
        cursor.execute(sql_select) # 取得搜尋結果
        # result = cursor.fetchone() # 取得單行資料
        # result = cursor.fetchmany() # 取得多行資料
        result = cursor.fetchall() # 取得所有資料
        for row in result:
            print(row)

        print("列出表格內名字為Lao的資料")
        cursor.execute(sql_select_where, ('Lao')) # 搜尋名字為'Lao'的資料
        result = cursor.fetchall()
        for row in result:
            print(row)

        print("將表格內姓Lee的名字改為Shao")
        cursor.execute(sql_update, ('Shao', 'Lee'))
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            print(row)

        print("刪除SID = 1 的資料")
        cursor.execute(sql_delete, (1))
        cursor.execute(sql_select)
        result = cursor.fetchall()
        for row in result:
            print(row)

        # 儲存變更
        conn.commit()
        print('success')
    except:
        # 發生錯誤時停止執行SQL
        conn.rollback()
        print('error')

    finally:
        # 關閉游標
        cursor.close()
        # 關閉連線
        conn.close()

except Exception as ex:
    print(ex)


""" 
# 筆記
sql = "以字串形式填入 {新增、修改、刪除的語法}"
try:
  cursor.execute(sql)
  #提交
  conn.commit()
except:
  #發生錯誤時停止執行SQL
  conn.rollback()
  print('error')
  
# 關閉物件
# 關閉游標
cursor.close()
# 關閉連線
conn.close()

# 也可以使用 python 的 with 語法來連接資料庫及執行 SQL 語法，在 with 區塊結束後
# connection 及 cursor 都會自動關閉。
with pymysql.connect(...) as conn:
    with conn.cursor(...) as cursor:
"""