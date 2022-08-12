
from operator import mod
from sklearn import tree
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
import graphviz
from sklearn.tree import plot_tree
import numpy as np
clf=DecisionTreeClassifier(max_depth=2)


df=pd.read_csv("/Users/hudaali/Downloads/pa_philadelphia_2020_04_01.csv")

print(df.head)
#extract year from date
df['year'] = pd.DatetimeIndex(df['date']).year
le_sex=LabelEncoder()
le_race=LabelEncoder()

df=pd.DataFrame(df).fillna('none')

df=df.loc[(df['search_conducted']==True) & (df['subject_age'] !='none')]
features=['year','subject_age','subject_race','subject_sex','type']
target=['outcome']
x=df.loc[:,features]
y=df.loc[:,target]

#transforming labels with numbers
x['race_n']=le_sex.fit_transform(x['subject_race'])
x['sex_n']=le_sex.fit_transform(x['subject_sex'])
x['type_n']=le_sex.fit_transform(x['type'])
x=x.drop(['subject_race','subject_sex','type'],axis='columns')

#  TRAINING
x_train, x_test, y_train, y_test= train_test_split(x,y,random_state=0,train_size=0.8)

#  FITTING 
model=clf.fit(x_train,y_train)
print(model.predict([[2016,33,1,1,1]]))
# [1 5 2 4 0 3] 
# ['black' 'white' 'hispanic' 'unknown' 'asian/pacific islander' 'other']

feature_names=x.columns
target_names=df['outcome'].tolist()


target_names=[str(x) for x in target_names]

plot_tree(model, 
          feature_names = feature_names, 
          class_names = target_names, 
          filled = True, 
          rounded = True)
plt.savefig('tree_visualization.png')
text_representation = tree.export_text(model)

# print(x_test)
# print(model.feature_names_in_)
# print(model.feature_importances_)

'''url='https://raw.githubusercontent.com/codebasics/py/master/ML/9_decision_tree/Exercise/titanic.csv'

df=pd.read_csv(url)
df=pd.DataFrame(df)

print(df.columns)

target=['Survived']

features=['Pclass','Sex', 'Age','Fare']

x=df.loc[:,features]
y=df.loc[:,target]

le_sex=LabelEncoder()
le_age=LabelEncoder()

x['sex_n']=le_sex.fit_transform(x['Sex'])
x.Age = x.Age.fillna(x.Age.mean())
x=x.drop(['Sex'], axis='columns')

print(x.columns)
x_train, x_test, y_train, y_test=train_test_split(x,y,random_state=0,train_size=0.8)

model=clf.fit(x_train,y_train)

y_pred=model.predict(x_test)

print("Acuracy: {}".format(metrics.accuracy_score(y_test,y_pred)))

feature_names=x.columns
target_names=df['Survived'].tolist()


print(feature_names)
print(target_names)
target_names=[str(x) for x in target_names]

plot_tree(model, 
          feature_names = feature_names, 
          class_names = target_names, 
          filled = True, 
          rounded = True)
plt.savefig('tree_visualization.png') '''


