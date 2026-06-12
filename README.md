# 褒めたもん (hometamon)

<img alt="hometamon" src="main/images/icon.jpg" width="150" align="middle">

[![GitHub Actions CI](https://github.com/seven320/metamon_code/actions/workflows/ci.yml/badge.svg)](https://github.com/seven320/metamon_code/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/seven320/metamon_code)](https://github.com/seven320/metamon_code/blob/master/LICENSE)

SNS を巡回し、「ばおわ」「疲れた」「退勤」などの投稿に**自動で褒め返信＋スタンプ**を付ける bot。

> **⚠️ 現在の稼働対象は mixi2 です。**
> 旧 X (Twitter) 版のコードはレガシーとして残していますが、デプロイ対象ではありません。
> X API が実質有料化したため、API 利用が無料の [mixi2 Developer Platform](https://developer.mixi.social/) へ「褒める」機能を移行しました。

---

## 何をするか（mixi2版）

専用コミュニティを cron でポーリングし、褒めトリガー語を含む投稿に反応します。

1. `GetCommunityTimeline` で新着投稿を**差分取得**（最新 post_id をカーソルとして永続化）
2. 褒めトリガー語（`ばおわ`/`疲れた`/`退勤`/`帰宅` 等）を含むかを判定
3. 定型文からランダムに選んだ褒め文で**返信**（`CreatePost`）＋**スタンプ付与**（`AddStampToPost`、旧「ファボ」相当）
4. NG ワード/NG ユーザー、自分の投稿、返信ポストは除外。bot 感対策にランダム待機・1 起動あたり返信件数上限あり
5. 実行結果を管理者へ DM レポート

**スコープ**: 今回移行したのは「褒める」機能のみ。朝/夜の挨拶・15 時のお菓子投稿・フォロー管理は旧 X 版のレガシー機能で、mixi2 には移行していません。

---

## ファイルマップ（X版 / mixi2版 / 共通）

X 版と mixi2 版が同居しているため、役割を明示します。

| 区分 | ファイル | 役割 |
|---|---|---|
| **mixi2版（現役）** | `main/src/hometamon_mixi2.py` | **エントリポイント**。巡回→分類→返信＋スタンプ→レポート |
| | `main/src/mixi2_client.py` | OAuth2 認証＋gRPC 接続ラッパ |
| | `main/src/mixi2_adapter.py` | mixi2 `Post`/`User` → 旧 tweet 風オブジェクトへ変換 |
| | `main/src/mixi2_probe.py` | 疎通確認・導入確認・スタンプ列挙（セットアップ補助） |
| | `main/src/mixi2_gen/` | proto から**自動生成**した gRPC スタブ（手で触らない） |
| | `main/proto/` | mixi2 公式 proto の vendor（生成元・[mixigroup/mixi2-api](https://github.com/mixigroup/mixi2-api)） |
| **共通** | `main/src/filters.py` | NG ワード・褒めトリガー語・返信文組み立て（両版で共用） |
| | `main/src/meta_manuscript.py` | 褒め文などの定型文リスト |
| **X版（レガシー・非デプロイ）** | `main/src/hometamon.py` | 旧エントリポイント（tweepy / X API） |
| | `main/src/tweet_intent.py`, `main/src/delete_friendship_byhand.py` | X 専用ユーティリティ |
| **共通ユーティリティ** | `main/src/make_icon.py`, `main/src/join_images.py` | 画像生成補助 |

---

## セットアップ

```bash
git clone https://github.com/seven320/metamon_code.git
cp main/env/exam.env main/env/.env   # 値を記入（mixi2の接続情報・COMMUNITY_ID・PRAISE_STAMP_ID 等）
```

`.env` に入れる値の意味は `main/env/exam.env` のコメント参照。
mixi2 側の事前準備（開発者登録・コミュニティ作成・**プラグイン導入**・資格情報の発行）が必要です。

## 実行（mixi2版）

ローカル（[uv](https://docs.astral.sh/uv/) 使用）:

```bash
cd main
uv run python -m src.mixi2_probe       # まず疎通＋導入確認＋使えるスタンプ一覧（読み取りのみ・安全）
uv run python -m src.hometamon_mixi2    # 1回実行（.env の MIXI2_DRY_RUN=1 なら投稿せずログのみ）
```

## proto の再生成

mixi2 が API を更新したら、公式 proto を取り込み直して再生成します（生成物 `main/src/mixi2_gen/` はコミット対象）:

```bash
cd main && make gen-proto      # = uv run bash scripts/gen_proto.sh
```

## テスト

```bash
cd main && uv run pytest
```

Docker 経由: `make test`

---

## about hometamon（記事）
[褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)
[褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)

## License
[MIT](LICENSE)

## Author
[seven320](https://github.com/seven320)
