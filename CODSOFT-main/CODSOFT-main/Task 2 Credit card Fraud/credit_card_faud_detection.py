# -*- coding: utf-8 -*-
"""credit_card_faud_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Du-W17PISApoJKrpo3D3ukMEc4JtiejY

## CODSOFT INTERNSHIP
varad patil
120A2036

### Adding the dataset from kaggle
"""

!pip install kaggle

from google.colab import drive
drive.mount('/content/drive')

"""### make a temporary directory"""

import os
os.environ['KAGGLE_CONFIG_DIR'] = '/content/drive/MyDrive/Colab Notebooks/kaggle_dataset'

!pwd

# Commented out IPython magic to ensure Python compatibility.
# %cd drive/MyDrive/Colab Notebooks/kaggle_dataset

!pwd

!kaggle datasets download -d kartik2112/fraud-detection

!unzip fraud-detection.zip

"""### Importing Library"""

from logging import warning
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

train = pd.read_csv('fraudTrain.csv')
test = pd.read_csv('fraudTest.csv')

train.head()

train.columns

print('train:', train.shape)
print('test:', test.shape)

"""### merging both dataset"""

data = pd.concat([train, test])

data.head()

print('data:', data.shape)

data.duplicated().sum()

data.isnull().sum()

data.isnull().sum()

data.info()

data.describe()

plt.figure(figsize=(20,10))
sns.heatmap(data.corr(), annot = True)

for i in data.columns:
  num = len(data[i].unique())
  print(i,':', str(num) + str(' Distinct values'))

data.drop(columns=['Unnamed: 0'], inplace=True)

"""### calculating age from dob and transaction time"""

transaction_date = pd.to_datetime(data['trans_date_trans_time'])
birth_date = pd.to_datetime(data['dob'])
year_timedelta = np.timedelta64(1, 'Y')
data['age'] = np.int64((transaction_date - birth_date) / year_timedelta)

data.head()

"""### Data Visulaization"""

plt.figure(figsize=(20,10))
sns.countplot(x='state', data=data)
plt.title('state')
plt.xticks(rotation=90)
plt.show()

sns.countplot(x='category', data=data)
plt.title('category')
plt.xticks(rotation=90)
plt.show()

sns.countplot(data = data, x = data['is_fraud'])
plt.show()

print("Number of is_fraud data:\n\n",data['is_fraud'].value_counts())

"""from this we can see that amount fraud = 0 is more than fraud = 1. As our data is not balanced it may lead to overfitting"""

sns.countplot(x='gender', data=data)
plt.title('Gender')
plt.show()

plt.hist(data['age'], edgecolor='black')
plt.title('Age Distribution')
plt.show()

sns.set(style="whitegrid")
sns.countplot(x='gender', hue='is_fraud', data=data)
plt.title('Gender vs fraud')
plt.show()

sns.set(style="whitegrid")
sns.countplot(x='category', hue='is_fraud', data=data)
plt.title('category vs fraud')
plt.xticks(rotation=90)
plt.show()

"""### Data preprocessing"""

from sklearn.utils import resample, shuffle
df_minority = data[data['is_fraud'].values==1]
df_majority = data[data['is_fraud'].values==0]
#print(len(df_minority), len(df_majority))
df_majority_downsampled = resample(df_majority, n_samples=18427, random_state=42)
new_data = pd.concat([df_minority, df_majority_downsampled])
new_data = shuffle(new_data, random_state=42 )

new_data.head()

sns.countplot(data = data, x = new_data['is_fraud'])
plt.show()

print("Number of is_fraud data:\n\n",new_data['is_fraud'].value_counts())

sns.countplot(x='gender', hue='is_fraud', data=new_data)
plt.title('Gender vs fraud')
plt.show()

"""selecting the columns"""

drops = [ 'cc_num', 'state', 'amt', 'category', 'gender',  'job', 'age', 'is_fraud' ]

processed_data = new_data[drops]

processed_data.head()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
processed_data['gender'] = le.fit_transform(processed_data['gender'])
processed_data['category'] = le.fit_transform(processed_data['category'])
processed_data['job'] = le.fit_transform(processed_data['job'])
processed_data['state'] = le.fit_transform(processed_data['state'])

processed_data.head()

plt.figure(figsize=(20,10))
sns.heatmap(processed_data.corr(), annot = True)

#from above matrix we can say that job, state and cc_num are not that important for predicting fraud
x = processed_data.iloc[:,[2,4,6]].values
y = processed_data.iloc[:,-1:].values
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

from sklearn.linear_model import LogisticRegression
log = LogisticRegression(random_state = 0)
log.fit(x_train, y_train)

from sklearn.svm import SVC
svc = SVC(kernel = 'linear', random_state = 0)
svc.fit(x_train, y_train)

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(x_train, y_train)

classifier = [log, svc, clf]
model = ['Logistic', 'Support Vector', 'Naive Bayes']

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, ConfusionMatrixDisplay
for i in range(len(classifier)):
  y_pred = classifier[i].predict(x_test)
  cm = confusion_matrix(y_test, y_pred)
  accuracy = accuracy_score(y_test, y_pred)*100
  print('\nfor ' + str(model[i]) + ':\n')
  disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['not fraud', 'is_fraud'])
  plt.rcParams['axes.grid'] = False
  disp.plot()
  print(accuracy)
  print(classification_report(y_test, y_pred))
  plt.show()

from sklearn.model_selection import cross_val_score
for i in classifier:
  accuracies  = cross_val_score(estimator=i, X = x_train, y = y_train, cv = 10)
  print('Accuracy: {:.2f} %'.format(accuracies.mean()*100))
  print("Standard Deviation: {:.2f} %".format(accuracies.std()*100))