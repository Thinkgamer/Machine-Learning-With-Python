#coding:utf-8
'''
Created on 2016/4/24

@author: Gamer Think
'''

from numpy import *

#加载数据集
def loadDataSet():
    dataMat = []
    labelMat = []
    fp = open("ex1.txt")
    for line in fp.readlines():
        lineArr = line.strip().split() #分割
        dataMat.append([1.0,float(lineArr[0]), float(lineArr[1])])
        labelMat.append( int(lineArr[2]))
        
    return dataMat,labelMat

#定义Sigmoid函数
def sigmoid(inX):
    return 1.0/(1+exp(-inX))

#梯度上升算法求解最佳回归系数
def gradAscent(dataMatIn,classLabels):
    dataMatrix = mat(dataMatIn) #将数组转为矩阵
    labelMat = mat(classLabels).transpose()
    m,n = shape(dataMatrix)      #返回矩阵的行和列
    alpha = 0.001      #初始化 alpha的值
    maxCycles = 500    #最大迭代次数
    weights = ones((n,1)) #初始化最佳回归系数
    for i in range(0,maxCycles):
        #引用原书的代码，求梯度
        h = sigmoid(dataMatrix*weights)
        error = labelMat - h
        weights = weights + alpha * dataMatrix.transpose() * error
        
    return weights
   
#随机梯度上升算法求回归系数
def stocGradAscent0(dataMatrix,labelMat): 
    dataMatrix = array(dataMatrix)
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(0,m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = labelMat[i] - h
        weights = weights + alpha *  error * dataMatrix[i]
    
    return weights
        
    
#改进版的随机梯度上升算法
def stocGradAscent1(dataMatrix,labelMat,numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for i in range(0,numIter):
        dataIndex = range(m)
        for j in range(0,m):
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex] * weights))
            error = labelMat[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
        
    return weights       

#分析数据，画出决策边界
def plotBestFit(wei,dataMatrix,labelMat):
    import matplotlib.pyplot as plt
    weights = wei     #将矩阵wei转化为list
    dataArr = array(dataMatrix)  #将矩阵转化为数组
    n = shape(dataMatrix)[0]
    xcord1 = [];ycord1=[]
    xcord2 = [];ycord2=[]
    
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red', marker='s')
    ax.scatter(xcord2,ycord2,s=30,c="green")
    x = arange(-3.0,3.0,0.1)
    y = (-weights[0]-weights[1] * x)/weights[2]
    ax.plot(x,y)
    plt.xlabel("x1")     #X轴的标签
    plt.ylabel("x2")     #Y轴的标签
    plt.show()
            
            
            
if __name__=="__main__":
    dataMatrix,labelMat = loadDataSet()
    #梯度上升算法
#     weight = gradAscent(dataMatrix, labelMat)
#     print weight
#     plotBestFit(weight.getA(),dataMatrix,labelMat)

    #随机梯度上升算法
#     weight = stocGradAscent0(dataMatrix, labelMat)
#     print weight
#     plotBestFit(weight,dataMatrix,labelMat)
    
    #改进版的随机梯度上升算法
    weight = stocGradAscent1(array(dataMatrix), labelMat)
    print weight
    plotBestFit(weight,dataMatrix,labelMat)
    
    