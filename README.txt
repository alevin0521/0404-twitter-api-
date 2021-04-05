第一步 申請twitter api key 跟 token  https://apps.twitter.com/  點擊右上角建立app 記得登入推特帳號
第二步 填寫個人專案名稱 國家 codeing等級等資訊 下一步
第三步 填寫為何使用twitter api 將做那些應用  填yes no就好
第四步 等收信 會收到說正在處理 我半天左右收到第二封信要填寫一些 機構是否使用你的專案或應用， 你的應用的更詳細描述 NLP 等分析 或是相關按讚喜歡的統計等
第五步 收到通過通知 開始設定你的api
記得 記下
CONSUMER_KEY  =  
CONSUMER_SECRET = 

ACCESS_TOKEN  = 
ACCESS_SECRET = 
等資訊 接著就可以使用api了

接下來說明程式本身
第一步 引入相關函式庫 跟自己api的金鑰資訊 
第二步 API設定
第三步 輸入要查詢的帳號，想看幾篇推文 
第四步 tweet 裡有很多json標籤 我選擇圖片網址，多張圖的圖片網址，推文本文，轉推數等標籤
記得檢查標籤tweet.entities跟tweet.extended_entities的內容 大部分都在裡面
第五步 接著是對取得的資料處理過後存入csv裡 
第六步 下載圖片 ，由於已獲得圖片網址 ，再進行簡單的requests及header等爬蟲步驟
接著選擇圖片儲存位置
第七步 使用concurrent.futures 進行爬取圖片部分的加速
第八步 註解及時間統計 
第九步 完成
