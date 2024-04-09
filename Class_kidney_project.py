import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier as DCT
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,precision_score,f1_score,recall_score,confusion_matrix
from sklearn.model_selection import train_test_split as tts
data_df=pd.read_csv("kidney_disease.csv")
# print(data_df.shape)
# print(data_df.info)
# print(data_df.head(1))
data_df.drop('id',axis=1,inplace=True)
# print(data_df.head(1))
# print(data_df.describe)
data_df.columns=['age','blood_pressure','specific_gravity','albumin','sugar','rbc','pus_cell',
                 'pus_cell_clums',
                 'bacteria','bllod_pressure_random',
                 'bllod_urea','seerum_creatine','soudium',
                 'potassium','hemoglobin','packed_cell_volume','wbc_count','rbc_count','hypertension',
                 'diabetis_mellitus','coronary_artery_disease','applite','peda_edema','animia','class']
# print(data_df.head(1))
text_columns=['packed_cell_volume','wbc_count','rbc_count']
# for i in text_columns:
      # print(f"{i}:{data_df[i].dtype}")
def text_num(data_df,column):
    data_df[column]=pd.to_numeric(data_df[column],errors='coerce')
for column in text_columns:
    text_num(data_df,column)
    # print(f"{column}:{data_df[column].dtype}")

# missing_values=data_df.isnull().sum()
# print(missing_values[missing_values>0].sort_values(ascending=False).head(20))
def meanvalue_imputation(data_df,column):
    meanvalue=data_df[column].mean()
    data_df[column].fillna(value=meanvalue,inplace=True)

def modevalue_imputation(data_df,column):
    modevalue=data_df[column].mode().iloc[0]
    data_df[column].fillna(value=modevalue,inplace=True)

# print(data_df.columns)
# print(len(data_df.columns))
num_cols=[col for col in data_df.columns if data_df[col].dtype!='object']  # for numeric column
for col_name in num_cols:
    meanvalue_imputation(data_df,col_name)

cat_cols=[col for col in data_df.columns if data_df[col].dtype=='object']
for col_name in cat_cols:
    modevalue_imputation(data_df,col_name)

# missing_values=data_df.isnull().sum()
# print(missing_values[missing_values>0].sort_values(ascending=False).head(20))
# print(data_df.head(1))

                     # to find the unordered text
# print(f"diabetis_mellitus : {data_df['diabetis_mellitus'].unique()}")
# print(f"coronary_artery_disease : {data_df['coronary_artery_disease'].unique()}")
# print(f"class : {data_df['class'].unique()}")
data_df['diabetis_mellitus']=data_df['diabetis_mellitus'].replace(to_replace={' yes':'yes',
                                                                              "\tno":'no',"\tyes":'yes'})
data_df['coronary_artery_disease'] = data_df['coronary_artery_disease'].replace(to_replace='\tno', value='no')
data_df['class']=data_df['class'].replace(to_replace={'ckd\t':'ckd'})
# print(f"diabetis_mellitus : {data_df['diabetis_mellitus'].unique()}")
# print(f"coronary_artery_disease : {data_df['coronary_artery_disease'].unique()}")
# print(f"class : {data_df['class'].unique()}")



# change categorical value into numeric value
#use mappings    using 1 or 0
data_df['class']=data_df['class'].map({'ckd':1,"notckd":0})
data_df['coronary_artery_disease']=data_df['coronary_artery_disease'].map({"yes":1,"no":0})
data_df['diabetis_mellitus']=data_df['diabetis_mellitus'].map({'yes':1,"no":0})
data_df['rbc']=data_df['rbc'].map({'normal':1,"abnormal":0})
data_df['pus_cell']=data_df['pus_cell'].map({'normal':1,"abnormal":0})
data_df['pus_cell_clums']=data_df['pus_cell_clums'].map({'present':1,"notpresent":0})
data_df['bacteria']=data_df['bacteria'].map({'present':1,"notpresent":0})
data_df['hypertension']=data_df['hypertension'].map({'yes':1,"no":0})
data_df['applite']=data_df['applite'].map({'good':1,"poor":0})
data_df["peda_edema"]=data_df['peda_edema'].map({'yes':1,"no":0})
data_df["animia"]=data_df['animia'].map({'yes':1,"no":0})
# print(data_df.head(30))
plt.figure(figsize=(15,9))
sns.heatmap(data_df.corr(),annot=True)
plt.show()

target=data_df.corr()["class"].abs().sort_values(ascending=False)[1:]
# print(target)
# print(data_df['class'].value_counts())
# from sklearn.model_selection import train_test_split as tts
x=data_df.drop("class",axis=1)
y=data_df['class']
x_train,x_test,Y_train,Y_test=tts(x,y,test_size=0.25,random_state=25)
print(x_train.shape,"trainning data")
print(x_test.shape,"test data")


# tte actual machine learning algorithim

# svc = support vector confusion
dct=DCT()
dct.fit(x_train,Y_train)
Y_pred_dct=dct.predict(x_test)
# print(Y_pred_dct)
models=[]
models.append(("naive_bayes", GaussianNB()))
models.append(("KNN", KNeighborsClassifier(n_neighbors=8)))
models.append(("RandomForestclassifier", RandomForestClassifier()))
models.append(("DecisionTreeClassifier", DCT()))  # Instantiate DCT here
models.append(("SVM", SVC(kernel='linear')))


for name, model in models:
    print(name,model)
    print("\n")
    model.fit(x_train, Y_train)
    Y_pred = model.predict(x_test)
    print("accuracy:", accuracy_score(Y_test, Y_pred))
    print("precision:", precision_score(Y_test, Y_pred))
    print("recall:", recall_score(Y_test, Y_pred))
    print("f1_score:", f1_score(Y_test, Y_pred))

affected_count = np.sum(Y_pred_dct)  # Assuming Y_pred_dct contains predictions for kidney disease (1 for affected, 0 for not affected)
not_affected_count = len(Y_pred_dct) - affected_count

print("Patients affected by kidney disease:", affected_count)
print("Patients not affected by kidney disease:", not_affected_count)