#-*-coding:utf-8-*-
'''
Created on 2016年5月9日

@author: Gamer Think
'''
import FP_Tree

#将数据集加载到列表
parsedDat = [line.split() for line in open('kosarak.dat').readlines()]
print parsedDat

#初始集合格式化
initSet = FP_Tree.createInitSet(parsedDat)

#构建FP树
myFPtree, myHeaderTab = FP_Tree.createTree(initSet, 100000)

#创建空列表，保存频繁项集
myFreqList = []
FP_Tree.mineTree(myFPtree, myHeaderTab, 100000, set([]), myFreqList)
print len(myFreqList)
print myFreqList