if __name__ == '__main__':

    data_list = [1, 5, 9]
    # 串列；存一串資料的串列容器
    data_turple = (1, 5, 9)
    # 元組；跟list效果很像，但內容不能更動，例如固定座標便適合用這種
    data_set = {1, 5, 9}
    # 集合；一堆不重複資料的集合容器，可以用於取交集、聯集運算
    data_dict = {1:10, 5:15, 9:20}
    # 字典；有索引跟內容值的字典容器，可以用索引呼叫出對應的內容值
    print(data_list)
    print(data_turple)
    print(data_set)
    print(data_dict)

    # import numpy as np
    # x = np.array([1, 2, 3])
    # print(x)
    # ratio = 3
    # result_x = x * ratio
    # print(result_x)
