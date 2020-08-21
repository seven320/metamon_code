import MySQLdb

class ConnectDB():
    def __init__(self, **args):
        self.args = {    
            "host":"127.0.0.1",
            "port":3306,
            "user":"root",
            "passwd":"root",
            "db":"hometask",
            "charset":'utf8'}

    # api
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

    # POST 
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
    
    def get_task_history(self, task_id):
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("SELECT * FROM task_history WHERE task_id = '{}'".format(task_id))
            cur.execute(sql)
            task_histories = cur.fetchall()

        return task_histories

    def get_task_count_by_day(self, task_id):
        """
        get_task_count_by_day(self_id)
        """
        with MySQLdb.connect(**self.args) as con:
            cur = con.cursor()
            sql = ("SELECT date_format(created_at,'%Y%m%d'),count(*) \
FROM task_history where task_id = '{}' GROUP BY date_format(created_at,'%Y%m%d')".format(task_id))
            cur.execute(sql)
            task_histories_by_day = cur.fetchall()
            task_count = len(task_histories_by_day)

        # return task_histories_by_day
        return task_count