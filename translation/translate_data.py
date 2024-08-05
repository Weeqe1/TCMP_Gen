import csv
import requests
import random
import hashlib
import time
import pypinyin

app_id = '20200507000442422'  #  App ID
secret_key = 'ML4zE75hN26JMb_dfp33'  #  Secret Key

url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

with open('data_zh-cn.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    with open('../Apriori/data/data_en-us.csv', 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for row in reader:
            translated_row = []
            for word in row:
                if word.strip() != '':
                    salt = str(random.randint(32768, 65536))
                    sign = hashlib.md5((app_id + word + salt + secret_key).encode('utf-8')).hexdigest()
                    params = {'q': word, 'from': 'zh', 'to': 'en', 'appid': app_id, 'salt': salt, 'sign': sign}
                    response = requests.get(url, params=params)
                    result = response.json()
                    if 'error_code' not in result:
                        translation = result['trans_result'][0]['dst']
                        translation = translation.strip('\ufeff')
                        pinyin_list = pypinyin.lazy_pinyin(word)
                        pinyin_str = ''.join(pinyin_list)
                        translated_word = f'{translation}({pinyin_str})'
                        print(translated_word)
                        time.sleep(1.5)
                    else:
                        translated_word = f'Translation failed({result["error_msg"]})'
                        time.sleep(1.5)

                else:
                    translated_word = ''
                translated_row.append(translated_word)
            writer.writerow(translated_row)
