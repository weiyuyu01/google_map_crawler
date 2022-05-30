import pandas as pd
import jieba
import jieba.analyse
from collections import Counter

jieba.set_dictionary('dict.txt.big')
with open('stops.txt', 'r', encoding='utf8') as f:
    stops = f.read().split('\n') 
    
df = pd.read_csv('./google_map評論.csv')
#抓取正面評價
positive_list = []
for i in range(len(df)):
    if int(df['評分星數'][i]) >= 4 and df['評論內容'][i] != 'None':
        positive_list.append(df['評論內容'][i])

positive_seg = []
for j in positive_list:
    seg = jieba.lcut(j)
    for l in seg:
        if l not in stops:
            positive_seg.append(l)
#抓取負面評價
negative_list = []
for i in range(len(df)):
    if int(df['評分星數'][i]) <= 2 and df['評論內容'][i] != 'None':
        negative_list.append(df['評論內容'][i])

negative_seg = []
for j in negative_list:
    seg = jieba.lcut(j)
    for l in seg:
        if l not in stops:
            negative_seg.append(l)

#正面評價轉DataFrame
result = sorted(Counter(positive_seg).items(), key=lambda x:x[1], reverse=True)
df1 = pd.DataFrame((result), columns = ['key_word', 'count'])
print(df1)
#負面評價轉DataFrame
result_neg = sorted(Counter(negative_seg).items(), key=lambda x:x[1], reverse=True)
df2 = pd.DataFrame((result_neg), columns = ['key_word', 'count'])
print(df2)

#TF-IDF 找出句子關鍵字
# tags = jieba.analyse.extract_tags(str(content_list), topK=20, withWeight=True)
# for tag in tags:
#     print('word:', tag[0], 'tf-idf:', tag[1])

# 轉csv
df1.to_csv("positive_key_word.csv", encoding='utf-8-sig', index=False, mode='w',header=True)
print("正面評論.csv 寫入完成")

df2.to_csv("negative_key_word.csv", encoding='utf-8-sig', index=False, mode='w',header=True)
print("負面評論.csv 寫入完成")