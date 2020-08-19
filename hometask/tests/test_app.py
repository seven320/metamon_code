import pytest
from server import app

@pytest.fixture(scope = "function")
def db():
    db = app.ConnectDB()
    return db


def test_exist_user_with_True(db):
    user_id = "123456"
    assert db.exist_user(user_id) == True

def test_exist_user_with_False(db):
    user_id = "00000"
    assert db.exist_user(user_id) == False

def test_get_user(db):
    user_id = "123456"
    user = db.get_user(user_id)
    id, username, user_id, twitter_id, dt, secret_account = user[0]
    assert username == "電電"

def test_insert_user(db):
    username = "褒めたもん"
    user_id = "123445"
    twitter_id = "999999"
    secret_account = 0
    db.insert_user(username, user_id, twitter_id, secret_account)

    assert db.exist_user(user_id) == True
    assert db.get_user(user_id)[0][1] == username

def test_update_user(db):
    fake_username = "ゴース"
    fake_user_id ="6666"
    fake_twitter_id = "9999"
    fake_secret_account = 0
    db.insert_user(fake_username, fake_user_id, fake_twitter_id, fake_secret_account)

    update_username = "ゴースト"
    update_twitter_id = "10000"
    update_secret_account = 1
    db.update_user(update_username, fake_user_id, update_twitter_id, update_secret_account)
    id, username, user_id, twitter_id, dt, secret_account = db.get_user(fake_user_id)[0]

    assert username == update_username
    assert twitter_id == update_twitter_id
    assert secret_account == update_secret_account

def test_set_user_with_new(db):
    fake_username = "電電"
    fake_user_id ="123456765432"
    fake_twitter_id = "yosyuaomenw"
    fake_secret_account = 0
    db.set_user(fake_username, fake_user_id, fake_twitter_id, fake_secret_account)
    id, username, user_id, twitter_id, dt, secret_account = db.get_user(fake_user_id)[0]

    assert fake_username == username
    assert fake_user_id == user_id
    assert fake_twitter_id == twitter_id
    assert fake_secret_account == secret_account

def test_get_task(db):
    fake_user_id = "123456"
    fake_task = "朝早く起きる"
    tasks = db.get_tasks(fake_user_id)
    id, user_id, task, created_at = tasks[0]

    assert id == 1
    assert fake_user_id == user_id
    assert fake_task == task

def test_get_new_task(db):
    fake_user_id = "123456"
    fake_task = "本を読む"
    task = db.get_new_task(fake_user_id)

    id, user_id, task, created_at = task
    assert id == 3
    assert fake_user_id == user_id
    assert fake_task == task

def test_insert_task(db):
    fake_user_id = "123456"
    fake_task = "走る"
    db.insert_task(fake_user_id, fake_task)

    id, user_id, task, created_at = db.get_new_task(fake_user_id)
    assert fake_user_id == user_id
    assert fake_task == task

def test_get_task_history(db):
    fake_task_id = 4
    task_histories = db.get_task_history(fake_task_id)

    assert len(task_histories) == 3

    id, task_id, tweeet_id, weet_text, created_at, praised = task_histories[0]
    assert fake_task_id == task_id

def test_get_task_count(db):
    fake_task_id = 4
    task_count = db.get_task_count_by_day(fake_task_id)

    assert task_count == 1

