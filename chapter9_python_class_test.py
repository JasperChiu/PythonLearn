class Accumulate:
    def __init__(self, n):
        self.n = n
    def accumulate_orginal_for(self,):
        # 在執行了這個函式，便會將資訊記錄到log中
        logger.info('use accumulate_orginal_for func')
        # 使用for迴圈計算1-2+3-4+5... 循序計算複雜度O(n)
        judge_posorneg = 1
        acc_sum = 0
        for i in range(1, n+1):
            acc_sum += i * judge_posorneg
            judge_posorneg *= -1
        return acc_sum

    def accumulate_orginal_while(self,):
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

    def accumulate_math(self,):
        # 測試使用其他等級
        logger.warning('執行 accumulate_math 的函式')
        # 使用數學方式去處理，直接判斷n是奇數還是偶數，來計算最終的值，複雜度O(3)，當n很大時仍不影響計算
        determining_odd = n % 2
        if determining_odd == 1:
            return int(n + 1) / 2
        elif determining_odd == 0:
            return int(n / 2) * (-1)

class TryUseLog:
    def __init__(self):
        logger.info('嘗試在其他模組(module)上添加log日誌的紀錄，看記錄下來的資訊差異')
        5/0

if __name__ == '__main__':
    import time
    import logging
    import logging.config

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('fileAndConsole')

    # 要測試的n值，n值定義到init中，然後套用到所有method中
    n = 10 ** 7
    acc = Accumulate(n)

    start = time.time()
    print(acc.accumulate_orginal_for()) # 印出計算結果
    end = time.time()
    # print(format(end - start)) # 印出計算耗時
    # 改成將計算耗時紀錄到log檔案中
    logger.info(f'for loop done wasted {"{:.4f}".format(end - start)} sec.')

    start = time.time()
    print(acc.accumulate_orginal_while())
    end = time.time()
    # print(format(end - start))
    logger.info(f'while loop done wasted {"{:.4f}".format(end - start)} sec.')

    start = time.time()
    print(acc.accumulate_math())
    end = time.time()
    # print(format(end - start))
    logger.info(f'math calculate done wasted {"{:.4f}".format(end - start)} sec.')

    try:
        TryUseLog()
    except:
        logger.critical('critical', exc_info=True)



