#!/usr/bin/env python
#-*-coding:utf-8-*-
import random  
#统计各类数量  
def addValueToMat(theMat,key,value,incr):  
    if key not in theMat: #如果key没出先在theMat中  
        theMat[key]=dict();  
        theMat[key][value]=incr;  
    else:  
        if value not in theMat[key]:  
            theMat[key][value]=incr;  
        else:  
            theMat[key][value]+=incr;#若有值，则递增  
  
user_tags = dict();  
tag_items = dict();  
user_items = dict();  
user_items_test = dict();#测试集数据字典  
  
#初始化，进行各种统计  
def InitStat():  
    data_file = open('delicious.dat')  
    line = data_file.readline();   
    while line:  
        if random.random()>0.1:#将90%的数据作为训练集，剩下10%的数据作为测试集  
            terms = line.split("\t");#训练集的数据结构是[user, item, tag]形式  
            user=terms[0];  
            item=terms[1];  
            tag=terms[2];  
            addValueToMat(user_tags,user,tag,1)  
            addValueToMat(tag_items,tag,item,1)  
            addValueToMat(user_items,user,item,1)  
            line = data_file.readline();  
        else:  
            addValueToMat(user_items_test,user,item,1)  
    data_file.close();     
    
#推荐算法  
def Recommend(usr):  
    recommend_list = dict();  
    tagged_item = user_items[usr];#得到该用户所有推荐过的物品  
    for tag_,wut in user_tags[usr].items():#用户打过的标签及次数  
        for item_,wit in tag_items[tag_].items():#物品被打过的标签及被打过的次数  
            if item_ not in tagged_item:#已经推荐过的不再推荐  
                if item_ not in recommend_list:  
                    recommend_list[item_]=wut*wit;#根据公式  
                else:  
                    recommend_list[item_]+=wut*wit;  
    return sorted(recommend_list.iteritems(), key=lambda a:a[1],reverse=True)

InitStat()
recommend_list = Recommend("48411")
# print recommend_list
for recommend in recommend_list[:10]:  #兴趣度最高的十个itemid
    print recommend