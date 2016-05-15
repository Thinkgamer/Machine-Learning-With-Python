#-*-coding:utf8-*-
'''
Created on 2016-5-15

@author: thinkgamer
'''
from numpy import *

def loadDataSet(filename,delim = "\t"):
    fr = open(filename)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [map(float, line) for line in stringArr]
    return mat(datArr)

#dataMat对应数据集，N个特征
def pca(dataMat, topNfeat=9999999):
    meanVals = mean(dataMat, axis = 0)   #求平均值
    meanRemoved = dataMat - meanVals #去平均值
    covMat = cov(meanRemoved,rowvar=0) #计算协防差矩阵
    eigVals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)
    #从小到大对N个值排序
    eigValInd = eigValInd[: -(topNfeat + 1) : -1]
    redEigVects = eigVects[:, eigValInd]
    #将数据转换到新空间
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat

#测试
dataMat = loadDataSet("testSet.txt")
lowDMat, reconMat = pca(dataMat,1)
print shape(lowDMat)

'''
#show
import matplotlib
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataMat[:,0].flatten().A[0], dataMat[:,1].flatten().A[0], marker='^',  s = 90 )
ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0],marker='o', s = 50 , c ='red' )
plt.show() 
'''

#将NaN替换成平均值函数
def replaceNanWithMean(): 
    datMat = loadDataSet('secom.data', ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i]) #values that are not NaN (a number)
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal  #set NaN values to mean
    return datMat

#加载数据               
dataMat = replaceNanWithMean()
#去除均值
meanVals = mean(dataMat, axis=0)
meanRemoved = dataMat - meanVals        
#计算协方差               
covMat = cov(meanRemoved, rowvar=0)

#特征值分析
eigVals,   eigVects = linalg.eig(mat(covMat))               
print eigVals               