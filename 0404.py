#安裝函式庫
import tweepy  #twitter api
import time    #用於爬蟲 緩衝及計算程式所需時間
import datetime #用於檔名設計 使用當天日期+帳號名稱
import requests #用於爬蟲請求
import os #用於創建資料夾等檔案操作
from userdata import *  #引入金鑰
import concurrent.futures #多執行緒 用來加速爬蟲

#import our access keys

#環境 提供與安裝
# pip freeze > requirements.txt
# pip install -r requirements.txt

# API設定
def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # Return API with authentication:
    api = tweepy.API(auth) #parser=tweepy.parsers.JSONParser()
    return api

# 創建提取器:
extractor = twitter_setup()
# We create a tweet list as follows:
name =input("請輸入要查詢的帳號:") #shuvi0521
k=int(input("要印出幾則最新推文查看(RT代表轉推):"))
tweets = extractor.user_timeline(screen_name=name, count=k)  #用戶名  / 幾個推文
print("提取了{}則推文.".format(len(tweets)))
# 印出最近k則推文:

i=1
for tweet in tweets[:k]:
    print(str(i)+"",tweet.text)
    i=i+1

print("--------------------------查詢tweet的各種標籤-------------------------")
print(tweet)

#把推文變成Dataframe
# 資料是那些推文，欄位名稱是Tweets
print("------------------------#開始推文處理-----------------")
t1 = time.time()

# 拿第一張圖片網址
imageurl =[]
# def getimageurl():
#     for tweet in tweets:
#         media = tweet.entities.get('media')  #[{'url ':[]}]
#         if media is not None: #如果有圖片
#             for image in media:
#                 url = image['media_url']#標籤名稱
#                 if url is not None:
#                     imageurl.append(url)
#     return imageurl

# getimageurl()

#拿多張圖
# timeline = tweepy.Cursor(extractor.user_timeline, tweet_mode='extended').items()
moreimageurl =[]
def getmoreimage():
    for tweet in tweets:
        media = tweet.entities.get('media')  # [{'url ':[]}]
        if media is not None:  # 如果有圖片
            moremedia =tweet.extended_entities['media'] #額外圖片 在extended_entities裡
            if len(moremedia)==1:
                for image in media:
                    url = image['media_url']  # 標籤名稱
                    if url is not None:
                        imageurl.append(url)
                        moreimageurl.append("")
            elif len(moremedia) >1: #如果有多張圖 ?
                # print("圖片張數",len(moremedia))
                # print(moremedia)
                # print(type(moremedia[0]))
                s =''
                for i in range(0, len(moremedia)):  #
                    page =moremedia[i]['media_url'] #標籤名稱
                    # print(page) #中間測試
                    s = s + page+' '
                moreimageurl.append(s)
                imageurl.append("")
            else:
                page =''
                moreimageurl.append(page)
    return imageurl,moreimageurl

# moreimage()

# 拿原文網址
url =[]
def geturl():
    for tweet in tweets:
        media1 = tweet.entities.get('media')
        if media1 is not None: #如果有原文網址 跟圖片一樣
            for originalurl in media1:
                testurl = originalurl['expanded_url']#標籤名稱
                # print(type(testurl))
                url.append(testurl)
    return url

# geturl()

# 目標 : 把list裡的字典的值抓出來  #抓出hashtags的text       #tweet.entities.get('hashtags')        有這個 [{'text': 'みんなの初めて描いたホロメンと直近で描いたホロメンがみたい', 'indices': [20, 50]}]
finalHash = [] #存放區
def gettagtext():
    for tweet in tweets:  #tweet 是一種status 是api抓的 是json檔
        tag =tweet.entities.get('hashtags')  #這是list
        if len(tag) !=0:
            for result in tag:  #result是字典
                final = result['text']  #final是我要的 text(key) 的value(那些文字)
                # print(type(final)) #str
                finalHash.append(final)
        else:
            # print("偵測到空")
            final =''
            finalHash.append(final)
    return finalHash

t =[]
def ori():
    for tweet in tweets:
        text =tweet.text
        t.append(text)
    return t

txt =ori()
# image =getimageurl()
image,moreimage =getmoreimage()
orignal =geturl()
tagtag =gettagtext()

print("image",image)
print("more",moreimage)

t2 = time.time()
print("推文處理結束，花了:"+str(t2-t1)+"秒") #取到小點2位
print("--------------------------csv相關處理-----------------")


data=[txt,image,orignal,tagtag,moreimage]
ll=len(data[1])
with open("C://Users//PRO//Desktop//twitter//"+str(datetime.date.today())+str(name)+".csv", 'w',encoding='utf-8-sig') as f:
    s ='原文'+','+'圖片網址'+ ',' + '原文網址'+ ',' +'hashtags'+','+'多圖網址' +'\n'
    f.write(s)
    for i in range(0,ll):
        s=data[0][i]+','+data[1][i]+','+data[2][i]+','+data[3][i]+','+data[4][i]+'\n'
        f.write(s)

# makeexcel().to_csv("C://Users//PRO//Desktop//twitter//"+str(name)+".csv",encoding='utf-8-sig')
#uft-8-sig"中sig全拼為 signature 也就是"帶有簽名的utf-8”亂碼問題解決
print("-------------------------csv儲存完畢-----------------")

print("--------------------------開始下載圖片--------------------")
t3 =time.time()


splitimage =[]
def split():
    for item in moreimage:
        s = str(item).split(' ') #用空白切割
        for i in s:
            if i is not '':
                splitimage.append(i)
    return splitimage
# print(split())
moreimage =split()
imagesave =image+moreimage

while '' in imagesave:
    imagesave.remove('')

print("全部圖片網址",imagesave)
# print("有幾張單張圖片",len(image))
# print("多圖的圖片 總和",len(moreimage))
print("全部有"+str(len(imagesave))+"張圖")
def climb(i):
    header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
            }

    print(str(i) + "網址", str(imagesave[i]))
    response = requests.get(str(imagesave[i]),headers=header)

    time.sleep(10) #避免造成伺服器負擔 #3秒會擋

    print("response",response)
    print(type(response)) #檢查為200或404
        # soup = BeautifulSoup(response.text, "lxml")

    if not os.path.exists("C://Users//PRO//Desktop//twitter//" + str(datetime.date.today()) + str(name) + "images"):
        os.mkdir("C://Users//PRO//Desktop//twitter//" + str(datetime.date.today()) + str(name) + "images")  # 建立資料夾

    dirname = "C://Users//PRO//Desktop//twitter//" + str(datetime.date.today()) + str(name) + "images"+"//"+str(i + 1) + ".jpg"
    with open(dirname, "wb") as f:  # 開啟資料夾及命名圖片檔
        f.write(response.content)  # 寫入圖片的二進位碼
        f.close()

numuber =[i for i in range(len(imagesave)) ]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(climb, numuber)

t4 =time.time()
print("圖片儲存結束，花了"+str(round(t4-t3, 2))+"秒存了"+str(len(imagesave))+"張圖") #小數點2位



