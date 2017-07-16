# coding: utf-8

from numpy import *

print '[+]------------欧式距离-----------'
def twoPointDistance(a,b):
	d = sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )
	return d

print 'a,b 二维距离为：',twoPointDistance((1,1),(2,2))

def threePointDistance(a,b):
	d = sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )
	return d

print 'a,b 三维距离为：',threePointDistance((1,1,1),(2,2,2))

def distance(a,b):
	sum = 0
	for i in range(len(a)):
		sum += (a[i]-b[i])**2
	return sqrt(sum)

print 'a,b 多维距离为：',distance((1,1,2,2),(2,2,4,4))

print '[+]------------标准欧式距离-----------'

def moreBZOSdis(a,b):
	sumnum = 0
	for i in range(len(a)):
		# 计算si 分量标准差
		avg = (a[i]-b[i])/2
		si = sqrt( (a[i] - avg) ** 2 + (b[i] - avg) ** 2 )
		sumnum += ((a[i]-b[i])/si ) ** 2
	
	return sqrt(sumnum)

print 'a,b 标准欧式距离：',moreBZOSdis((1,2,1,2),(3,3,3,4))

print '[+]------------曼哈顿距离-----------'
def twoMHDdis(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])

print 'a,b 二维曼哈顿距离为：', twoMHDdis((1,1),(2,2)) 

def threeMHDdis(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1]) + abs(a[2]-b[2])
 
print 'a,b 三维曼哈顿距离为：', threeMHDdis((1,1,1),(2,2,2)) 


def moreMHDdis(a,b):
	sum = 0 
	for i in range(len(a)):
		sum += abs(a[i]-b[i])
	return sum

print 'a,b 多维曼哈顿距离为：', moreMHDdis((1,1,1,1),(2,2,2,2)) 

print '[+]------------切比雪夫距离-----------'
def twoQBXFdis(a,b):
	return max( abs(a[0]-b[0]), abs(a[1]-b[1]))

print 'a,b二维切比雪夫距离：' , twoQBXFdis((1,2),(3,4))

def moreQBXFdis(a,b):
	maxnum = 0
	for i in range(len(a)):
		if abs(a[i]-b[i]) > maxnum:
			maxnum = abs(a[i]-b[i])
	return maxnum

print 'a,b多维切比雪夫距离：' , moreQBXFdis((1,1,1,1),(3,4,3,4))


print '[+]------------夹角余弦-----------'

def twoCos(a,b):
	cos = (a[0]*b[0]+a[1]*b[1]) / (sqrt(a[0]**2 + b[0]**2) * sqrt(a[1]**2 + b[1]**2) )

	return cos
print 'a,b 二维夹角余弦距离：',twoCos((1,1),(2,2))


def moreCos(a,b):
	sum_fenzi = 0
	sum_fenmu = 1
	for i in range(len(a)):
		sum_fenzi += a[i]*b[i]
		sum_fenmu *= sqrt(a[i]**2 + b[i]**2 )

	return sum_fenzi/sum_fenmu
print 'a,b 多维夹角余弦距离：',moreCos((1,1,1,1),(2,2,2,2))

print '[+]------------汉明距离-----------'

def hanmingDis(a,b):
	sumnum = 0
	for i in range(len(a)):
		if a[i]!=b[i]:
			sumnum += 1
	return sumnum

print 'a,b 汉明距离：',hanmingDis((1,1,2,3),(2,2,1,3))

print '[+]------------杰卡德距离-----------'

def jiekadeDis(a,b):
	set_a = set(a)
	set_b = set(b)
	dis = float(len( (set_a | set_b) - (set_a & set_b) ) )/ len(set_a | set_b)
	return dis

print 'a,b 杰卡德距离：', jiekadeDis((1,2,3),(2,3,4))

def jiekadeXSDis(a,b):
	set_a = set(a)
	set_b = set(b)
	dis = float(len(set_a & set_b)  )/ len(set_a | set_b)
	return dis

print 'a,b 杰卡德相似系数：', jiekadeXSDis((1,2,3),(2,3,4))
