#Read Data
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv("subj_measures.csv",header=0)


#Reform the "date" column
import time
import datetime
reformed = []
for date in data["date"]:
    if isinstance(date,str):
        date = date[0:10]
        reformed.append(date)
data["date"]=pd.Series(reformed)


#Extract subset for mood, stress, rumination, and sleep tracking.
mood = data[data["type"]=="mood"]
sleep = data[data["type"]=="sleep"]
rumination = data[data["type"]=="ruminationStress"]
stress = data[data["type"]=="anticipatoryStress"]


#Dataset description
print("number of distinct users:", len(data["user_id"].unique()))
print("number of distinct days:", len(data["date"].unique()))
print("number of records for mood:", len(mood["value"]))
print("number of records for sleep:",len(sleep["value"]))
print("number of records for rumination stress:",len(rumination["value"]))
print("number of records for anticipatory stress:",len(stress["value"]))


#Data Explorations
#First, we create buckets for each dataset. The criterion is rounding to the nearest integer.
def CreateBucket(column):
    result = []
    for item in column:
        if item <0.5:
            result. append(0)
        elif item >= 0.5 and item <1.5:
            result. append(1)
        elif item >= 1.5 and item <2.5:
            result. append(2)
        elif item >= 2.5 and item <3.5:
            result. append(3)
        elif item >= 3.5 and item <=4:
            result. append(4)
    return pd.Series(result)


#We would like to see the proportion of all the kind of response in each Subjective Metrics questions.
mood_level = CreateBucket(mood["value"])
mood_counts = list(mood_level.groupby(mood_level).count())
sleep_level = CreateBucket(sleep["value"])
sleep_counts = list(sleep_level.groupby(sleep_level).count())
rumination_level = CreateBucket(rumination["value"])
rumination_counts = list(rumination_level.groupby(rumination_level).count())
stress_level = CreateBucket(stress["value"])
stress_counts = list(stress_level.groupby(stress_level).count())

import matplotlib.pyplot as plt
level = ["Awful", "Bad", "Okay", "Good", "Great"]
level_=["Not at all", "Slightly", "Moderately", "Very", "Extremely"]
level_.reverse()
colormap=["dimgrey","grey","silver","gainsboro","whitesmoke"]

plt.figure(figsize=(6,6))
plt.title("Mood Level Frequency for All Users All Date",{'fontsize': 16})
plt.pie(mood_counts, labels=level, colors=colormap,autopct='%1.1f%%')

plt.figure(figsize=(6,6))
plt.title("Sleep Level Frequency for All Users All Date",{'fontsize': 16})
plt.pie(sleep_counts, labels=level, colors=colormap,autopct='%1.1f%%')

plt.figure(figsize=(6,6))
plt.title("Rumination Stress Level Frequency for All Users All Date",{'fontsize': 16})
plt.pie(rumination_counts, labels=level_, colors=colormap,autopct='%1.1f%%')

plt.figure(figsize=(6,6))
plt.title("Anticipatory Stress Level Frequency for All Users All Date",{'fontsize': 16})
plt.pie(stress_counts, labels=level_, colors=colormap,autopct='%1.1f%%')

plt.show()


#Next, we are going to find how will each Subjective Metrics changes for a specific user.
def UserSubsetQuery(user_id,dataset):
    try:
        user_subset = dataset[dataset["user_id"]==user_id]
        user_data = pd.DataFrame([user_subset["date"],user_subset["value"]]).T
    except:
        print("We are missing subjective metrics data for this user.")
    return user_data

def UserQuery(user_id):
    user_mood = UserSubsetQuery(user_id,mood).set_index("date")
    user_mood.columns = ["mood"]
    user_sleep = UserSubsetQuery(user_id,sleep).set_index("date")
    user_sleep.columns = ["sleep"]
    user_rumination = UserSubsetQuery(user_id,rumination).set_index("date")
    user_rumination.columns = ["rumination"]
    user_stress = UserSubsetQuery(user_id,stress).set_index("date")
    user_stress.columns = ["stress"]
    if len(user_mood.join([user_sleep,user_rumination,user_stress],how='outer')) == 0:
        print("We are missing subjective metrics data for this user.")
    return user_mood.join([user_sleep,user_rumination,user_stress],how='outer')
    

#You can simply change user_id here:
user_id = mood["user_id"].unique()[10]
#user_id = 10
UserQuery(user_id)


#Plot these metrics' changes.
x = UserQuery(user_id).index
y1 = UserQuery(user_id)["mood"]
y2 = UserQuery(user_id)["sleep"]
y3 = UserQuery(user_id)["rumination"]
y4 = UserQuery(user_id)["stress"]

plt.figure(figsize=(20,5))
plt.title(f"Subjective Metrics Changes for User%s"%user_id, fontsize=25)
plt.plot(x,y1,'g',x,y2,'y',x,y3,'r',x,y4,'b',linewidth=2)
plt.xticks([])

plt.show()


#Let's discover a little bit more about the patients. For example, for each patient, we can calculate the average score of each metrics.
avg_mood=[]
avg_sleep=[]
avg_rumination=[]
avg_stress=[]
for user_id in list(data["user_id"].unique()):
    user_avg_data = UserQuery(user_id).mean()
    avg_mood.append(user_avg_data["mood"])
    avg_sleep.append(user_avg_data["sleep"])
    avg_rumination.append(user_avg_data["rumination"])
    avg_stress.append(user_avg_data["stress"])
user_avg_info = pd.DataFrame([data["user_id"].unique(),avg_mood,avg_sleep,avg_rumination,avg_stress]).T
user_avg_info.columns = ["user_id","avg_mood","avg_sleep","avg_rumination","avg_stress"]
user_avg_info = user_avg_info.set_index("user_id")
user_avg_info = user_avg_info.dropna()

import scipy
from scipy import optimize
def MSE(b):
    x1 = np.array(user_avg_info["avg_sleep"])
    x2 = np.array(user_avg_info["avg_rumination"])
    x3 = np.array(user_avg_info["avg_stress"])
    y =  np.array(user_avg_info["avg_mood"])
    pred =b[0] + b[1]*x1 + b[2]*x2 + b[3]*x3
    mse = sum(list(map(lambda x: x**2, y - pred)))
    return mse
    
result = scipy.optimize.minimize(MSE, [1,1,1,1])
print("The relationship between average mood and sleep, rumination/anticipatory stress scores is: ")
print("mood = % 5.2f + % 5.2f * sleep + % 5.2f * rumination stress+ % 5.2f  * anticipatory stress" % tuple(result.x))