# metamon_code
褒めたもんを実行するためのコード

## Requirement
tweepy==3.8.0  
dotenv==0.10.3

## 使い方 How to USE

#### 1 clone this repository
~~~
git clone https://github.com/seven320/metamon_code.git
cd metamon_code
~~~
#### 2 get twitter api and input your api keys in .env like .env.exam
~~~
cd main/src/
vim .env.exam
cp .env.exam .env
~~~
#### 3 run code
~~~
python hometamon.py --deploy 0
~~~

--deploy 1にすると実際にツイートを行います

#### 4 deploy with docker(optional)
~~~
cd /metamon_code/
make restart
~~~
run hometamon.py with busybox every 8 min.

## about hometamon (記事)
[褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)  
[褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)  

## licence
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author
[seven320](https://github.com/seven320)
