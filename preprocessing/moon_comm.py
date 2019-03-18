from pymongo import MongoClient
import re
from ckonlpy.tag import Twitter
import pickle
import time

def comm_date(comm_name, dates_array):
    for dates in dates_array:
        client = MongoClient('mongodb://local:port')
        db = client.mongodb
        # 컬렉션 객체 가져오기

        comm = db[comm_name]
        cursor = comm.find({'content.idate' : {'$regex': dates}}).sort([('_id', -1)])

        client.close()

        idate_with_all = []

        for record in cursor:

            reply_temp = record['content']['creplies']
            content_temp = record['content']['ccontent']
            title_temp = record['ctitle']

            if isinstance(reply_temp, list):
                idate_with_all.extend(reply_temp)
            else: 
                idate_with_all.append(reply_temp)

            if isinstance(content_temp, list):
                idate_with_all.extend(content_temp)
            else: 
                idate_with_all.append(content_temp)

            if isinstance(title_temp, list):
                idate_with_all.extend(title_temp)
            else: 
                idate_with_all.append(title_temp)


        # #%%
        # # 전처리 (필요없는 특수기호 영문 숫자 지우기)

        twitter = Twitter()

        tokened_texts = []
        for i in range(len(idate_with_all)):
            text = idate_with_all[i]

            # 전처리
            text = re.sub('[0-9A-Za-zㅋㅎㄷㅡ]+',' ',text)
            text = re.sub('[\[\]\.\!\?\/\.\:\-\>\~\@\·\"\"\%\,\(\)\&]+', ' ' , text)
            text = re.sub('[\n\xa0\r]+',' ',text)
            
            # 토큰화
            token = twitter.nouns(text)  # 명사만

            if token != []:
                tokened_texts.extend(token)

            print(dates, i, '/', len(idate_with_all))

        pickle_name = str(comm_name) + str(dates)
        with open(pickle_name,"wb") as fw:
            pickle.dump(tokened_texts, fw)
        print('저장완료')
  

#  함수 실행부 
date_array = ['2019-01-09','2019-01-10','2019-01-30','2019-02-10','2019-02-11']
comm_name = 'MPark_19'
comm_date(comm_name, date_array)

from collections import Counter
# 로딩 테스트 
for dates in date_array:
    pickle_name = str(comm_name) + str(dates)
    with open(pickle_name, 'rb') as f: 
        texts = pickle.load(f)

    wc = Counter(texts)

    print(wc.most_common(10))