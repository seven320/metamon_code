# README
![hometamon](https://user-images.githubusercontent.com/33506506/74358523-e9594980-4e04-11ea-8130-ee86a32fef74.jpg)

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
#### 2 get twitter api and input 

input your api keys into "main/src/.env" like "main/src/exam_env"

~~~
cd main/src
cp exam_env .env
vim .env
~~~

#### 3 run code
~~~
python hometamon.py --test 1
~~~
#### 4 deploy with docker(optional)
~~~
cd /metamon_code/
make re-run
~~~
run hometamon.py with busybox every 8 min.

## about hometamon (記事)
[褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)  
[褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)  

## license
[MIT](LICENSE)

## Author
[seven320](https://github.com/seven320)
