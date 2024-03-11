# -*- coding: utf-8 -*-
# =============================CODE FROM BAIDU FANYI================================
# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import os
import requests
import random
import json
from hashlib import md5

# retrieve the appid/appkey from the environment variables
appid = os.environ.get('BAIDU_APP_ID')
appkey = os.environ.get('BAIDU_APP_KEY')
# appid = '20240311001989817'
# appkey = 'jzni3ki1fZtfnStLnCod'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def translate(from_lang: str='en', to_lang: str='zh', query: str=None):
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    result = _extarct_from_results(result)
    if result:
        return result
    else:
        return "No translated results is contained!"

def _extarct_from_results(results: dict, ):
    res = ''
    try:
        trans_result = results['trans_result']
    except KeyError as e:
        print("No translated results is contained!")
        return ""
    for item in trans_result:
        res += item['dst']
        res += '\n'
    return res


if __name__ == "__main__":
    result = translate(query="I like her!\nBut she does not like me.\nSAD!")
    print(result)