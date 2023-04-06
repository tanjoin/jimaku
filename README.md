# jimaku

画像に字幕をつけます。

## 設定

```
brew install python@3.10
brew install pipenv
pipenv --python 3.10
pipenv install
```

## 実行方法

```
pipenv shell
python main.py -t こんにちは
python main.py -f res/sample/sample.txt
```

## TODO
- 自動で折り返し
- VOICEBOXのずんだもんの声を付けたムービーを生成
- キャラクターアニメーション
  - 検証スクリプト（背景画像と前景画像を用意する）
    ```
    python lib/move.py
    ```