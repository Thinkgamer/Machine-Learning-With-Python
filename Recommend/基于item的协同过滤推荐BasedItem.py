#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Created on 2016-5-30

@author: thinkgamer
'''
import math

class ItemBasedCF:
    def __init__(self,train_file):
        self.train_file = train_file
        self.readData()
    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        for line in open(self.train_file):
            # user,item,score = line.strip().split(",")
            user,score,item = line.strip().split(",")
            self.train.setdefault(user,{})
            self.train[user][item] = int(float(score))

    def ItemSimilarity(self):
        #建立物品-物品的共现矩阵
        C = dict()  #物品-物品的共现矩阵
        N = dict()  #物品被多少个不同用户购买
        for user,items in self.train.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i] += 1
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j : continue
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W

    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=3,N=10):
        rank = dict()
        action_item = self.train[user]     #用户user产生过行为的item和评分
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])
    
#声明一个ItemBased推荐的对象    
Item = ItemBasedCF("uid_score_bid")
Item.ItemSimilarity()
recommedDic = Item.Recommend("xiyuweilan")
for k,v in recommedDic.iteritems():
    print k,"\t",v