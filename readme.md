KeepaAPIサンプル
====

公式API(商品情報取得)  
https://keepa.com/#!discuss/t/request-products/110


# 使い方
モジュールインストール（初回のみ）
```
pip install -r requirements.txt
```

.env_devファイルにKeepaAPIのkeyをセット
```
KEEPA_API_KEY = "キーをセット"
```

.env_devファイルを.envファイルにリネーム
```
.env_dev →　.env
```

サンプルプログラム実行
```
python main/crawle_keepa.py
```