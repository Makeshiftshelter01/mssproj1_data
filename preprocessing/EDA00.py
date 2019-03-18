import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 좋은 별명 목록
good_nicks = ['젠틀재인','문바마', '문깨끗','파파미','왕수석',
'negotiator','달님','문프','명왕','재인리','금괴왕','문통']

# 부정적 별명 목록
bad_nicks = ['문재앙','문죄앙','슈퍼문재앙','MC재앙','문제인','문제인간', '문죄인','문죄악', '문근혜',
'문구라', '문벌구','문적문', '문찐따', '문재인조', '쇼통령', '곡재인', '쩝쩝이', '문쩝쩝', '문산군', '문독재', '독재인',
'독재앙', '문야동', '귀걸이 아빠', '문치매', '문베스', '문두로', '문진핑', '문석탄', '문재인버스',
'문페미', '문메갈', '미세문지', '문세먼지', '먼지앙', '먼재앙', '느그 달', '느그 달님', '느그 이니', '느그 문통', '느그 문프', '느그 재인','문제아','부엉이', '노무현의 그림자']

# 중립 별명
neutral_nicks = ['문재인']

# 모든 별명을 담을 리스트
allnicks = []

# extend를 통해서 모든 리스트를 하나의 리스트로 합침
allnicks.extend(good_nicks)
allnicks.extend(bad_nicks)
allnicks.extend(neutral_nicks)



# mysql 연결객체 생성
# conn = pymysql.connect(host='HOSTNAME', user='http', password='PASSWORD', db='DBNAME', charset='utf8')

# # mysql 접속 후 커서 얻어옴
# curs = conn.cursor()

# # DB NICKNAMES 테이블 -> 데이터프레임으로
# df = pd.read_sql('select * from NICKNAMES' , con = conn)

# # 판다스형 데이트타임으로 변경
# df['idate'] = pd.to_datetime(df['idate'])

# conn.close()

# df.to_csv('nicknames1.csv', index=False)


df = pd.read_csv('nicknames1.csv')
df['idate'] = pd.to_datetime(df['idate'])


# 원하는 커뮤니티의 날짜 별 별명 빈도 표를 리턴하는 함수
def nick_counts_for_community(comm_name):

    # 해당 커뮤니티만 포함하는 df 생성
    comm_df = df[df.comm == comm_name]


    # 날짜를 담을 리스트 생성
    comm_dates = []


    # comm_df 를 통한 반복문
    for i in range(len(comm_df)):
        if comm_df.iloc[i,2] not in comm_dates: # 모든 날짜를 담을 리스트 안에 해당 날짜가 없다면
            comm_dates.append(comm_df.iloc[i,2]) # 추가
    # comm_dates 안에는 unique value만 있게 됨


    # 날짜별 별명 카운트를 위한 df 생성 준비
    idates = [] # 날짜 column
    nicks = []  # 닉네임 column
    values = [] # count column
    sent = []  # 긍부정 column

    for i in range(len(comm_dates)):  # 유니크한 날짜만 담았던 날짜를 반복하면서
        for j in range(len(allnicks)): # 날짜마다 별명도 반복
            idates.append(comm_dates[i]) # 날짜 컬럼에는 유니크한 날짜를 담고(한 날짜를 여러번)
            nicks.append(allnicks[j])    # 닉네임 컬럼에는 모든 닉네임을 담고
            sent.append(0)
            values.append(0)             # 카운트는 일단 한번도 안했으니 모두 0으로 추가

    for_new_df = {
        'idate' : idates,
        'nick' : nicks,
        'count' : values,
        'sent' : sent
    } # 사전으로 만든 뒤
    # 데이터 프레임화 (모든 날짜 + 모든 별명 + 모든 카운트는 0)
    comm_freq_df = pd.DataFrame(for_new_df)


    fre = df[df.comm == comm_name].groupby(['idate','nick'], as_index=False).count()

    for i in range(len(fre)):
        comm_freq_df.loc[(comm_freq_df.idate == fre.iloc[i, 0]) & (comm_freq_df.nick == fre.iloc[i, 1]), 'count'] = fre.iloc[i, 2]


        # 카운트 데이터 프레임에 해당하는 날짜와 별명을 가졌을 때 미리 카운트해놓은 value를 대입한다. 


    # 현재 날짜 순서가 거꾸로 되어있으니 날짜와 별명 순으로 정렬
    comm_freq_df.sort_values(by = ['idate','sent','nick'], inplace=True)

    #print(comm_freq_df)


    # for i in range(len(comm_freq_df)):
    #     print(comm_freq_df.iloc[i,1])


    # # 긍부정 나타내는 sent 칼럼에 value 넣기
    for i in range(len(comm_freq_df['nick'])):
        if comm_freq_df.iloc[i,1] in bad_nicks:
            comm_freq_df.iloc[i,3] = -1
            
        else:
            comm_freq_df.iloc[i,3] = 1

    # 그래프를 그릴 때 쉽게 하기 위해 index도 날짜와 동일하게 만듦
    comm_freq_df.set_index('idate', inplace=True)
    return comm_freq_df


ilbe = nick_counts_for_community('ilbe')


ilbe.to_csv('ilbe.csv')



# 5번 이상 언급한 경우만 가져오는 함수



def over5(self):

    # 함수 실행--------------------------------------------------------------------------
    if __name__ == '__main__':
        comm_df = nick_counts_for_community(self)
    #----------------------------------------------------------------------------------
    case = []
    for i in range(len(comm_df)):
        if comm_df.iloc[i,2] >5 :
            case.append(list(comm_df.iloc[i,]))


    df = pd.DataFrame(case, columns=['idate','nick','count'])     
    return(df)

# mpark = over5('mpark')

# print(mpark)



# 키워드 뽑아서 time series 그래프 그리는 함수

def serise(comm_name,nick,nick2,nick3):
    df = over5(comm_name)
    #print(df)
    keyword_df = df[df.nick == nick]
    keyword2_df = df[df.nick == nick2]
    keyword3_df = df[df.nick == nick3]
    #keyword3_df(df.nick)


    plt.plot(keyword_df.iloc[:,0], keyword_df.iloc[:,2], 'g-', label = 1)
    plt.plot(keyword2_df.iloc[:,0], keyword2_df.iloc[:,2], 'r--', label = 2)
    plt.plot(keyword3_df.iloc[:,0], keyword3_df.iloc[:,2], 'y-', label = 3)


    plt.title(comm_name)
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()

#serise('mpark','문재앙', '문프','문통')



# 사이트 별 키워드 빈도수 나타내는  dataframe 생성 함수
def nick_count(self):
    df = over5(self)
    df = df.groupby(['nick'], as_index=False).count()

    case = []
    for i in range(len(df)):   
        case.append(list(df.iloc[i,0:2]))
        newdf = pd.DataFrame(case, columns=['nick','count'])     
        # 큰 빈도수 별로 내림차순 정렬
        newdf.sort_values(by = 'count', ascending= False, inplace= True)
    return newdf

# mpark =nick_count('mpark')
# print(mpark)

# 사이트 별 키워드 빈도수 나타내는 막대 그래프 생성 함수
def bar(comm_name):
    df =nick_count(comm_name)
    
    # 한글을 지원하기 않기 때문에 닉네임 숫자로 범주화
    colums = df.nick
    mapping = {}
    for i in range(len(colums)):
        mapping[colums[i]] = i
#     #city=['Delhi','Beijing','Washington','Tokyo','Moscow']
#     pos = list(newdf.nick)
#     print(type(newdf.cnt))
#     Happiness_Index=list(newdf.cnt)
    
    
#     plt.barh(pos,Happiness_Index,color='blue',edgecolor='black')
#     #plt.yticks(pos, city)
#     plt.xlabel('cnt', fontsize=16)
#     plt.ylabel('nick', fontsize=16)
#     #plt.title('Barchart - Happiness index across cities',fontsize=20)
#     plt.show()

    print(mapping)
    df.nick = df.nick.map(mapping)

    case = []
    for j in range(len(df)):   
        case.append(list(df.iloc[j,0:2]))
        newdf = pd.DataFrame(case, columns=['nick','cnt'])     
        # 큰 빈도수 별로 내림차순 정렬
        newdf.sort_values(by = 'cnt', ascending= False, inplace= True)
        newdf = newdf.head(n=7)
        # nick칼럼의 모든 데이터를 apply함수를 통해 전부 str 으로 변경
        newdf['nick'] = newdf.nick.apply(str)
    print(type(newdf.nick))
    print(newdf)
   

    pos = list(newdf.nick)
    Happiness_Index=list(newdf.cnt)
    
    
    plt.barh(pos,Happiness_Index,color='black',edgecolor='black')
    plt.xlabel('cnt', fontsize=16)
    plt.ylabel('nick', fontsize=16)
    plt.title('top 7 in the frequency of nickname',fontsize=20)
    plt.show()

#bar('cook')