import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.io import arff
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import seaborn as sns

def plot_heatmap(class_names, y_pred, y_test, title="Confusion Matrix"):
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 6))
    heatmap = sns.heatmap(cm, fmt='g', cmap='Blues', annot=True, ax=ax) 
    ax.set_xlabel('Predicted class',size=12)
    ax.set_ylabel('True class',size=12)
    ax.set_title(title)
    ax.xaxis.set_ticklabels(class_names) 
    ax.yaxis.set_ticklabels(class_names)
    ax.xaxis.set_ticklabels(class_names)
    plt.show()

def get_train_test_data():
    eeg_data = arff.loadarff("ML_Models/data/EEGEyeState.arff")
    eeg_df = pd.DataFrame(eeg_data[0])
    # 0 Is eyes open 1 is eyes closed
    classes_dict = {b'0': 0, b'1': 1}
    eeg_df = eeg_df.replace({"eyeDetection": classes_dict})
    labels = eeg_df.iloc[:,-1]
    data = eeg_df.iloc[:,0:-1]
    # Split training and testing data with 80/20 split.
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=1)
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = get_train_test_data()
pipeline = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=2, C=20))
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

class_names = ["Eyes Open", "Eyes Closed"]
report = accuracy_score(y_test, y_pred)
print("Accuracy: {:.3f}".format(report))
plot_heatmap(class_names, y_pred, y_test,title="Confusion Matrix")