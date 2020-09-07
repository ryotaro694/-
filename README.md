# 校正スコア判定・文章校正
Djangoを使って校正スコア判定・文章校正アプリを構築

## 開発環境 
- django-3.1.1
- Python 2.7.16

## API
- A3RT（リクルート社）　Proofreading API                    
https://a3rt.recruit-tech.co.jp/product/demo/proofreadingAPI_demo2/typo_detect.html

- 校正支援　（Yahoo!JAPAN デベロッパー支援）                
https://developer.yahoo.co.jp/webapi/jlp/kousei/v1/kousei.html

注意）それぞれAPI取得のための登録が必要です。

## 機能
### ログイン機能

ログイン機能はこの記事を参考にしました。（ログイン機能はこのアプリのメインではないので割愛します。）
参照：https://mizzsugar.hatenablog.com/entry/2018/06/28/215117

きちんとログイン機能を果たせていないので、後にリニューアル予定します。（ログインページのみログイン機能が機能します。）

### 校正スコア判定

この機能は、入力された文章に対して、文章のスコアを判定するものです。
APIの機能として、入力文章に対する単語それぞれに一定のスコアの値を返すので、
そのスコアの平均値を取ったものをスコアとして出力します。
（0に近いほどもっともらしい文章、1に近づくほど完成度が怪しい文章という解釈です。）

また、「感度」を指定することもでき、「high」「medium」「low」から選択することができます。


```
class Kousei:
  def __init__(self):
      self.API = "https://api.a3rt.recruit-tech.co.jp/proofreading/v2/typo"
      self.apikey = "　"'
```

self.apikey に A3RTで登録したAPI keyを使ってください。

```
      if data["status"] == 0:
         messages = "GOOD"
            texts= data['checkedSentence']
            scores= '0'
            return messages,texts,scores
            
        elif data["status"] == 1:
            data_alerts = [d.get('score') for d in data["alerts"]]#内包リストで誤字抽出のScoreを導出
            scores = sum(data_alerts) / len(data_alerts) #Scoreの平均値を算出
            if scores >= 0.5:
                messages = "NG"
                texts= data['checkedSentence']
                scores = scores
                return messages,texts,scores

            elif scores < 0.5:
                messages = "OK"
                texts= data['checkedSentence']
                scores = scores
                return messages,texts,scores
```
結果出力された値は、

- 0→Good
- 0.5以下→OK
- 0.5-1.0→NG

とそれぞれメッセージを返します。

### 文章校正

この機能は、入力された文章に対して、文章の誤字脱字、表現ミスなど校正を行なってくれる機能です。
今回は、「該当箇所」「スタート位置」「指摘箇所」「指摘情報」を出力するようになっています。

また、「フィルター」の設定がマストとなっており、
「1：表記、表現ミス」「2:わかりやすい表記」「3:文章の精度UP」の3つのフィルターがあります。

> 1: 表記・表現の間違いや不適切な表現に関する指摘
>　 －誤変換、誤用、使用注意語、不快語（使用不適切な語や隠語など）、
>　 機種依存文字または拡張文字、外国地名、固有名詞、人名、ら抜き言
>   葉 が指摘されます。
>
> 2: わかりやすい表記にするための指摘
>   －当て字、表外漢字、用字（※） が指摘されます。
>　 ※日本新聞協会「新聞用語集」、共同通信社「記者ハンドブック」を
>   主な参考としています。
>
> 3: 文章をよりよくするための指摘
>　 －用語言い換え、二重否定、助詞不足の可能性あり、冗長表現、
>　 略語 が指摘されます。
>    無指定の場合は、すべての指摘を返します。

引用：https://developer.yahoo.co.jp/webapi/jlp/kousei/v1/kousei.html

```
class Sentence:
    def yahoo_api(self,text,filter_group):
        # Yahoo! JAPAN テキスト解析WebAPI　校正ツールのURL
        url = 'https://jlp.yahooapis.jp/KouseiService/V1/kousei'
        # アプリケーションID
        appid = ''
        # 変換する文字列の文字コード変換
        sentence = parse.quote(text.encode('utf-8'))
        # URLを構成
        target = "%s?appid=%s&sentence=%s&filter_group=%s" % (url, appid, sentence, filter_group)
        # 返り値を取得
        response = request.urlopen(target).read()
        return response
```
appid に 校正支援（Yahoo!）で登録したAPIIDを使ってください。
