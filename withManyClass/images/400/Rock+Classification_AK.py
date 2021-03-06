


import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import os
import cv2
import joblib
from sklearn.model_selection import train_test_split
from autokeras import ImageClassifier



DATADIR="/home/jafar/Desktop/Master/jafar/Sem4/Rock Classification/withManyClass/images/400"
#CATEGORIES=["Aaaa", "interflw","pahoehoe","transi"]
#CATEGORIES=["Aaa_enta","Aaa_lava ball","inter_brown","inter_red","pa_domed vesicle","pa_gas cavity","pa_inflection1","pa_inflection2","pa_joints","pa_pipes","pa_pipes and vesicles","pa_ropes","pa_squeezeup","pa_sq up","pa_toes","pa_vesicle banding","pa_vesicle cyl","tr_ftb 800","tr_rubbly","tr_slabby"]

CATEGORIES=[
'Aaa_enta','Aaa_lava ball',
'inter_brown','inter_red',
'pa__hummocky_inflection1','pa_hummocky_inflection2','pa_hummocky_ropes',
'pa_hummocky_squeezeup','pa_hummocky_toes',
'pa_sheet_domed vesicle','pa_sheet_gas cavity','pa_sheet_joints',
'pa_sheet_pipes and vesicles','pa_sheet_sq up','pa_sheet_vesicle banding','pa_sheet_vesicle cyl',
'tr_ftb','tr_rubbly','tr_slabby']

numclasses=len(CATEGORIES)


plt.ion()
for category in CATEGORIES:
    path=os.path.join(DATADIR,category)
    for img in os.listdir(path):
        img_array=cv2.imread(os.path.join(path,img))
        plt.imshow(img_array)
        plt.show()
        plt.close('all')
        break
    break

print("Here")

IMG_SIZE=300
new=cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
plt.imshow(new)
plt.show()


#img_array



rock_data=[]
def create_rock_data():
    for category in CATEGORIES:
        path=os.path.join(DATADIR,category)
        class_num=CATEGORIES.index(category)
        for img in os.listdir(path):
            img_array=cv2.imread(os.path.join(path,img))
            #print(np.shape(img_array) ,class_num)
            new_array=cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
            rock_data.append([new_array,class_num])

create_rock_data()
print("Rock data created")

# for i in training_data:
#     #print(i)
#     height, width = i.shape[:2]
#     break

# In[18]:


import random
random.shuffle(rock_data)
X=[]
y=[]
for features, label in rock_data:
    X.append(features)
    y.append(label)
X=np.array(X).reshape(-1,IMG_SIZE,IMG_SIZE,3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42,shuffle=True,stratify=y)

# In[19]:
# PLotting Class imbalance in the data
fig=plt.figure(figsize=(10, 5), dpi= 80, facecolor='w', edgecolor='k')
Y=pd.Series(y)

class_counts=Y.value_counts()
print(class_counts.index)
cats=pd.Series(CATEGORIES).iloc[class_counts.index]
#plt.hist(y,bins=numclass, color='#0504aa',alpha=0.7, rwidth=0.85)
plt.scatter(cats,class_counts,s=100)
plt.xticks(rotation=90)
plt.title("Plot to show Class Imbalance")
plt.show()


#pickle_out=open("X.pickle","wb")
#pickle.dump(y,pickle_out)
#pickle_out.close()





#X=np.divide(X,255)




"""
def rock_classifier():
    model=Sequential()

    model.add(Conv2D(20,(2,2),input_shape=X.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64,(2,2)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64,(2,2)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64,(2,2)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64,(2,2)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(100))

    model.add(Dense(numclasses))
    model.add(Activation('softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
    #model.fit(X,y,batch_size=1,epochs=30, validation_split=0.1)
    return model
#rock_classifier()
"""



clf = ImageClassifier(verbose=True, augment=False)
clf.fit(X_train, y_train, time_limit=12 * 60 * 60)
clf.final_fit(X_train, y_train, X_test, y_test, retrain=True)

y = clf.evaluate(X_test, y_test)
print(y * 100)



#X.shape[0:]


# ### CV accuracy



"""
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline




kfold = KFold(n_splits=5, shuffle=True)




estimator = KerasClassifier(build_fn=rock_classifier, epochs=25, batch_size=1,verbose=1)
results=cross_val_score(estimator, X, y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

filename='results_800_5.sav'
joblib.dump(results, filename)
"""
