# -*- coding: utf-8 -*-
"""digified-task (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VmVtwrwFQlwFJDxUSRY9Wjm6fiph6Z9z

## **Import Libariries nad Packages**
"""

# !pip install tensorflow

# !pip install --upgrade tensorflow

import pandas as pd
import numpy as np
import random
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import string
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from joblib import dump
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt

"""##**1- Data generation**

#### Read the Data
"""

arabic_names = pd.read_csv("/kaggle/input/digified/Arabic_names.csv") # first read the file arabic names which contains a varaity names between females and males 
arabic_names

Female = pd.read_csv("/kaggle/input/newdigified/Female.csv",names=["Name","Gender"]) # first read the file arabic names which contains a varaity names between females and males 
Male = pd.read_csv("/kaggle/input/newdigified/Male.csv",names=["Name","Gender"]) # first read the file arabic names which contains a varaity names between females and males

Male['Gender']="M"
Female['Gender']="F"
Female=Female.dropna()
Male=Male.dropna()

Male

all_names = pd.concat([arabic_names, Female, Male], ignore_index=True).drop(index=0)
print(len(all_names))

all_names

all_names[all_names['Name']=="سعيدة بضم السين"]
all_names = all_names.drop(all_names[all_names['Name'] == "سعيدة بضم السين"].index)

all_names = all_names.drop(all_names[all_names['Name'].str.len() == 1].index)

print("# of compound names in all_names: ", len(all_names[all_names["Name"].apply(lambda x: len(str(x).split(" ")) > 1)]))
# map list to convert compund names to be one name
map_lst = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ة": "ه",
    "ى": "ي",
    "ـ": "",
    " الدين": "الدين",
    "عبد ": "عبد",
    "ابو ": "ابو",
    "ام ": "ام",
}

for i, j in map_lst.items():
    all_names["Name"] = all_names["Name"].str.replace(i, j)


all_names.drop_duplicates(inplace=True)

all_names

print("# of compound names in all_names: ", len(all_names[all_names["Name"].apply(lambda x: len(str(x).split(" ")) > 1)]))

# a function to extract female nad male names from arabic_names csv file 
female_lst=[] #list of female names 
male_lst=[] # list of males names 
def split_gender(df):
  for index, row in df.iterrows():
    if row['Gender']=='F':
      name=row['Name']
      female_lst.append(name)
    else:
      name=row['Name']
      male_lst.append(name)

split_gender(all_names)

female_lst

print(len(male_lst))

print(len(female_lst))

"""#### Generate Real Data"""

# a function to generate a full name, 3 names separated with a space, taking into consideration
# the basic structure of the full name combination. 

def generate_real_name(list1,list2,K=0 ):
  if K: # k a variable to make sure the logical structure of a name  1 for female and 0 for male 
    full_name1 = random.choice(list1)+" "+random.choice(list2)+" "+random.choice(list2)
    return full_name1

  else: #Male+Male+Male or Female + Male + Male it is not logic that a female name being at the end or the middle 
    full_name1 = random.choice(list2)+" "+random.choice(list2)+" "+random.choice(list2)
    return full_name1

"""#### Generate Fake Data"""

# a function tha helps th create a fake name which is depend on changing a one letter
# form real name with a randome letter from aphabetic characters 

def replace_one_letter(name):

    letters = 'ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ'
    new_name=" "
    replace_set = set()

    for i in range(len(name)):
        new_name = name[:i]+ random.choice(letters)+name[i+1:] 
        if new_name == name: #to check the name after replacing a character that does not match the real name If yes, it will be skipped
            continue
        replace_set.add(new_name)
    replace_l = list(replace_set) # a set of all possible 
                           #words that can be repleaced with all char in Arabic alphabet letters

    return  random.choice(replace_l) # take a random word from the set

def replace_letter(name):
    pos = random.randint(0, len(name) - 1)
    return name[:pos] + random.choice("ابتةثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئ") + name[pos+1:]

replace_one_letter("ندي")

# a function tha helps to add one char to the name to be a fake name 
def add_one_letter(name):

    add_lst = []
    for i in range(len(name)+1):
      letter=random.choice("ابتثجحخدذرزسشصضطظعغفقكلمنهوي") # pick a random char to add to the name
      new_name = name[:i]+letter+name[i:]
      add_lst.append(new_name)
    
    return random.choice(add_lst)

# a function tha helps to delete one char from the name to be a fake name different from the real one
def remove_one_letter(name):
    index = random.randint(0, len(name))
    new_name= name[:index]+name[index+1:]
    return new_name

# a function to generate a fake  full name from the real by makes some modificatons such as add, remove and replace letter
def generate_fake_name(full_name):
  
  names = full_name.split(" ")
  first=names[0] # first name 
  second=names[1] # seconde name 
  third=names[2] # thrid name 
   


  changes = [add_one_letter, replace_one_letter, remove_one_letter] # list of changes to apply random changes
  for i in range(0,3):# each time apply different change to the real name 
      new_first = random.choice(changes)(first)
      new_second=random.choice(changes)(second)
      new_thrid=random.choice(changes)(third)



  fake_name= " ".join([new_first,new_second,new_thrid])
  return fake_name

real_example =generate_real_name(female_lst,male_lst,0) # here a generated real name from the data  
real_example

fake_example =generate_fake_name(real_example) # here a generated fake name  
fake_example

"""#### Creat dataset contain real and fake names with label"""

generate_fake_name('ناهد منتصر حسن ')

# Here, create a dataset contains real and fake names to train and test the model
fake_names=[] 
real_names=[]

for i in range(0,10000):
  if i%2==0: #female names (real and fake)
    r=generate_real_name(female_lst,male_lst,1)
    f=generate_fake_name(r)
    fake_names.append(f)
    real_names.append(r)
  else: #male names (real and fake)
    r=generate_real_name(female_lst,male_lst,0)
    f=generate_fake_name(r)
    fake_names.append(f)
    real_names.append(r)

real_df = pd.DataFrame(real_names, columns=['Name']) # DataFrame for real names 
fake_df = pd.DataFrame(fake_names, columns=['Name']) # DataFrame for fake names 

# Print the resulting DataFrame
real_df['Label']= 1   # adding 1 in the column label for real data which indicates the the name is correct
fake_df['Label']= 0   # adding 0 in the column label for fake data which indicates the the name is incorrect

# Concatenate and shuffle fake and real dataframes
result = pd.concat([real_df, fake_df], ignore_index=True)
shuffled_df = result.sample(frac=1).reset_index(drop=True)

# Print the shuffled DataFrame
shuffled_df.drop_duplicates(inplace=True)
shuffled_df

fake_names

real_names

"""##**2- Core model**

### Feature Extraction
"""

#padding function to make sure that all names has the same length
def add_padding(X):
  return np.array(list(zip(*itertools.zip_longest(*X , fillvalue=0))))

"""#### 1- Bag Of Words (BOW)"""

# initialize a CountVectorizer object
Bow = CountVectorizer()

# Fit the vectorizer on the text data
Bow.fit(shuffled_df["Name"])

# Transform the text data into a BOW matrix
bow_matrix = Bow.transform(shuffled_df["Name"])
bow_name=bow_matrix.toarray()

"""#### 2- TF_IDF

"""

# initialize the vectorizer
tfidf = TfidfTransformer(use_idf=True)

# Fit the vectorizer to the names
tfidf.fit(bow_name)

# Transform the names into a sparse matrix of TF-IDF features
tfidf_matrix = tfidf.transform(bow_name)

# print the resulting matrix
tf_names=tfidf_matrix.toarray()
tf_names

tfidf_data= add_padding(tf_names) # add padding to tf_idf names
tfidf_target=shuffled_df["Label"].to_numpy()
tf_names

"""### Train the model"""

X_train, X_test, y_train, y_test = train_test_split(tf_names, tfidf_target, random_state=42,test_size=0.2)  #split the data after TF_IDF to train and test befor Modeling

print(len(X_train[0]))

print(len(X_train))



# Build a neural network model
verify_model = Sequential()
verify_model.add(Dense(128, activation='relu'))
verify_model.add(Dropout(0.5))
verify_model.add(Dense(32, activation='relu'))
verify_model.add(Dropout(0.5))
verify_model.add(Dense(1, activation='sigmoid')) # assigne the activation to sigmoid to classify based on threshold 

# Compile the model
verify_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Train the model
verify_model_history=verify_model.fit(X_train, y_train, epochs=10, batch_size=64,validation_data=(X_test,y_test))

# Evaluate the model on the testing data
verify_model_score = verify_model.evaluate(X_test, y_test)

print('Loss: %.2f' % (verify_model_score[0]))
print('Accuracy: %.2f' % (verify_model_score[1] * 100))

verify_model.summary()

fig, ax = plt.subplots(2,1)
ax[0].plot(verify_model_history.history['loss'], color='b', label="Training loss")
ax[0].plot(verify_model_history.history['val_loss'], color='r', label="validation loss",axes =ax[0])
legend = ax[0].legend(loc='best', shadow=True)

ax[1].plot(verify_model_history.history['accuracy'], color='b', label="Training accuracy")
ax[1].plot(verify_model_history.history['val_accuracy'], color='r',label="Validation accuracy")
legend = ax[1].legend(loc='best', shadow=True)

"""### Testing the model"""

# # Define a function to classify a given text as a correcr name  or incorrect name
# def verify_name(text):

#     new_name = Bow.transform([text]).toarray()
#     new_name = tfidf.transform(new_name).toarray()
#     # Make a prediction with the model
#     prediction = verify_model.predict(new_name)[0][0]
 
#     # Classify the prediction based on a threshold
#     if prediction > 0.5:
#         print(f"{text}  is a real name with high confidence")
#     else:
#         print(f"{text} is a real name with low confidence")

# # Define a function to classify a given text as a correcr name  or incorrect name
# def verify_name3(text):
#    names= text.split(" ")
#    pred=[]
#   #  fullname_score=0
#    for name in names:
#       new_name = Bow.transform([name]).toarray()
#       new_name = tfidf.transform(new_name).toarray()
#       #prediction with the model
#       prediction = verify_model.predict(new_name)[0][0]
#       pred.append(prediction)
#   #  for p,value in enumerate(pred):
#    if pred[0]>0.5:
#     print(f"{names[0]}  the first name is written in correct way")
#    else:
#     print(f"{names[0]}  the first name is written in Incorrect way")
#    if pred[1] >0.5:
#     print(f"{names[1]}  the second name is written in correct way")
#    else:
#     print(f"{names[1]}  the second name is written in Incorrect way")
#    if pred[2] >0.5:
#      print(f"{names[2]}  the third name is written in correct way")
#    else:
#     print(f"{names[2]}  the third name is written in Incorrect way")




#   # fullname_score+=prediction

#   # #  fullname_score = fullname_score.mean()
#   #  #first case is that the three names in the full name are correct 
#   #  if fullname_score > 0.6:
#   #    print(f"{text}  is a real name with high confidence")
#   #  #second case is that the one or two names in the full name are correct
#   #  elif fullname_score < 0.3 and fullname_score < 0.6:
#   #    print(f"{text} is a real name with low confidence")
#   #  #third case is that all three names in the full name are Incorrect
#   #  else: 
#   #    print(f"{text} is Incorrect name")

# Define a function to classify a given text as a correcr name  or incorrect name
def verify_name(text):
   names= text.split(" ")
   fullname_score=0
   for name in names:
      new_name = Bow.transform([name]).toarray()
      new_name = tfidf.transform(new_name).toarray()
      #prediction with the model
      prediction = verify_model.predict(new_name)[0][0]
      fullname_score+=prediction

   fullname_score = fullname_score.mean()
   #first case is that the three names in the full name are correct 
   if fullname_score >= 0.6:
     print(f"{text}  is a real name with high confidence")
   #second case is that the one or two names in the full name are correct
   elif fullname_score > 0.3 and fullname_score < 0.6:
     print(f"{text} is a real name with meduim confidence,at least one mae is correct")
   #third case is that all three names in the full name are Incorrect
   else: 
     print(f"{text} is a real name with low confidence / Incorrect name")

print(verify_name('نجيب مغيث سمير'))

print(verify_name('منة الله صلاح الدين محمد'))

print(verify_name('ندى علي ضوي'))

print(verify_name('باسم منتصر ندي'))

print(verify_name('باسمم1 وحيد السيد'))

# Test the function on some example names

print(verify_name('مصطفي محمود نوفل')) 
print(verify_name('باسمم وحد السد'))
print(verify_name('ندى احمد الكاشف')) #failed to verifiy the name
print(verify_name('نسي منضرى حلو'))
print(verify_name('محمود رضوان محمود'))
print(verify_name('باسم وحيد السيد')) 
print(verify_name('باسمم1 وحةد السد'))
print(verify_name('محمد عطية عيد')) 
print(verify_name('سوسن السيد عوض'))
print(verify_name('ضائ غلي وسمي'))
print(verify_name('شيماء ممدوح احمد'))
print(verify_name('منة الله صلاح الدين محمد'))
print(verify_name('احمد زياده علي '))
print(verify_name('محمود يحيي احمد'))
print(verify_name('يره عبحميد وسن'))
print(verify_name('باسمم وحةد السد'))
print(verify_name('حميل سوفي جملل'))
print(verify_name('خدي ويسف كملج'))
print(verify_name('هدي يوسف كمال'))

fake_examp =generate_fake_name("مصطفي محمود نوفل")
fake_examp

for g in range(0,30):
  real_exam =generate_real_name(female_lst,male_lst,0)
  fake_examp =generate_fake_name(real_exam)
  print(verify_name(fake_examp))
  print(verify_name(real_exam))

"""### Save the model"""

# Save verification model in the h5 format to disk
verify_model.save('verification_model.h5')

# save the Bow vectorizer using joblib
dump(Bow, 'Bow_vectorizer.joblib')

# save the tfidf vectorizer using joblib
dump(tfidf, 'tfidf_vectorizer.joblib')





