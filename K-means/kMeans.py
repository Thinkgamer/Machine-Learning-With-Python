#coding:utf-8
'''
Created on 2015年11月9日

@author: Administrator
'''
import numpy as np

def kMeans(X, k, maxIt):
    #横纵坐标
    numPoints, numDim = X.shape
    dataSet = np.zeros((numPoints, numDim + 1))
    dataSet[: ,: -1 ] = X
    #随机产生新的中心点
    centroids = dataSet[np.random.randint(numPoints, size = k), :]
    #centroids = dataSet[0:2,:]
    #给k个中心点标签赋值为[1，k+1]
    centroids[:, -1] = range(1, k+1)
    
    iterations = 0 #循环次数
    oldCentroids = None  #用来储存旧的中心点
    
    while not shouldStop(oldCentroids, centroids, iterations, maxIt):
        print "iterations:\n ",iterations
        print "dataSet: \n",dataSet
        print "centroids:\n ",centroids
        
        #用copy的原因是进行复制，不用=是因为=相当于同时指向一个地址，一个改变另外一个也会改变
        oldCentroids = np.copy(centroids)
        iterations += 1
        
        #更新中心点
        updataLabels(dataSet, centroids)
        
        #得到新的中心点
        centroids = getCentroids(dataSet, k)
    
    return dataSet
    
def shouldStop(oldCentroids, centroids, iterations, maxIt):
    if iterations > maxIt:
        return True
    return np.array_equal(oldCentroids, centroids)


def updataLabels(dataSet, centroids):
    numPoints, numDim = dataSet.shape
    for i in range(0,numPoints):
        dataSet[i,-1] = getLabelFromCloseestCentroid(dataSet[i, :-1],centroids)
        

def getLabelFromCloseestCentroid(dataSetRow, centroids):
    label = centroids[0, -1]
    #np.linalg.norm() 计算两个向量之间的距离
    minDist = np.linalg.norm(dataSetRow - centroids[0, :-1])
    for i in range(1,centroids.shape[0]):
        dist = np.linalg.norm(dataSetRow - centroids[i,:-1])
        if dist < minDist:
            minDist = dist
            label = centroids[i,-1]
            
        print "minDist :\n" ,minDist
        return label
    
    
def getCentroids(dataSet, k):
    result = np.zeros((k, dataSet.shape[1]))
    for i in range(1, k+1):
        oneCluster = dataSet[dataSet[:,-1] == i,:-1]
        result[i - 1, :-1] = np.mean(oneCluster, axis=0)
        result[i - 1, -1] = i
        
    return result


x1 = np.array([1, 1])
x2 = np.array([2, 1])
x3 = np.array([4, 3])
x4 = np.array([5, 4])
testX = np.vstack((x1, x2, x3, x4))

result = kMeans(testX, 2, 10)
print "final result: \n",result