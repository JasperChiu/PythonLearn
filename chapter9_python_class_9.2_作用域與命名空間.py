def scope_test():
    # 區域賦值（預設情況）不會改變 scope_test 對 spam 的連結
    def do_local():
        spam = "local spam"

    # nonlocal 賦值改變了 scope_test 對 spam 的連結
    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    # 而 global 賦值改變了模組層次的連結
    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    # do_loacl內定義的spam不影響外部

    do_nonlocal()
    print("After nonlocal assignment:", spam)
    # nonlocal 語句會使得所列出的名稱指向之前在最近的包含作用域中綁定的除全局變量以外的變量。

    do_global()
    print("After global assignment:", spam)
    # global 語句是作用於整個當前代碼塊的聲明。它意味著所列出的標識符將被解讀為全局變量。
    # 要給全局變量賦值不可能不用到global 關鍵字

scope_test()
print("In global scope:", spam)