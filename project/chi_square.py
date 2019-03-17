#%%
import numpy as np
import pandas as pd
from scipy import stats  # 파이썬 통계 패키지 scipy - 카이제곱검정 
import pymysql

#%%
'''
A. 범주형 자료 : 범주로만 분류될 수 있는 관측 값(수치적으로 측정되지 않는 자료)
   범주형 자료 분석 - 피어슨의 검정
   매 모집단이 두 가지 이상의 서로 다른 속성을 가지는 개체들로 나뉘는 경우에 여러 모집단을 비교하는 방법
    1)여러 범주로 분류되는 단일표본 - 적합도 검정
    2)여러 범주로 분류되는 독립표본 - 동질성 검정
    3)두 특성에 따라 동시에 분류되는 단일표본 - 독립성검정

B. 카이제곱 검정(chi-square test)
            귀무가설(H0) 두 집단 사이에 차이가 없다, 두 요인은 독립적이지 않다
            대립가설(H1) 두 집단 사이에 차이가 있다, 두 요인은 독립적이다
    사용 목적 : 기대빈도와 관찰빈도 사이에 상당한 차이가 있는지 없는지 알기 위해 사용
                주로 범주화 데이터 분석에 사용(ex.교육수준, 색깔, 성별) 

    사용법 : scipy.stats.chisquare  기대빈도 스스로 계산해야함
                참고자료) https://towardsdatascience.com/running-chi-square-tests-in-python-with-die-roll-data-b9903817c51b
            scipy.stats.chi2_contingency  기대빈도 자동으로 계산
                참고자료) https://www.kaggle.com/omarayman/chi-square-test-in-python        

'''

#%%

df = pd.read_csv('nicknames.csv')


#%%
# 교차표(cross tabulation) 생성    닉네임 -> 가로 ,  커뮤니티 -> 세로로 하는 crosstab 생성x
cnt = pd.crosstab(df["comm"],df["nick"])
print(cnt)

#%%
# 카이제곱 검정 실시
stats.chi2_contingency(cnt)


#  튜플로 나온 결과를 이해하기 쉽게 만들기
chi2_stat, p_val, dof, ex = stats.chi2_contingency(cnt)

print("===Chi2 Stat===")
print(chi2_stat)
print("\n")

print("===Degrees of Freedom===")
print(dof)
print("\n")

print("===P-Value===")
print(p_val)
print("\n")

print("===Contingency Table===")
print(ex)


