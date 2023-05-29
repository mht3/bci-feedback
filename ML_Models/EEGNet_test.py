import glob, os
import pandas as pd
from EEGNet import EEGNet
from sklearn.model_selection import train_test_split
from scipy.io import arff
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils as np_utils
import numpy as np 

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

def get_train_test_data():
    eeg_data = arff.loadarff("ML_Models/data/EEGEyeState.arff")
    eeg_df = pd.DataFrame(eeg_data[0])
    # 0 Is eyes open 1 is eyes closed
    classes_dict = {b'0': 0, b'1': 1}
    eeg_df = eeg_df.replace({"eyeDetection": classes_dict})
    labels = np.array(eeg_df.iloc[:,-1])
    data = np.array(eeg_df.iloc[:,0:-1])
    # Split training and testing data with 80/20 split.
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=1)
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = get_train_test_data()
features = X_train.shape[1]

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

kernels = 1
chans = 64
samples = 128

X_train = X_train.reshape(X_train.shape[0], chans, samples, kernels)
X_test = X_test.reshape(X_test.shape[0], chans, samples, kernels)


# model = EEGNet(nb_classes = 2, Chans = chans, Samples = samples, 
#                dropoutRate = 0.5, kernLength = samples//2, dropoutType = 'Dropout')

# # compile the model and set the optimizers
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])  

# checkpointer = ModelCheckpoint(filepath='/tmp/checkpoint.h5', verbose=1, save_best_only=True)
# fittedModel = model.fit(X_train, y_train, batch_size = 16, epochs = 300, verbose = 2, validation_split=0.1, callbacks=[checkpointer])

# y_pred = model.predict(X_test)

# class_names = ["Eyes Open", "Eyes Closed"]
# report = accuracy_score(y_test, y_pred)
# print("Accuracy: {:.3f}".format(report))

# # plot_heatmap(class_names, y_pred, y_test,title="Confusion Matrix")