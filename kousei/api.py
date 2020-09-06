import json
import requests
import urllib.request
import urllib.parse
from .forms import KouseiForm,SentenceForm
from urllib import request, parse

class Kousei:
    def __init__(self):
        self.API = "https://api.a3rt.recruit-tech.co.jp/proofreading/v2/typo"
        self.apikey = "DZZAg1fME6TJIa8GJAjU9JMulPVG3dsP"
    
    def get(self,request):
        url = self.apikey
        quoted_text = request.POST['bunsyo']
        sensitivity = request.POST['sensivity']
        values = {
            'apikey': url,
            'sentence': quoted_text,
            'sensitivity':sensitivity,
        }

        # パラメータをURLエンコードする
        params1 = urllib.parse.urlencode(values)
        # リクエスト用のURLを生成
        url = "https://api.a3rt.recruit-tech.co.jp/proofreading/v2/typo" + "?" + params1
 
        #リクエストを投げて結果を取得
        r = requests.get(url)
        #辞書型に変換←これめちゃくちゃ大事
        data = json.loads(r.text)
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

class Sentence:
    def yahoo_api(self,text,filter_group):
        # Yahoo! JAPAN テキスト解析WebAPI　校正ツールのURL
        url = 'https://jlp.yahooapis.jp/KouseiService/V1/kousei'
        # アプリケーションID
        appid = 'dj00aiZpPVRjeDZ0U1NYWHJ5TiZzPWNvbnN1bWVyc2VjcmV0Jng9YWM-'
        # 変換する文字列の文字コード変換
        sentence = parse.quote(text.encode('utf-8'))
        # URLを構成
        target = "%s?appid=%s&sentence=%s&filter_group=%s" % (url, appid, sentence, filter_group)
        # 返り値を取得
        response = request.urlopen(target).read()
        return response

    def get(self,request):
        filter_group = request.POST['filter_group']
        target = request.POST['sentence']
        api = self.yahoo_api(target,filter_group)
        api_decode = api.decode('utf-8')
        api_decode = api_decode.split('\n')
        
        lists = []
        for shiteki_word in api_decode:
            if '<Surface>' in shiteki_word:
                lists.append(shiteki_word.replace('<Surface>','').replace('</Surface>',''))
            elif '<StartPos>' in shiteki_word:
                lists.append(shiteki_word.replace('<StartPos>','').replace('</StartPos>',''))
            elif '<ShitekiWord/>' in shiteki_word:
                lists.append(shiteki_word.replace('<ShitekiWord>',' ').replace('<ShitekiWord/>','\t'))
            elif '<ShitekiInfo>' in shiteki_word:
                lists.append(shiteki_word.replace('<ShitekiInfo>','').replace('</ShitekiInfo>',''))
        lists1 = [lists[idx:idx + 4] for idx in range(0,len(lists), 4)]
        return lists1