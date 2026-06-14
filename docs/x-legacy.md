# X (Twitter) 版（レガシー）

> **これは旧バージョンです。** 現在の稼働対象は mixi2（[mixi2.md](mixi2.md)）。
> X 版コードは**削除せず残置**しているが、デプロイ対象ではない。

## 位置づけ
褒めたもんは元々 **X (Twitter) API + tweepy** で動作していた。X API が実質有料化（従量課金）し、
タイムライン全体取得のような使い方がコスト/制限的に厳しくなったため、API 利用が無料の
**mixi2 Developer Platform** へ「褒める」機能を移行した。

移行時の方針はコードを削除せず**分岐から外すだけ**としたため、X 版の実装はそのまま残っている。

## 何をしていたか
`main/src/hometamon.py` の `main()` が旧エントリポイント。Home Timeline（`api.home_timeline`）を
取得し、条件に応じて反応していた:

- **褒めリプ**（キーワードベース）← この機能だけ mixi2 へ移行
- 朝/夜の挨拶リプ（おはよう / おやすみ）
- 15 時のお菓子ツイート
- フォローバック管理
- 実行件数の DM レポート

褒め以外（挨拶・お菓子・フォロー管理）は**未移行**。mixi2 にはフォロー管理 API が無く、
他は今回スコープ外。

## 主要ファイル
| ファイル | 役割 |
|---|---|
| `main/src/hometamon.py` | 旧本体（`Hometamon` クラス、tweepy / X API v1.1 想定） |
| `main/src/tweet_intent.py` | ツイート intent 関連 |
| `main/src/delete_friendship_byhand.py` | フォロー手動整理 |

## mixi2 版との関係
- **共通化済み**: NG ワード群・褒めトリガー語・返信文の組み立て・除外判定は
  `main/src/filters.py` に抽出され、**X 版・mixi2 版の両方が利用**する。定型文も
  `main/src/meta_manuscript.py` を共用。
- そのため X 版に手を入れても mixi2 版に影響しうる共通部分があるので、変更時は両版のテスト
  （`main/tests/test_hometamon.py` と `test_hometamon_mixi2.py`）を確認すること。

## 参考（X 版時代の記事）
- [褒めたもんについて（コンセプト編）](https://denden-seven.hatenablog.com/entry/2019/01/09/131220)
- [褒めたもんについて（技術編）](https://denden-seven.hatenablog.com/entry/2019/01/09/130437)
