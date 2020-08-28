server:
		python3 manage.py runserver 127.0.0.1:8001

migrate:
		python3 manage.py makemigrations api
		python3 manage.py migrate

		 
get/user:
		curl -X GET -H "Content-Type: application/json" \
		localhost:8001/api/users/

search/user:
		curl -X GET -H "Content-Type: application/json" \
		localhost:8001/api/search/task_historys/?user_id=1234567

# 
post/user:
		curl -X POST -H "Content-Type: application/json" \
		 -d '{"user_name": "test", "user_id": 123, "screen_name": "test", "secret_status": 0}' localhost:8001/api/users/

# return 
# {"user_name":"test","user_id":123,"screen_name":"test","created_at":"2020-08-27T17:57:39.706357","secret_status":"public"}

post/task:
		curl -X POST -H "Content-Type: application/json" \
		 -d '{"task":"プログラミング勉強", "user_id":"123"}' localhost:8001/api/tasks/

# {"id":3,"task":"プログラミング勉強","user_id":123,"created_at":"2020-08-28T14:54:42.287769"

post/task_history:
		curl -X POST -H "Content-Type: application/json" \
		 -d '{"tweet_id":"19999", "tweet_text":"起きれた", "user_id":"1234567", "task_id": 1}' localhost:8001/api/task_historys/

search/task_history:
		curl -X GET -H "Content-Type: application/json" \
		 localhost:8001/api/search/task_history/?task_id=1

new/data:
		make post/user
		make post/task
		make post/task_history
		make post/task_history
		




