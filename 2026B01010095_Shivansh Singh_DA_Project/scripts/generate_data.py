"""Generate a SYNTHETIC student performance dataset for learning purposes.
No real student data is used. Run: python scripts/generate_data.py"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
n = 250
branch = rng.choice(['CSE','IT','ECE','ME','CE'], n, p=[.30,.20,.20,.15,.15])
gender = rng.choice(['Male','Female'], n, p=[.58,.42])
residence = rng.choice(['Hostel','Day Scholar'], n, p=[.45,.55])
attendance = np.clip(rng.normal(76, 12, n), 40, 100).round(1)
study = np.clip(rng.normal(12, 5, n), 1, 30).round(1)
sleep = np.clip(rng.normal(6.8, 1.0, n), 4, 9).round(1)
tutoring = rng.choice(['Yes','No'], n, p=[.3,.7])
ability = rng.normal(0, 1, n)
def marks(w):
    m = 28 + 0.32*attendance + 1.0*study + 5*ability + w + (tutoring=='Yes')*3 + rng.normal(0, 6, n)
    return np.clip(m, 5, 100).round(0)
maths, physics, programming = marks(0), marks(-2), marks(2)
df = pd.DataFrame({'Student_ID':[f'S{1001+i}' for i in range(n)],'Gender':gender,'Branch':branch,
  'Residence':residence,'Attendance_Pct':attendance,'Study_Hours_Per_Week':study,'Sleep_Hours':sleep,
  'Tutoring':tutoring,'Maths_Marks':maths,'Physics_Marks':physics,'Programming_Marks':programming})
# Introduce realistic data-quality problems for the cleaning exercise
for col, k in [('Attendance_Pct',6),('Study_Hours_Per_Week',5),('Maths_Marks',4),('Sleep_Hours',4)]:
    df.loc[rng.choice(n, k, replace=False), col] = np.nan
df.loc[7,'Attendance_Pct'] = 105.0          # impossible value
df.loc[[30,90],'Gender'] = ['male','FEMALE'] # inconsistent text
df = pd.concat([df, df.sample(5, random_state=1)], ignore_index=True)  # 5 duplicate rows
df.to_csv('data/raw/student_performance.csv', index=False)
print(df.shape)
