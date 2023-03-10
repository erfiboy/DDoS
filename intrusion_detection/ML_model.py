import os
import pandas as pd
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

def clean_data(src_path, des_path, learning_features, benign_label, ddos_label):
    if not os.path.exists(src_path):
        print("This path does not existed!")
        return

    df = pd.read_csv(src_path)
    df = df[learning_features]

    print(df.head())

    if benign_label in df[' Label'].unique() and ddos_label in df[' Label']:
        print(f"Changing {benign_label} to 0, and {ddos_label} to 1")

    df[' Label'] = df[' Label'].replace("BENIGN", 0)
    df[' Label'] = df[' Label'].replace("DDoS", 1)

    df.to_csv(des_path)

def train_model(data_path, X_columns, Y_columns, test_size = 0.7):

    df = pd.read_csv(data_path)
    X = df[X_columns]
    Y = df[Y_columns]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=42)
    
    # scale = 1 / (n_features * X.var())
    param_grid = [
        {'C': [0.1, 1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [0.1, 1, 10, 100, 1000], 'gamma': ['scale' ,0.001, 0.0001], 'kernel': ['rbf']},
    ]
    
    clf = svm.SVC(max_iter= 1000)
    grid = GridSearchCV(clf, param_grid, refit = True, verbose = 3, n_jobs=-1)
    grid.fit(X_train, y_train.values.ravel())
    print(grid.best_params_)
    with open("param", "w") as f:
        f.write(str(grid.best_params_))
    
    return grid, X_test, y_test

def test_model(grid: svm.SVC, x_test, y_test):
    y_pred = grid.predict(x_test)
    return f1_score(y_pred, y_test)

def give_malicious_packets(grid: svm.SVC, data_path):
    df = pd.read_csv(data_path)
    X_columns = [' Source IP1', ' Source IP2', ' Source IP3', ' Source IP4', ' Destination IP1',
        ' Destination IP2', ' Destination IP3', ' Destination IP4', ' Source Port', ' Destination Port', ' Protocol', ' Timestamp']
    X = df[X_columns]
    y_pred = grid.predict(X)
    indices = [i for i, x in enumerate(y_pred) if x == 1]
    
    malicious_packets = []
    for index in indices:
        malicious_packets.append({
            "src_ip": f"{X[' Source IP1'][index]}.{X[' Source IP2'][index]}.{X[' Source IP3'][index]}.{X[' Source IP4'][index]}",
            "dst_ip": f"{X[' Destination IP1'][index]}.{X[' Destination IP2'][index]}.{X[' Destination IP3'][index]}.{X[' Destination IP4'][index]}",
            "src port": f"{X[' Source Port'][index]}",
            "dst port": f"{X[' Destination Port'][index]}"}
            )
    return malicious_packets

if __name__ == "__main__":
    csv_path = input("CSV path: ")
    X_columns = [' Source IP1', ' Source IP2', ' Source IP3', ' Source IP4', ' Destination IP1',
        ' Destination IP2', ' Destination IP3', ' Destination IP4', ' Source Port', ' Destination Port', ' Protocol', ' Timestamp']
    X_columns = list(input("feature column names: ") or X_columns)
    Y_columns =  [' Label']
    Y_columns = list(input("label column names: ") or Y_columns)
    grid, x_test, y_test = train_model(data_path = csv_path, X_columns=X_columns, Y_columns=Y_columns)
    print(f"Test score on best model is: {test_model(grid, x_test, y_test)}")

