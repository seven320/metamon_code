# README
## 褒めたもん
<img alt="hometamon" 
src = "main/images/icon.jpg" 
width = "150"
align = "middle">

[![GitHub Actions CI](https://github.com/seven320/metamon_code/actions/workflows/ci.yml/badge.svg)](https://github.com/seven320/metamon_code/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/seven320/metamon_code)](https://github.com/seven320/metamon_code/stargazers)


# metamon_code
褒めたもんを実行するためのコード

## Requirement
~~~
see `main/pyproject.toml` and `main/uv.lock` (installed by uv in Docker)
~~~

## How to USE(使い方)

#### 1 clone this repository
~~~
git clone https://github.com/seven320/metamon_code.git
~~~
#### 2 get twitter api and input 
input your api keys into "main/src/.env" like "main/src/exam_env"
~~~
cd hometamon/main/src
cp exam_env .env
vim .env
~~~

#### 3 run code
~~~
python hometamon.py
~~~
#### 4deploy with docker(optional)
~~~
cd hometamon/
make re-run
~~~

#### test (optional)
~~~
cd metamon_code/main
pytest
~~~

## about hometamon (記事)
[褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)  
[褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)  

## license
[MIT](LICENSE)

## Author
[seven320](https://github.com/seven320)
