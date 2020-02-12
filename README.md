# metamon_code
褒めたもんを実行するためのコード

## Requirement
tweepy==3.8.0  
dotenv==0.10.3

## How to USE

#### 1 このレポジトリをコピーしてください. clone this repository
~~~
git clone github.com/seven320/metamon_code
cd metamon_code
~~~
#### 2 ツイッターのapiを取得し，/metamoncode/main/src/.envに入力してください．この時，通知を送るアカウントの情報も書いてください．get twitter api and input your api keys in .env like .env.exam
~~~
cd main/src/
vim .env.exam
cp .env.exam .env
~~~
#### 3 テストコードの実行　run code
~~~
python hometamon.py --deploy 0
~~~

--deploy 1にすると実際にツイートを行います

追加機能(optional)
####　3.1 docker の起動と時間ごとに自動実行
~~~
cd /metamon_code/
make restart
~~~

## about hometamon (記事)
[褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)  
[褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)  

## licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[seven320](https://github.com/seven320)
