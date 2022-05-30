import pandas as pd
import jieba
import jieba.analyse
from collections import Counter

jieba.set_dictionary('dict.txt.big')
with open('stops.txt', 'r', encoding='utf8') as f:
    stops = f.read().split('\n') 
    
df = pd.read_csv('./google_map評論.csv')
content = df["評論內容"]

seg_list = []
for i in content:
    seg = jieba.lcut(i)
    # print(seg)
    for j in seg:
        # print(j)
        # print(type(j))
        if j not in stops and j != "None":
            seg_list.append(j)
# print(seg_list)
result = sorted(Counter(seg_list).items(), key=lambda x:x[1], reverse=True)
df1 = pd.DataFrame((result), columns = ['key_word', 'count'])
print(df1)
df1.to_csv("key_word.csv", encoding='utf-8-sig', index=False, mode='w',header=True)
print("google_map評論.csv 寫入完成")


