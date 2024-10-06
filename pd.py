import pandas as pd
import numpy as np
from collections import Counter
df=pd.read_csv("sample.csv")
temp= list(df.columns)
df=df = df.T.reset_index(drop=True).T
df1 = pd.concat([pd.DataFrame(data=[temp]),df],ignore_index=True)
stat=[]
for i in range(0,df1.shape[1]):
    stat.append( df[i].lt(0).idxmax())

array=np.array(stat)
ctr=Counter(array)
first_most_common_value, its_frequency1 = ctr.most_common(1)[0]
second_most_common_value, its_frequency2 = ctr.most_common(2)[1]
third_most_common_value, its_frequency3 = ctr.most_common(3)[2]
print(third_most_common_value, its_frequency3)
