from fastapi import FastAPI,Request
from pandas import *
import sqlalchemy as mysql
from time import time
import environ
env=environ.Env()
environ.Env.read_env()

st=time()
sentiment_engine=mysql.create_engine(
    f"mysql+mysqlconnector://{env('UNAME')}:{env('PASSWORD')}@{env('ENDPOINT')}:3306/{env('DB')}"
    )
print(time()-st)
app=FastAPI()
sentiment_mapping={
    1:'very negative',
    2:'negative',
    3:'neutral',
    4:'positive',
    5:'excellent'
}

@app.get('/test_url')
async def test():
    return {'data':'test'}

@app.get("/sentiment_analysis")
async def monthly_sentiment_api(request:Request):

    df_monthly_review=read_sql_query(
    '''
    select month(date) as month,round(avg(value),2) as avg_value
    from sentiment_analysis
    group by month(date)
    order by month(date)
    ;
    ''',sentiment_engine
    )

    df_monthly_review['avg_sentiment']=df_monthly_review['avg_value'].apply(
        lambda x : sentiment_mapping[round(x)]
    )
    response={
            'monthly_average_sentiment':df_monthly_review[['month','avg_sentiment']].to_dict('list')
        }
    
    monthly_sentiment_count=read_sql_query('''
    select month(date) as `month`,sentiment,count(sentiment) as `monthly_count`
    from sentiment_analysis group by `month`,`sentiment`
    order by `month`;
    ''',sentiment_engine)
    data={}
    for month,month_df in monthly_sentiment_count.groupby('month'):
        data[f'{month}']=month_df.drop('month',axis=1).to_dict('list')

    response['monthly_sentiment_count']=data
    
    overall_avg_sentiment=sentiment_mapping[
        read_sql_query(
        'select round(avg(value)) as avg_sentiment from sentiment_analysis;',
        sentiment_engine
                    ).to_dict('records')[0]['avg_sentiment']
    ]
    print(overall_avg_sentiment)
    response['overall_avg_sentiment']=overall_avg_sentiment
    
    df_sentiment_count=read_sql_query(
        '''
        select sentiment,count(sentiment) as `sentiment_count`
        from sentiment_analysis
        group by sentiment
        order by `sentiment_count`;
        ''',sentiment_engine).to_dict('list')

    response['overall_sentiment_count']=df_sentiment_count

    df_yearly_review=read_sql_query(
    '''
    select year(date) as year,round(avg(value)) as avg_value
    from sentiment_analysis
    group by year(date)
    order by year(date)
    ;
    ''',sentiment_engine
    )
    df_yearly_review['avg_value']=df_yearly_review.avg_value.apply(lambda x : sentiment_mapping[x])
  

    response['yearly_average_sentiment']=  df_yearly_review.to_dict("list")

    return {
        'data':response,'status':200
    }

@app.post("/reviews")
async def show_reviews(request:Request):
    data=await request.json()

    sentiment_type=data['sentiment_type']

    reviews=read_sql_query(
        f'''
        select review from sentiment_analysis
        where sentiment = '{sentiment_type}'
        order by date desc
        limit 5;
        ''',sentiment_engine
    ).to_dict('list')['review']

    return {
        'data':reviews
    }


