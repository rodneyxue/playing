# https://www.quantinsti.com/blog/gold-price-prediction-using-machine-learning-python/

import datetime

# LinearRegression is a machine learning library for linear regression
from sklearn.linear_model import LinearRegression

# pandas and numpy are used for data manipulation

import pandas as pd

import numpy as np

# matplotlib and seaborn are used for plotting graphs

import matplotlib as plt
plt.use('TkAgg')  #for mac using matplotlib
import seaborn

import fix_yahoo_finance as yf


now=datetime.datetime.now()

today_str=now.strftime("%Y-%m-%d")
print today_str

Df = yf.download('GLD','2008-01-01',today_str)
Df=Df[['Close']]

# Drop rows with missing values
Df= Df.dropna()

## Plot the closing price of GLD
# Df.Close.plot(figsize=(10,5))
# plt.pyplot.ylabel("Gold ETF Prices")
# plt.pyplot.show()

Df['S_3'] = Df['Close'].shift(1).rolling(window=3).mean()
Df['S_9']= Df['Close'].shift(1).rolling(window=9).mean()
Df= Df.dropna()
X = Df[['S_3','S_9']]
# print X.head()

y=Df['Close'] #store the gold ETF price in y


t=.8
t = int(t*len(Df))
# Train dataset
X_train = X[:t]
y_train = y[:t]

# Test dataset
X_test = X[t:]
y_test = y[t:]

regr=LinearRegression()

regr.fit(X_train,y_train)

print "Gold ETF Price =", round(regr.coef_[0],2), "* 3 Days Moving Average", round(regr.coef_[1],2), "* 9 Days Moving Average +", round(regr.intercept_,2)

predicted_price = regr.predict(X_test)

predicted_price = pd.DataFrame(predicted_price,index=y_test.index,columns = ['price'])

predicted_price.plot(figsize=(10,5))

r2_score = regr.score(X[t:],y[t:])*100

score = float("{0:.2f}".format(r2_score))
print score

y_test.plot()

plt.pyplot.legend(['predicted_price','actual_price'])

plt.pyplot.ylabel("Gold ETF Price")

plt.pyplot.show()

