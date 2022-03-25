class Accumulate:
    def accumulate_orginal_for(self, n):
        # 在執行了這個函式，便會將資訊記錄到log中
        logger.info('use accumulate_orginal_for func')
        # 使用for迴圈計算1-2+3-4+5... 循序計算複雜度O(n)
        judge_posorneg = 1
        acc_sum = 0
        for i in range(1, n+1):
            acc_sum += i * judge_posorneg
            judge_posorneg *= -1
        return acc_sum

    def accumulate_orginal_while(self, n):
        # 測試能否填入中文
        logger.info('執行 accumulate_orginal_while 的函式')
        # 使用while迴圈計算1-2+3-4+5... 循序計算複雜度O(n)
        i = 1
        judge_posorneg = 1
        acc_sum = 0
        while i < (n+1):
            acc_sum += i * judge_posorneg
            judge_posorneg *= -1
            i += 1
        return acc_sum

    def accumulate_math(self, n):
        logger.warning('執行 accumulate_math 的函式')
        # 使用數學方式去處理，直接判斷n是奇數還是偶數，來計算最終的值，複雜度O(3)，當n很大時仍不影響計算
        determining_odd = n % 2
        if determining_odd == 1:
            return int(n + 1) / 2
        elif determining_odd == 0:
            return int(n / 2) * (-1)

if __name__ == '__main__':
    import time
    import logging
    import logging.config

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('fileAndConsole')

    acc = Accumulate()
    # 要測試的n值
    n = 10 ** 7

    start = time.time()
    print(acc.accumulate_orginal_for(n))
    end = time.time()
    print(format(end - start))
    logger.info('for loop done', exc_info=True)

    start = time.time()
    print(acc.accumulate_orginal_while(n))
    end = time.time()
    print(format(end - start))
    logger.info('while loop done', exc_info=True)

    start = time.time()
    print(acc.accumulate_math(n))
    end = time.time()
    print(format(end - start))
    logger.info('math calculate done', exc_info=True)
