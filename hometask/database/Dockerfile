FROM mysql:5.7

MAINTAINER denden<github: seven320>

# MySQLをrootで実行する設定に書き換える
RUN sed -e 's/^ *user *= *mysql$/user = root/' -i /etc/mysql/my.cnf