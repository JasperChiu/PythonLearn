# 使用for、while和數學方法計算累加數列 1-2+3-4+5-6+....+n，題目條件n是個很大的數字
# 若單純用for、while迴圈方式去寫，則複雜度會是O(n)，要計算的數字n越大越花時間，計算n=10**7時耗時1.3秒多
# 若是使用數學方式去計算則複雜度相較之下減少非常多，才是有效率的方法。

def accumulat_orginal_for(n):
    # 使用for迴圈計算1-2+3-4+5... 循序計算複雜度O(n)
    judge_posorneg = 1
    acc_sum = 0
    for i in range(1, n+1):
        acc_sum += i * judge_posorneg
        judge_posorneg *= -1
    return acc_sum

def accumulat_orginal_while(n):
    # 使用while迴圈計算1-2+3-4+5... 循序計算複雜度O(n)
    i = 1
    judge_posorneg = 1
    acc_sum = 0
    while i < (n+1):
        acc_sum += i * judge_posorneg
        judge_posorneg *= -1
        i += 1
    return acc_sum

def accumulat_math(n):
    # 使用數學方式去處理，直接判斷n是奇數還是偶數，來計算最終的值，複雜度O(3)，當n很大時仍不影響計算
    determining_odd = n % 2
    if determining_odd == 1:
        return int(n + 1) / 2
    elif determining_odd == 0:
        return int(n / 2) * (-1)

if __name__ == '__main__':
    import time
    n = 10 ** 7

    start = time.time()
    print(accumulat_orginal_for(n))
    end = time.time()
    print(format(end - start))

    start = time.time()
    print(accumulat_orginal_while(n))
    end = time.time()
    print(format(end - start))

    start = time.time()
    print(accumulat_math(n))
    end = time.time()
    print(format(end - start))