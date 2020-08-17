import MySQLdb

connect = MySQLdb.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    passwd = "root",
    db = "hometask",
    charset = 'utf8'
)
cursor = connect.cursor()

"""
insert user
"""
# sql = "INSERT INTO user(username, user_id, twitter_id, secret_account) values('test_user','666666','test',0)"
# cursor.execute(sql)

# connect.commit()

# cursor.close()
# connect.close()

"""
show user
"""

# sql = "select * from user"
# cursor.execute(sql)

# for row in cursor:
#     print(row)

# class ConnectDB():
#     def __init__(self):
#         self.connect = MySQLdb.connect(
#             host = "127.0.0.1",
#             port = 3306,
#             user = "root",
#             passwd = "root",
#             db = "hometask",
#             charset = 'utf8'
#         )
#         self.cursor = self.connect.cursor()

def set_user(username, user_id, twitter_id, secret_account):
    """
    user_idが存在していなければinsert
    存在していれば無視
    """
    sql = ('insert into user (username, user_id, twitter_id, secret_account) '+ 
    'select * from (select "{}","{}", "{}", "{}") as tmp '.format(username, user_id, twitter_id, secret_account) +
    'where not exists (select user_id from user where user_id = "{}")'.format(user_id))
    cursor.execute(sql)
    connect.commit()

set_user(
    username = "褒めたもん", 
    user_id = "966247026416472064",
    twitter_id = "denden_by", 
    secret_account = 0
    )

def select_user(user_id):
    sql = (
        "SELECT * FROM user WHERE user_id = '{}'".format(user_id)
    )
    cursor.execute(sql)
    for row in cursor:
        print(row)

# select_user(user_id = "denden_by")


def set_task(user_id, task):
    # set_user()

    sql = (
        'INSERT INTO task(user_id, task) ' +
        'values ("{}", "{}")'.format(user_id, task)
    )
    cursor.execute(sql)
    connect.commit()

# set_task(
#     user_id = "966247026416472064",
#     task = "早寝早起き！！"
#     )

def set_task_history(task_id, praised):
    sql = (
        'INSERT INTO task_history(task_id, praised) ' +
        'value("{}", "{}")'.format(task_id, praised)
    )
    cursor.execute(sql)
    connect.commit()


set_task_history(
    task_id = 1,
    praised = 1
    )







