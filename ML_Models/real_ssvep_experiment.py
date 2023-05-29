import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import seaborn as sns
import glob
import shap

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

frequencies = [2.5, 3, 3.5]
labels_dict = {i:frequencies[i] for i in range(len(frequencies))}

def format_data(frequencies = [2.5, 3, 3.5]):
    '''
    Reads all csv files, adds a handpicked label for each LED, and converts to one giant data frame.
    Note that you must be in the main bci-feedback folder to run this program.
    '''
    led_data = []
    for i in range(1,len(frequencies)+1):
        for name in glob.glob('Experiment_Data/Person*/*/LED[{}].csv'.format(i)):
            df = pd.read_csv(name, header=None, sep="\t", usecols=range(1,9))
            # Manually Add a label of 0, 1, 2
            labels = [i - 1]*df.shape[0]
            df["Label"] = labels
            led_data.append(df)
            
    dataset = pd.concat(led_data, axis=0, ignore_index=True)
    return dataset

# Split into training and testing data
dataset = format_data()
data = dataset.iloc[:,0:-1]
labels = dataset.Label
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=20)

# Create a SVM pipeline
gamma, C = (20, 2)
pipeline = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=gamma, C=C))
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# shap explainability
# X_train_summary = shap.kmeans(X_train, 10)
# svm_explainer = shap.KernelExplainer(pipeline.predict, X_train_summary)
# svm_shap_values = svm_explainer.shap_values(X_test)

# summary plot
# shap.summary_plot(svm_shap_values, X_test)

# dependence plot
# shap.dependence_plot("alcohol", svm_shap_values, X_test)

# individual force plot
# plot the SHAP values for the 10th observation 
# shap.force_plot(svm_explainer.expected_value,svm_shap_values[10,:], X_test.iloc[10,:])

# collective force plot
# shap.force_plot(svm_explainer.expected_value, svm_shap_values, X_test)

class_names = ["2.5 Hz", "3 Hz", "3.5 Hz"]
report = accuracy_score(y_test, y_pred)
print("Accuracy: {:.3f}".format(report))
plot_heatmap(class_names, y_pred, y_test,title="SSVEP Confusion Matrix")