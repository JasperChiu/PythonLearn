# Chapter7 try except
# 練習使用try except
# Python基本的例外錯誤處理就是將程式碼置於try區塊中
# 接著在except區塊定義當try區塊中有任一行發生例外錯誤時，需進行什麼樣的反應或處理。

# 1. 基本的例外錯誤處理(try-except)
# 錯誤範例 x是數值的型態，無法與文字相加
x = 3.14159
y = "26"
print(type(x))
print(type(y))
try:
    print(x + y)
except:
    print("發生錯誤")
print("區塊一執行完畢\n")

# 2. 不同例外錯誤處理(different exceptions)
# 根據控制台中出現的錯誤資訊，執行指定的處理方式
try:
    print(x + y)
except TypeError:
    print("型別發生錯誤")
except NameError:
    print("使用沒有被定義的對象")
except Exception:
    print("不知道怎麼了，總之發生錯誤")
print("區塊二執行完畢\n")

# 3. finally區塊(try-except-finally)
# 用途在運算完成後，要將資源釋放，否則資源將耗盡或無法開啟檔案
# 一般情況下都會放在程式碼最後面，但如果出現例外的情況，程式碼會直接中止，導致資源佔在那邊沒有釋放
# 而放在finally區塊下，不論程式碼是否有發生例外，該區塊都會執行，適合釋放外部的資源
try:
    f = open("read_this_file.txt", "r",encoding="utf-8") # 開啟之前的測試.txt檔案
    read_file = f.readline()
    print(type(read_file))
    print(type(x))
    read_file = read_file + x
    print(read_file)
except TypeError:
    print("型別發生錯誤")
except Exception:
    print("不知道怎麼了，總之發生錯誤")
finally:
    f.close()
    print("區塊三執行完畢\n")

# 4. 自行拋出例外錯誤(raise exceptions)
# 自訂當出現例外錯誤時，要拋出什麼樣的錯誤資訊
# 呼叫端一定要作例外處理，才會顯示自訂之錯誤訊息

def num0to9(input_num):
    num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # 數字清單
    print("請輸入整數數字0~9")
    if input_num not in num_list: # 若輸入值不在該清單內，則跳出ValueError
        raise ValueError('數字不在範圍內')
    print("你輸入的數字",input_num)

test_list = [0, "0", "零", 1.49, 120, -1, 9] # 測試清單
for n in test_list:
    try:
        num0to9(n)
    except ValueError as error: # 如果輸入的不是數字，執行這邊的程式
      print(error)

print('區塊四執行完畢')

# def my_name(name):
#     names = ["Jasper", "Chiu", "Chih", "Chia"]
#     if name not in names:
#         raise ValueError("not my name")
#     print(name)
# try:
#     my_name("Wang")
# except ValueError as error:
#     print(error)

