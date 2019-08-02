# -*- coding: utf-8 -*-

"""
    Time    : 2019-08-02 15:29
    Author  : Thinkgamer
    File    : SlopeOne.py
    Software: PyCharm
"""

class SlopeOne:
    def __init__(self):
        self.user_rate, self.item_rate = self.loadData()

    # 加载数据
    def loadData(self):
        user_rate = {
            "U1": {"a": 2, "b": 3, "c": 3, "d": 4},
            "U2": {"b": 4, "c": 2, "d": 3, "e": 3},
            "U3": {"a": 4, "b": 2, "c": 3, "e": 2},
            "U4": {"a": 3, "c": 5, "d": 4, "e": 3}
        }
        item_rate = {
            "a": {"U1": 2, "U3": 4, "U4": 3},
            "b": {"U1": 3, "U2": 4, "U3": 2},
            "c": {"U1": 3, "U2": 2, "U3": 3, "U4": 5},
            "d": {"U1": 4, "U2": 3, "U4": 4},
            "e": {"U2": 3, "U3": 2, "U4": 3}
        }
        return user_rate,item_rate

    # 计算物品之间的评分偏差
    def cal_item_avg_diff(self):
        avgs_dict = {}
        for item1 in self.item_rate.keys():
            for item2 in self.item_rate.keys():
                avg = 0.0
                user_count = 0
                if item1 != item2:
                    for user in self.user_rate.keys():
                        user_rate = self.user_rate[user]
                        if item1 in user_rate.keys() and item2 in user_rate.keys():
                            user_count += 1
                            avg += user_rate[item1] - user_rate[item2]
                    avg = avg / user_count
                avgs_dict.setdefault(item1,{})
                avgs_dict[item1][item2] = avg
        return avgs_dict

    # 计算两个电影的共同评分人数
    def item_both_rate_user(self, item1, item2):
        count = 0
        for user in self.user_rate.keys():
            if item1 in self.user_rate[user].keys() and item2 in self.user_rate[user].keys():
                count += 1
        return count

    # 预估评分
    def predict(self, user, item, avgs_dict):
        total = 0.0 # 分子
        count = 0   # 分母
        for item1 in self.user_rate[user].keys():
            num = self.item_both_rate_user(item, item1)
            count += num
            total += num * (self.user_rate[user][item1] - avgs_dict[item][item1])
        return total/count

if __name__ == "__main__":
    slope = SlopeOne()
    avgs_dict = slope.cal_item_avg_diff()
    result = slope.predict("U2", "a", avgs_dict)
    print("U2 对 a的预测评分为: %s" % result)