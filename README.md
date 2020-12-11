## 環境構築

### Python

1. Pythonのインストール  
※ バージョンは3.8をおすすめ
        
1. コマンドプロンプトで `python --version` と打ってPythonのバージョンが出てきたら成功、出てこなかったらたぶんPythonにパスが通ってない

1. コマンドプロンプトで以下のコマンドを実行  
```pip install -r requirements.txt```  
 ※ 「ちゃんとこの場所にPATH通しておけよ！」みたいな文章がで出てきたらおとなしく従っておく
        
### データベース構築
 
 1. コマンドプロンプトからmysqlに"root"でログインして以下のコマンドを実行  
 ``` source [本アプリのルートディレクトリのパス]/sql/create_hf21_db.sql ```

## アプリ起動方法

1. mysqlサーバーを起動

1. コマンドプロンプトで本アプリのルートディレクトリに移動

1. ルートディレクトリで以下のコマンドを実行してサーバーを立ち上げる  
 ```python app.py```

1. 以下のURLに"Chrome"でアクセス  
```http://127.0.0.1:5000/```

1. サーバーの停止方法はCtrl+C

# 以上

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
