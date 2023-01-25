import numpy as np
from sklearn.linear_model import LinearRegression

# get the data
run = 8
with open(f"Results/result_{run}.txt", 'r') as f:
    lines = f.readlines()
    # get the data
    x = np.array(eval(lines[8]))  # number of events
    y = np.array(eval(lines[6]))  # number of jobs
    # reshape the arrays to make them 2-dimensional
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    # get the regression
    reg = LinearRegression()
    reg.fit(x, y)
    # print the results
    print(reg.intercept_[0])
    print(reg.coef_[0][0])
