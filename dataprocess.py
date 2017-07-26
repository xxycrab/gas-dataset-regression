import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import LinearRegression

def features(dataset, featureset):
    for feature in featureset:
        if not (feature in dataset.columns.tolist()):
            print feature,"is not in dataset"
            return

    return dataset[featureset]

def target(dataset, target):
    #if not (target in dataset):
     #   print target ,"is not in dataset"
      #  return
    return dataset[target]

def delMissing(featureset, target):
    if not (type(target) is 'DataFrame'):
        target = pd.DataFrame(target)
    data = pd.concat([featureset, target], axis= 1)
    data= data.replace(-200.00, np.nan).dropna(how = 'any')
    featureset, target = data[featureset.columns], data[target.columns]
    return featureset, target

def polynomia(dataset, a= 2):
    poly = preprocessing.PolynomialFeatures(a)
    dataset = poly.fit_transform(dataset)
    return dataset

def MAE(golden, pred):
    score = np.average(abs(golden - pred))
    return score

def MBE(golden, pred):
    score = np.average(golden - pred)
    return score

def baseline(golden, pred):
    golden_new = preprocessing.scale(golden)
    pred_new = preprocessing.scale(pred)
    RMSE =  np.sqrt(metrics.mean_squared_error(golden_new, pred_new))
    return RMSE

def relativeError(golden, pred):
    RE=0
    for i in range(len(golden)):
        RE = RE + abs(pred[i] - golden[i]) / golden[i]
    return RE/float(len(golden))

def sort(featureset, target, pivot):
    if not (type(target) is 'DataFrame'):
        target = pd.DataFrame(target)
    data = pd.concat([featureset, target], axis = 1)

    data = data.sort_values(by = [pivot])
    featureset, target = data[featureset.columns], data[target.columns]
    return featureset, target

def pretraining(X, y):
    linear = LinearRegression()
    model = linear.fit(X,y)
    pred = model.predict(X)
    return pred, model

def weights(X,y):
    weights = []
    pre = pretraining(X,y)
    for i in range(len(y)):
        weights.append(np.exp(-abs((y[i] - pre[i]))/0.1))
    return weights

def calibrate(X,y):
    X_new = X[:,1]
    y_new = y.copy().T
    y_new = np.reshape(y_new,(len(y_new),1))

    calibration, model = pretraining(y_new, X_new)
    for i in range(len(calibration)):
        X[i, 1] = calibration[i]
    return X, model