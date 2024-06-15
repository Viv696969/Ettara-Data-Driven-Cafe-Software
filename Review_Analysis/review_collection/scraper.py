from datetime import datetime,timedelta
from dateutil import relativedelta
from bs4 import BeautifulSoup
import requests
import mysql.connector as mysql
import pprint
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer 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"}

query = '''
        INSERT INTO sentiment_analysis (review, date, sentiment, value,id)
        VALUES (%s, %s, %s, %s,%s)
        '''

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	


# tokenizer = AutoTokenizer.from_pretrained(
#     'nlptown/bert-base-multilingual-uncased-sentiment'
#     )

# model = AutoModelForSequenceClassification.from_pretrained(
#     'nlptown/bert-base-multilingual-uncased-sentiment'
#     )

sentiment_mapping={
    1:'very negative',
    2:'negative',
    3:'neutral',
    4:'positive',
    5:'excellent'
}

def give_sentiment(text):
    # tokens = tokenizer.encode(text, return_tensors='pt')
    # result=model(tokens)
    # value=int(torch.argmax(result.logits[0]))+1
    output = int(
        query(
            {"inputs": text}
    )[0][0]['label'].split()[0]
    )
    # return {'sentiment':sentiment_mapping[output],'value':output,'status':True}
    return {'sentiment':sentiment_mapping[output],'value':output,'status':True}

def give_date(col):
    if 'yesterday' in col:
        d = datetime.today() - timedelta(days=1)
        return d.strftime("%Y-%m-%d")
    
    if 'days' in col or 'day' in col:
        day=col.split()[0]
        if day=="one" or day=="One":
            day=1
        else:
            day=int(day)
            
        d = datetime.today() - timedelta(days=day)
        return d.strftime("%Y-%m-%d")
    
def connect():
    conn=mysql.connect(
        host='myfirstrds.c5eeiea4ujq1.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='admin1234',
        database='ettara_sentiments_db'
    )
    cursor=conn.cursor()
    return conn,cursor 

def store_reviews():
    zomato_link="https://www.zomato.com/mumbai/ettarra-1-juhu/reviews"
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    r = requests.get(zomato_link, headers=headers)
    if r.status_code == 200:
        
        soup=BeautifulSoup(r.text,'html.parser')
        results=soup.select('p[class*="sc-1hez2tp-0"]')
        reviews=[]

        for number,result in enumerate(results):
            if 'time-stamp' in str(result):
                payload={
                    'date':result.text,
                    'review':results[number+1].text
                }
                reviews.append(payload)
        

        conn,cursor=connect()
        # cursor.execute(
        #     "select review,date,id from sentiment_analysis order by date desc,id desc limit 1;"
        # )
        cursor.execute("select review,id from sentiment_analysis where id = (select max(id) from sentiment_analysis);")
        latest_review=cursor.fetchone()

        latest_id=latest_review[1]
        print(latest_review,"\n")

        value_list=[]

        for review in reviews:
            if review['review']==latest_review[0]:
                break
            else:
                review_date=give_date(review['date'])
                text=review['review']
                print("came")
                data=give_sentiment(text)
                values = (text,review_date,data['sentiment'],data['value'])
                value_list.append(values)

        print(value_list,"\n")
        data_list=[]
        for data in value_list[::-1]:
            latest_id+=1
            data=data+(latest_id,)
            cursor.execute(query,data)
            conn.commit()
            # data_list.append(data+(latest_id,))

        
    else:
        print("Erorr in recieveing data")
    cursor.close()
    conn.close()


if __name__=="__main__":
    store_reviews()