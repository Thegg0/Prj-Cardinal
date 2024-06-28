import matplotlib.pyplot as plt 
import numpy as np 
from scipy import stats
from sklearn.metrics import r2_score

X = [12, 21, 22, 23, 24, 18, 16, 23, 14, 18]
y = [22, 25, 27, 22, 34, 18, 19, 20, 23, 26]

slope, intercept, r, p , std_err = stats.linregress(X,y)

def myfunc(X):
    return slope * X + intercept

mymodel = list(map(myfunc, X))

plt.scatter(X,y)
plt.plot(X, mymodel)

print(r2_score(y, mymodel))

