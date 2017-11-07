#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Register <registerdedicated(at)gmail.com>
#
# Distributed under terms of the GPLv3 license.

"""
"""
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

# pandas 读取数据
data = pd.read_csv("Folds5x2_pp.csv")
print data.shape

# 准备样本数据和样本输出
X = data[["AT","V","AP","RH"]]
print X.shape
y = data[["PE"]]
print y.shape

linreg = LinearRegression()
linreg.fit(X_train,y_train)

# 训练模型完毕，查看结果
print linreg.intercept_
print linreg.coef_

y_pred = linreg.predict(X_test)
from sklearn import metrics

# 使用sklearn来计算mse和Rmse
print "MSE:",metrics.mean_squared_error(y_test, y_pred)
print "RMSE:",np.sqrt(metrics.mean_squared_error(y_test, y_pred))

# 交叉验证
from sklearn.model_selection import cross_val_predict
predicted = cross_val_predict(linreg,X,y,cv=10)
print "MSE:",metrics.mean_squared_error(y, predicted)
print "RMSE:",np.sqrt(metrics.mean_squared_error(y, predicted))

# 画图查看结果
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.scatter(y, predicted)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
