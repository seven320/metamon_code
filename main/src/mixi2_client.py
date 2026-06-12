# encoding utf-8
"""mixi2 Application API への薄い接続・認証ラッパ。

- OAuth2 client credentials grant でアクセストークンを取得・キャッシュ・更新する。
- gRPC の各呼び出しに `authorization: Bearer <token>` メタデータを付与する。
- bot が必要とする RPC だけを高レベルメソッドとして公開し、生成スタブの型を
  この層に閉じ込める（呼び出し側は protobuf を直接触らない）。

env (`/env/.env` もしくは `env/.env`):
    CLIENT_ID, CLIENT_SECRET   OAuth2 クライアント資格情報
    TOKEN_URL                  OAuth2 トークンエンドポイント
    API_ADDRESS                gRPC エンドポイント host:port（例 api.mixi.social:443）
    MIXI2_AUTH_KEY             任意。x-auth-key ヘッダに載せる値（無ければ送らない）
    MIXI2_GRPC_INSECURE        任意。"1" でTLS無し（ローカル検証用）
"""

import os
import sys
import time
from urllib.parse import quote

import grpc
import requests

# 生成スタブは絶対 import (`social.mixi...`) を使うため、生成ルートを path に通す。
_GEN_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mixi2_gen")
if _GEN_ROOT not in sys.path:
    sys.path.insert(0, _GEN_ROOT)

from social.mixi.application.service.application_api.v1 import (  # noqa: E402
    service_pb2,
    service_pb2_grpc,
)
from social.mixi.application.const.v1 import language_code_pb2  # noqa: E402


class Mixi2AuthError(RuntimeError):
    pass


class TokenProvider:
    """OAuth2 client credentials grant のトークン取得・キャッシュ。

    Go SDK と同じく資格情報は HTTP Basic（AuthStyleInHeader）で送る。
    有効期限の1分前で先回りして再取得する。
    """

    _EXPIRY_BUFFER_SEC = 60

    def __init__(self, token_url, client_id, client_secret, session=None):
        if not (token_url and client_id and client_secret):
            raise Mixi2AuthError(
                "TOKEN_URL / CLIENT_ID / CLIENT_SECRET が設定されていません"
            )
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = session or requests.Session()
        self._access_token = None
        self._expires_at = 0.0

    def _now(self):
        return time.time()

    def token(self):
        if self._access_token and self._now() < self._expires_at:
            return self._access_token
        return self._refresh()

    def _refresh(self):
        # RFC6749 §2.3.1 / Go SDK と同様、Basic認証前に id/secret を URL エンコードする
        # （CLIENT_SECRET に + / = 等が含まれると生のBasicでは invalid_client になるため）
        resp = self._session.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(quote(self.client_id, safe=""), quote(self.client_secret, safe="")),
            timeout=10,
        )
        if resp.status_code != 200:
            raise Mixi2AuthError(
                "token endpoint returned {}: {}".format(resp.status_code, resp.text)
            )
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise Mixi2AuthError("token response missing access_token")
        expires_in = float(payload.get("expires_in", 3600))
        self._access_token = token
        self._expires_at = self._now() + max(0.0, expires_in - self._EXPIRY_BUFFER_SEC)
        return token


class Mixi2Client:
    """bot が使う RPC を公開する高レベルクライアント。"""

    def __init__(
        self,
        api_address,
        token_provider,
        auth_key=None,
        insecure=False,
        channel=None,
    ):
        if not api_address:
            raise Mixi2AuthError("API_ADDRESS が設定されていません")
        self._token_provider = token_provider
        self._auth_key = auth_key
        # gRPC は host:port を要求するため、ポート未指定なら TLS 既定の 443 を補う
        if channel is None and ":" not in api_address:
            api_address = api_address + ":443"
        if channel is not None:
            self._channel = channel
        elif insecure:
            self._channel = grpc.insecure_channel(api_address)
        else:
            self._channel = grpc.secure_channel(
                api_address, grpc.ssl_channel_credentials()
            )
        self._stub = service_pb2_grpc.ApplicationServiceStub(self._channel)

    @classmethod
    def from_env(cls):
        token_provider = TokenProvider(
            token_url=os.environ.get("TOKEN_URL"),
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
        )
        return cls(
            api_address=os.environ.get("API_ADDRESS"),
            token_provider=token_provider,
            auth_key=os.environ.get("MIXI2_AUTH_KEY") or None,
            insecure=os.environ.get("MIXI2_GRPC_INSECURE") == "1",
        )

    def _metadata(self):
        md = [("authorization", "Bearer {}".format(self._token_provider.token()))]
        if self._auth_key:
            md.append(("x-auth-key", self._auth_key))
        return md

    def close(self):
        self._channel.close()

    # ---- 読み取り系 -------------------------------------------------------
    def get_community_timeline(
        self, community_id, since_cursor=None, until_cursor=None
    ):
        """コミュニティTLのポスト一覧を返す。since_cursor=最新post_idで差分取得。"""
        req = service_pb2.GetCommunityTimelineRequest(community_id=community_id)
        if since_cursor:
            req.since_cursor = since_cursor
        if until_cursor:
            req.until_cursor = until_cursor
        return list(
            self._stub.GetCommunityTimeline(req, metadata=self._metadata()).posts
        )

    def get_users(self, user_ids):
        """user_id のリストから User をバッチ取得する。"""
        if not user_ids:
            return []
        req = service_pb2.GetUsersRequest(user_id_list=list(user_ids))
        return list(self._stub.GetUsers(req, metadata=self._metadata()).users)

    def get_stamps(self, official_language=None, community_ids=None):
        """利用可能スタンプを取得（stamp_id の発見用）。"""
        req = service_pb2.GetStampsRequest()
        if official_language is not None:
            req.official_stamp_language = official_language
        if community_ids:
            req.community_ids.extend(community_ids)
        return self._stub.GetStamps(req, metadata=self._metadata())

    def get_communities_using_application(self):
        """アプリが導入済みのコミュニティ一覧（CommunityUsingApplication）を返す。"""
        communities = []
        cursor = None
        while True:
            req = service_pb2.GetCommunitiesUsingApplicationRequest()
            if cursor:
                req.cursor = cursor
            resp = self._stub.GetCommunitiesUsingApplication(
                req, metadata=self._metadata()
            )
            communities.extend(resp.communities_using_application)
            if resp.next_cursor:
                cursor = resp.next_cursor
            else:
                break
        return communities

    # ---- 書き込み系 -------------------------------------------------------
    def create_post(
        self, text, in_reply_to_post_id=None, community_id=None, media_id_list=None
    ):
        """ポスト作成（返信は in_reply_to_post_id 指定）。作成された Post を返す。"""
        req = service_pb2.CreatePostRequest(text=text)
        if in_reply_to_post_id:
            req.in_reply_to_post_id = in_reply_to_post_id
        if community_id:
            req.community_id = community_id
        if media_id_list:
            req.media_id_list.extend(media_id_list)
        return self._stub.CreatePost(req, metadata=self._metadata()).post

    def add_stamp_to_post(self, post_id, stamp_id):
        """ポストにスタンプを付与（旧ファボ相当）。更新後 Post を返す。"""
        req = service_pb2.AddStampToPostRequest(post_id=post_id, stamp_id=stamp_id)
        return self._stub.AddStampToPost(req, metadata=self._metadata()).post

    def send_direct_message(self, receiver_id, community_id, text):
        """コミュニティメンバーへDM送信（管理者レポート用）。"""
        req = service_pb2.SendDirectMessageToCommunityMemberRequest(
            receiver_id=receiver_id, community_id=community_id, text=text
        )
        return self._stub.SendDirectMessageToCommunityMember(
            req, metadata=self._metadata()
        ).message


# 言語コード enum を呼び出し側へ再公開（GetStamps 用）
LanguageCode = language_code_pb2.LanguageCode
