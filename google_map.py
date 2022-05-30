import pandas as pd
import requests 
import json
from datetime import datetime

df = pd.read_csv('google_map_api.csv',sep=",",quotechar='"',header=None,encoding='utf-8')
df.columns=["品牌","分店","地址","api","lat","lng"]

date_list, content_list, star_list, lat_list, lng_list = [],[],[],[],[]
brand_list ,name_list ,address_list =[],[],[]

# 第1～100篇評論，共10個json
page_list = ["1i0","1i10","1i20","1i30","1i40","1i50","1i60","1i70","1i80","1i90"] 

# 已知欄位複製補齊
for idx in range(len(df["品牌"])):
    for i in range(100):
        brand_list.append(df["品牌"][idx])
        name_list.append(df["分店"][idx])
        address_list.append(df["地址"][idx])
        lat_list.append(df["lat"][idx])
        lng_list.append(df["lng"][idx])

# 只取每家餐廳所需變換的參數(1y後面數字,2y後面數字)
error_count = []
for url in df["api"]:
    link_list = url.replace("1y","").replace("2y","").split("!")[2:4]
    a = link_list[0]
    b = link_list[1]
    
    # 每家餐廳要請求10次json
    for i in range(10):
        url = f"https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=zh-TW&gl=tw&pb=!1m2!1y{a}!2y{b}!2m2!{page_list[i]}!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sLCJRYo79OPqUr7wP1uWnuAo!7e81"
        # 發送get請求
        json_text = requests.get(url).text
        # 取代掉特殊字元，這個字元是為了資訊安全而設定
        pretext = ')]}\''
        json_text = json_text.replace(pretext,'')
        # 把字串讀取成json
        soup = json.loads(json_text)
        
        # 取出包含留言的List 。
        conlist = soup[2]
        
        try:
        # 逐筆抓出 (日期(時間戳需轉換)、內容(過濾空格換行)、評分星數)
            for i in conlist:
                dt_object = str(datetime.fromtimestamp(int(str(i[57])[:10]))).split(" ")[0].replace("-","/")
                date_list.append(dt_object) 
                content = (str(i[3])).replace(" ","").replace("\n","") 
                content_list.append(content)
                star_list.append(str(i[4]))
        except:
            error_count += 1
            print(f"留言內容錯誤{error_count}")
            date_list.append("null") 
            content_list.append("null")
            star_list.append("null")
            
print("日期筆數",len(date_list))
print("留言筆數",len(content_list))
print("評星筆數",len(star_list))

# 寫入 csv
df1 = pd.DataFrame({
    '品牌': brand_list,
    '分店': name_list,
    '地址': address_list,
    'lat': lat_list,
    'lng': lng_list,
    '日期': date_list,
    '評論內容': content_list,
    '評分星數': star_list
    })
# df1.to_csv(f"{keyword}.csv",encoding='utf_8_sig', index=False)
# print(f"{keyword}.csv 寫入完成")
with open(f"google_map評論.csv", mode='a') as f:
    f.write('\n') 
df1.to_csv(f"google_map評論.csv",encoding='utf-8-sig', index=False, mode='a',header=False)
print(f"google_map評論.csv 寫入完成")

# csv 重新轉碼
df = pd.read_csv('google_map評論.csv',sep=",",quotechar='"',header=None,encoding='utf-8')
df.columns=["品牌","分店","地址","lat","lng","日期","評論內容","評分星數"]
df.to_csv(f"google_map評論.csv",encoding='utf-8-sig', index=False, mode='w',header=True)

# 寫入 json
js001 = df1.to_json(force_ascii=False)
with open(f"google_map評論.json", 'w') as f:
    f.write(js001)
