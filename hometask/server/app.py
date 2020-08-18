import MySQLdb

# connect = MySQLdb.connect(
#     host = "127.0.0.1",
#     port = 3306,
#     user = "root",
#     passwd = "root",
#     db = "hometask",
#     charset = 'utf8'
# )
# cursor = connect.cursor()


class ConnectDB():
    def __init__(self, **args):
        self.args = {    
            "host":"127.0.0.1",
            "port":3306,
            "user":"root",
            "passwd":"root",
            "db":"hometask",
            "charset":'utf8'}

    def get_user(self, user_id):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("SELECT * FROM user WHERE user_id = '{}'".format(user_id))
            cur.execute(sql)
            user = cur.fetchall()
        return user

    def exist_user(self, user_id):
        user = self.get_user(user_id)
        return len(user) > 0

    def insert_user(self, username, user_id, twitter_id, secret_account):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("INSERT INTO user (username, user_id, twitter_id, secret_account)\
 VALUES ('{}', '{}', '{}', '{}')".format(username, user_id, twitter_id, secret_account))
            cur.execute(sql)
            con.commit()

    def update_user(self, username, user_id, twitter_id, secret_account):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("UPDATE user SET username = '{}', twitter_id = '{}', secret_account = '{}' \
WHERE user_id = '{}'".format(username, twitter_id, secret_account, user_id))
            cur.execute(sql)
            con.commit()

    def set_user(self, username, user_id, twitter_id, secret_account):
        if self.exist_user(user_id):
            self.update_user(username, user_id, twitter_id, secret_account)
        else:
            self.insert_user(username, user_id, twitter_id, secret_account)

    def get_tasks(self, user_id):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("SELECT * FROM task WHERE user_id = '{}'".format(user_id))
            cur.execute(sql)
            tasks = cur.fetchall()
        return tasks

    # 一番直近のタスクを表示
    def get_new_task(self, user_id):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("SELECT * FROM task WHERE user_id = '{}' ORDER BY id DESC LIMIT 1".format(user_id))
            cur.execute(sql)
            task = cur.fetchall()[0]
        return task

    def insert_task(self, user_id, task):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("INSERT INTO task (user_id, task) VALUES ('{}', '{}')".format(user_id, task))
            cur.execute(sql)
            con.commit()
    
    # def get_task_history(self, )


"""
show user
"""

# sql = "select * from user"
# cursor.execute(sql)

# for row in cursor:
#     print(row)


# def set_task(user_id, task):
#     # set_user()

#     sql = (
#         'INSERT INTO task(user_id, task) ' +
#         'values ("{}", "{}")'.format(user_id, task)
#     )
#     cursor.execute(sql)
#     connect.commit()

# # set_task(
# #     user_id = "966247026416472064",
# #     task = "早寝早起き！！"
# #     )

# def set_task_history(task_id, tweet_id, tweet_text, praised):
#     sql = (
#         'INSERT INTO task_history(task_id, tweet_id, tweet_text, praised) ' +
#         'value("{}", "{}", "{}", "{}")'.format(task_id, tweet_id, tweet_text, praised)
#     )
#     cursor.execute(sql)
#     connect.commit()

# # set_task_history(
# #     task_id = 1,
# #     tweet_id = 123456786543,
# #     tweet_text = '#hometask 今日も頑張ったぞ',
# #     praised = 1
# #     )

# args = {    
#     "host":"127.0.0.1",
#     "port":3306,
#     "user":"root",
#     "passwd":"root",
#     "db":"hometask",
#     "charset":'utf8'}


# with MySQLdb.connect(**args) as con:
#     print("hoge")
#     sql = "INSERT INTO user (username, user_id, twitter_id, secret_account) VALUES ('{}', '{}', '{}', '{}')".format("hoddgddde", "12dddddddd34", "1234111", "0")
#     print(sql)
#     con.cursor().execute(sql)
#     con.cursor().execute(sql)
#     con.commit()




