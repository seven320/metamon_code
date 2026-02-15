import random
import hometamon


def delete_by_hand():
    h = hometamon.Hometamon()
    friends = h.api.friends_ids(h.my_twitter_user_id)
    random.shuffle(friends)

    friend_status_list = h.api.lookup_users(friends[:100])

    cnt = 0
    for friend_status in friend_status_list:
        if h.exclude_user(friend_status):
            print(f"ユーザー名:{friend_status.name}")
            print(f"説明欄:{friend_status.description}")
            print(f"認証: {friend_status.verified}")
            user_input = input(
                "上記ユーザーを忘れさせたいのであれば1入力してください。"
            )
            if user_input == "1":
                h.api.destroy_friendship(id=friend_status.id)
                print("忘れました")
                cnt += 1
            else:
                print("覚えています")
                pass
    print(f"{cnt}人の記憶を忘れました")


if __name__ == "__main__":
    delete_by_hand()
