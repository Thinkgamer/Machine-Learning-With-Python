#-*-coding:utf-8-*-
'''
Created on 2016年5月2日

@author: Gamer Think
'''
from math import sqrt

fp = open("uid_score_bid.dat","r")

users = {}

for line in open("uid_score_bid.dat"):
    lines = line.strip().split(",")
    if lines[0] not in users:
        users[lines[0]] = {}
    users[lines[0]][lines[2]]=float(lines[1])


#----------------新增代码段END----------------------



class recommender:
    #data：数据集，这里指users
    #k：表示得出最相近的k的近邻
    #metric：表示使用计算相似度的方法
    #n：表示推荐book的个数
    def __init__(self, data, k=3, metric='pearson', n=10):

        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        if type(data).__name__ == 'dict':
            self.data = data
      
    def convertProductID2name(self, id):

        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    #定义的计算相似度的公式，用的是皮尔逊相关系数计算方法
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        
        #皮尔逊相关系数计算公式 
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n)  * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator
    
    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],self.data[instance])
                distances.append((instance, distance))

        distances.sort(key=lambda artistTuple: artistTuple[1],reverse=True)
        return distances
    
    #推荐算法的主体函数
    def recommend(self, user):
        #定义一个字典，用来存储推荐的书单和分数
        recommendations = {}
        #计算出user与所有其他用户的相似度，返回一个list
        nearest = self.computeNearestNeighbor(user)
#         print nearest
        
        userRatings = self.data[user]
#         print userRatings
        totalDistance = 0.0
        #得住最近的k个近邻的总距离
        for i in range(self.k):
            totalDistance += nearest[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
            
        #将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名
        for i in range(self.k):
            
            #第i个人的与user的相似度，转换到[0,1]之间
            weight = nearest[i][1] / totalDistance
            
            #第i个人的name
            name = nearest[i][0]

            #第i个用户看过的书和相应的打分
            neighborRatings = self.data[name]

            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist]+ neighborRatings[artist] * weight)

        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v)for (k, v) in recommendations]
        
        #做了一个排序
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

#         print recommendations[:self.n],"-------"
        return recommendations[:self.n]

def adjustrecommend(id):
    bookid_list = []
    r = recommender(users)
    print "用户id:",id
    k = r.recommend("%s" % "changanamei")
    print "推荐book:",k
    for i in range(len(k)):
        bookid_list.append(k[i][0])
    print bookid_list
        
if __name__ == '__main__':
   adjustrecommend(2)