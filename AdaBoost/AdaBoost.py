#-*-coding:utf-8-*-
'''
Created on 2016年5月10日

@author: Gamer Think
'''
from test.inspect_fodder import StupidGit

__author__="thinkgamer"

from numpy import *

#加载数据集
def loadSimData():
    datMat = matrix([[1.0 , 2.1],
                     [2.  , 1.1],
                     [1.3 , 1. ],
                     [1.  , 1. ],
                     [2.  , 1. ]])
    
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

#单层决策树生成函数
def stumpClassify(dataMatrix, dimen,threshVal, threshInsq):
    retArray = ones((shape(dataMatrix)[0],1))
    if threshInsq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray

def buildStump(dataArr,classLabels,D):
    dataMatrix = mat(dataArr)
    #matrix必须是二维的，numpy可以是多维的
    labelMat = mat(classLabels).T #.T表示转置矩阵
    m,n = shape(dataMatrix)     #给定数据集的行列数
    numSteps = 10.0 #变用于在特征的所有可能值上进行遍历
    bestStump = {} #字典用于存储给定权重向量0时所得到的最佳单层决策树的相关信息
    bestClassEnt = mat(zeros((m,1)))
    minError = inf #首先将minError初始化为正无穷大
    for i in range(n):
        rangeMin = dataMatrix[:,i].min()
        rangeMax = dataMatrix[:,i].max()
        stepSize = (rangeMax-rangeMin)/numSteps
        for j in range(-1,int(numSteps)+1):
            #lt ：小于，lte，le：小于等于
            #gt：大于，，gte，ge：大于等于
            #eq：等于  ne,neq：不等于
            for inequal in ['lt','gt']:
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix,i,threshVal, inequal)
                errArr = mat(ones((m,1)))
                errArr[predictedVals==labelMat]=0
                weightedError = D.T * errArr    #计算加权错误概率
#                 print "split: dim %d, thresh % .2f, thresh inequal: %s, the weighted error is %.3f" % (i, threshVal,inequal,weightedError)
                #更新bestStump中保存的最佳单层决策树的相关信息
                if weightedError < minError:
                    minError = weightedError
                    bestClassEnt = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
     
    return bestStump,minError,bestClassEnt 
                    
#基于单层决策树的AdaBoost训练过程
#numIt：迭代次数，默认为40
def adaBoostTrainDS(dataArr,classLabels,numIt=40):
    weakClassArr = []
    m= shape(dataArr)[0]
    D = mat(ones((m,1))/m)
    aggClassEst = mat(zeros((m,1)))
    #迭代
    for i in range(numIt):
        #调用单层决策树
        bestStump,error,classEst = buildStump(dataArr, classLabels, D)  
        print "D:",D.T  #打印D的转置矩阵
        alpha = float(0.5 * log((1.0 - error) / max(error,1e-16)))# max(error,1e-16)))用于确保没有错误时，不会发生溢出
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print "classEst:",classEst.T
        #为下一次迭代计算D
        expon = multiply(-1 * alpha * mat(classLabels).T,classEst)
        D = multiply(D,exp(expon))
        D = D /D.sum()
        #错误率累加计算
        aggClassEst += alpha* classEst
        print "aggClassEst:",aggClassEst.T
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
        errorRate = aggErrors.sum()/m
        print "total error:",errorRate
        #如果不发生错误，返回
        if errorRate == 0.0:
            break
    return weakClassArr      
      

#AdaBoost分类函数
#输入参数为待分类样例datToClass和多个弱分类器classifierArr
def adaClassify(datToClass,classifierArr):
    dataMatrix = mat(datToClass)
    m = shape(dataMatrix)[0]      
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])
        aggClassEst+= classifierArr[i]['alpha'] * classEst
        print aggClassEst
    return sign(aggClassEst)

      
#main函数
if __name__=="__main__":
    #加载数据集
    datMat,classLabels = loadSimData()
#     print "datMat:",datMat
#     print "classLabels:",classLabels
    
    #单层决策树生成函数
#     D = mat(ones((5,1))/5)
#     print buildStump(datMat, classLabels, D)
    
    #基于单层决策树的Adaboost训练过程
    classifierArray = adaBoostTrainDS(datMat, classLabels, 30)
#     for classifier in classifierArray:
#         print classifier 
        
    #测试AdaBoost分类函数
    print "[0,0]:\n",adaClassify([0,0], classifierArray)
    print "\n\n[[5,5],[0,0]]:\n",adaClassify([[5,5],[0,0]], classifierArray)
