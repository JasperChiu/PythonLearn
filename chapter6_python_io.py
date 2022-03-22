# Chapter6 Python IO
# 1. print
print("測試使用print印出該段文字")
x = 3.1415926
print("列印出x =", x)

# 2. 讀取檔案
f = open("read_this_file.txt", "r",encoding="utf-8")
# 讀取中文檔案時須設定UTF-8編碼，否則會報cp950的錯誤
# r是讀取; w是覆寫; a是續寫
read_file1 = f.read()
# .read 為將檔案資料全部讀取出來
print(read_file1)
f.close()
# 最後關閉檔案

with open('read_this_file.txt','r',encoding="utf-8") as f:
    read_file2 = f.read()
# 用with能簡潔的讀取檔案，且不須再關閉文件(f.close())
print(read_file2)

with open('read_this_file.txt','r',encoding="utf-8") as f:
    read_file3_single_line = f.readline()
# 僅讀取"單行"資料
print(read_file3_single_line)

with open('read_this_file.txt','r',encoding="utf-8") as f:
    read_file3_all_line = f.readlines()
# 讀取所有資料，並儲存成list的形式 (比前面的多加了s)
print(read_file3_all_line)

# 3. 讀取與修改JSON檔案
import json
with open('OldWangData.json','r',encoding="utf-8") as f:
    read_json = json.load(f) # 匯入json檔案要使用 json.load
print(read_json) # 印出初始json檔
print(type(read_json)) # 字典(dict)的形式
print(read_json["age"]) # 讀取出年紀
read_json["age"] = 40 # 將年紀該鍵值對應的資料改為40
read_json["friend"].append("LittleLee") # 在朋友的清單(list)裡新增小李的名字
print(read_json) # 印出修改過後的json檔
with open("OldWangData_renew.json",'w',encoding='utf-8') as f:
    # 將修改過的資料寫入新的檔案，若是檔案名稱相同則會直接覆寫掉舊的檔案
    json.dump(read_json, f)
    # ensure_ascii = False 是用於保存中文的json成果，此處還用不到