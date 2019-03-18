# #%%
import pandas as pd
import numpy as np
import pickle

## Load pickle
with open("T_0130.pickle","rb") as fr:
    text_list = pickle.load(fr)



#%%
# stopwords
stopwords = ['합니다','겁니다','그리고','갑니다','있습니다','리플수정', '거예요', '한다는', '보다는','못한다고'\
   ,'하는', '이런', '그런', '이건','놨는데']
filtered = []
filtered = [w for w in text_list if w not in stopwords]



# 단어 카운팅
from collections import Counter


wc = Counter(filtered)



word_list= []
freq_list = []
for word, freq in wc.most_common(200000):  
    if len(word) >=2 :
        #print(word, freq)
        word_list.append(word)
        freq_list.append(freq)
    # word_list.append(word)
    # freq_list.append(freq)


result = pd.DataFrame(word_list, columns=['word'])
result['freq'] = freq_list


# zscore 칼럼 추가
from scipy import stats


result['zscore'] = stats.zscore(result.freq)


print(result)

result.to_csv('M_0130.csv',index=None)


#%%
result.tail()




