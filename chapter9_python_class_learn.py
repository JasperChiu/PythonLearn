# Class 物件 https://docs.python.org/zh-tw/3.9/tutorial/classes.html

"""A. 建立Class物件，說明解釋屬性參照"""

# Class 物件支援兩種運算：屬性參照 (attribute reference) 和實例化 (instantiation)。
# 屬性參照使用 Python 中所有屬性參照的標準語法：obj.name。
# 有效的屬性名稱是 class 物件被建立時，class 的命名空間中所有的名稱。(以下為例 i、def f 等即是有效屬性)
# 所以，如果 class definition 看起來像這樣：
class MyClass:
    # A simple example class
    i = 12345

    def f(self):
        return 'hello world'

# 那麼 MyClass.i 和 MyClass.f 都是有效的屬性參照，會分別回傳一個整數和一個函式物件。
# Class 屬性也可以被指派 (assign)，所以您可以透過賦值改變 MyClass.i 的值。
# 呼叫該物件內的屬性i
print(MyClass.i)
# 呼叫該物件內的屬性f
print(MyClass.f(None))

# 建立 class 的一個新實例，並將此物件指派給區域變數 x。
x = MyClass()
# 後續就可以該變數代替class函式
print(x.i)

"""B. 說明屬性參照下，兩種有效的屬性名稱(data attribute & method)"""
# 實例物件能理解的唯一運算就是屬性參照。有兩種有效的屬性名稱：資料屬性 (data attribute) 和 method。

# 1. 資料屬性(data attribute)不需要被宣告；和區域變數一樣，它們在第一次被賦值時就會立即存在。
# 例如，如果 x 是 MyClass 在上述例子中建立的實例，下面的程式碼將印出值 16，而不留下蹤跡
# 以下為資料屬性(data attribute)範例
# 在區域變數x中(MyClass)類別裡新增counter資料屬性
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
# 最後又偷偷將該資料屬性刪除
del x.counter

# 2. 實例的另一種屬性參照是 method。Method 是一個「屬於」物件的函式。（在 Python 中，術語 method 並不是 class 實例所獨有的：其他物件型別也可以有 method。
# 例如，list 物件具有稱為 append、insert、remove、sort 等 method。但是，在下面的討論中，我們將用術語 method 來專門表示 class 實例物件的 method，除非另有明確說明。）

# 實例物件的有效 method 名稱取決於其 class。根據定義，一個 class 中所有的函式物件屬性，就定義了實例的對應 method。
# 所以在我們的例子中，x.f 是一個有效的 method 參照，因為 MyClass.f 是一個函式，但 x.i 不是，因為 MyClass.i 不是。
# 但 x.f 與 MyClass.f 是不一樣的 — 它是一個 method 物件，而不是函式物件。(x.f是method物件；MyClass.f是函式物件，兩嚴格來講不一樣)

# 實例變數用於每一個實例的獨特資料，而 class 變數用於該 class 的所有實例共享的屬性和 method
class Dog:
    # class variable shared by all instances 所有實例共享的類變量
    kind = 'canine'

    def __init__(self, name):
        self.name = name
        # instance variable unique to each instance
        # 每個實例唯一的實例變量

d = Dog('Fido') # 指定變數e在Dog類別中的姓名實例變量為'Fido'
e = Dog('Buddy')
print(d.kind) # shared by all dogs
print(e.kind) # kind這個變數是類別內所有Dog都共享的
print(d.name) # d單獨持有的姓名
print(e.name)

# 通常，方法的第一個引數稱為 self。這僅僅只是一個慣例：self 這個名字對 Python 來說完全沒有特別的意義。
# 但請注意，如果不遵循慣例，你的程式碼可能對其他 Python 程式設計師來說可讀性較低

""" 此段僅作備註，參考性較低
# 任何一個作為 class 屬性的函式物件都為該 class 的實例定義了一個相應的 method。
# 函式定義不一定要包含在 class definition 的文本中：將函式物件指定給 class 中的區域變數也是可以的。
# Function defined outside the class (class外部定義的函式(function))
def f1(self, x, y):
    return min(x, x+y)
class C:
    f = f1
    def g(self):
        return 'hello world'
    h = g
# 現在 f、g 和 h 都是 class C 的屬性，並指向函式物件，所以他們都是class C 實例的 method —— h 與 g 是完全一樣的。
# 請注意，這種做法通常只會使該程式的讀者感到困惑。(僅做說明，可以這樣使用，但盡量不要用該方法==)
"""

"""C. 私有變數"""
# 「私有」(private) 實例變數，指的是不在物件內部便無法存取的變數，這在 Python 中是不存在的。
# 但是，大多數 Python 的程式碼都遵守一個慣例：前綴為一個底線的名稱（如：_spam）應被視為 API （應用程式介面）的非公有 (non-public) 部分（無論它是函式、方法或是資料成員）。

class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)
    __update = update   # private copy of original update() method
class MappingSubclass(Mapping): # 繼承Mapping

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)
# 在上例中，就算在 MappingSubclass 當中加入 __update 識別符，也能順利運作。
# 因為在 Mapping class 中，它會被替換為 _Mapping__update
# 而在 MappingSubclass class 中，它會被替換為 _MappingSubclass__update。

"""D. 迭代器 (Iterator)"""
# 大多數的容器 (container) 物件都可以使用 for 陳述式來進行迴圈:
for element in [1, 2, 3]:
    print(element)
for element in (1, 2, 3):
    print(element)
for key in {'one':1, 'two':2}:
    print(key)
for char in "123":
    print(char)

# 這種存取風格清晰、簡潔且方便。疊代器的使用在 Python 中處處可見且用法一致。
# 在幕後，for 陳述式會在容器物件上呼叫 iter()。
# 該函式回傳一個疊代器物件，此物件定義了 __next__() method，而此 method 會逐一存取容器中的元素。
# 當元素用盡時，__next__() 將引發 StopIteration 例外，來通知 for 終止迴圈。
# 你可以使用內建函式 next() 來呼叫 __next__() method
s = 'abc'
it = iter(s)
print(next(it))
print(next(it))
print(next(it))
# print(next(it)) # 元素用盡會報錯 __next__() 將引發 StopIteration 例外，來通知 for 終止迴圈。

""" 向後循環的迭代器，迭代器的應用，此段僅作備註
# 看過疊代器協定的幕後機制後，在你的 class 加入疊代器的行為就很容易了。
# 定義一個 __iter__() method 來回傳一個帶有 __next__() method 的物件。
# 如果 class 已定義了 __next__()，則 __iter__() 可以只回傳 self
class Reverse:
    # Iterator for looping over a sequence backwards.
    # 用於向後循環的迭代器
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
rev = Reverse('spam')
iter(rev)
for char in rev:
    print(char)
"""

"""E. 產生器 (Generator)"""
# 產生器是一個用於建立疊代器的簡單而強大的工具。
# 它們的寫法和常規的函式一樣，但當它們要回傳資料時，會使用 yield 陳述式。
# 每次在產生器上呼叫 next() 時，它會從上次離開的位置恢復執行（它會記得所有資料值以及上一個被執行的陳述式）

# yield 能一次回傳一筆資料，並保留紀錄
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
    print(char)

