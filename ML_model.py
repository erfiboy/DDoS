import os
import time
import pickle
import pandas as pd
from sklearn import svm
from datetime import datetime
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

def clean_data(src_path, des_path, learning_features, Out_Column, ):
    if not os.path.exists(src_path):
        print("This path does not existed!")
        return

    df = pd.read_csv(src_path)
    df = df[learning_features]

    print(df.head())

    if 'DDoS' in df[' Label'].unique():
        print("hroa")

    df[' Label'] = df[' Label'].replace("BENIGN", 0)
    df[' Label'] = df[' Label'].replace("DDoS", 1)

    df.to_csv(des_pathdes_path)

df = pd.read_csv('./Data/Split.csv')
X = df[[ ' Source IP1',
       ' Source IP2', ' Source IP3', ' Source IP4', ' Destination IP1',
       ' Destination IP2', ' Destination IP3', ' Destination IP4', ' Source Port', ' Destination Port', ' Protocol', ' Timestamp']]
Y = df[[
    ' Label']]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.7, random_state=42)
clf = svm.LinearSVC(max_iter= 1000)
print("here")

param_grid = {'C': [0.1, 1, 10, 100, 1000], 
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
              'kernel': ['rbf']} 
grid = GridSearchCV(svm.SVC(), param_grid, refit = True, verbose = 3, n_jobs=-1)

grid.fit(X_train, y_train.values.ravel())

print(grid.best_params_)
with open("param", "w") as f:
    f.write(str(grid.best_params_))
