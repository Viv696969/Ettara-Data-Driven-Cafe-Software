import mysql.connector as mysql
from apyori import apriori
import pandas as pd

def connect():
    conn=mysql.connect(
        host='',
        user='',
        password='',
        database=''
    )
    cursor=conn.cursor()
    return conn,cursor

def inspect(results):
    rules = []
    for result in results:
        for ordered_stat in result.ordered_statistics:
            rules.append({
                'items_base': tuple(ordered_stat.items_base),
                'items_add': tuple(ordered_stat.items_add),
                'support': result.support,
                'confidence': ordered_stat.confidence,
                'lift': ordered_stat.lift
            })
    return pd.DataFrame(rules)

def analysis():
    conn,cursor=connect()
    query='''
    select basket_string from shop_marketbasket;
    '''
    cursor.execute(query)
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    df=pd.DataFrame(data,columns=['text'])
    df=df.text.str.split(',',expand=True)
    df.replace({None:""},inplace=True)
    results = list(apriori(df.values))
    rules_df = inspect(results)
    top_rules = rules_df.sort_values(by='confidence', ascending=False).head(10)
    data=[]
    for index, rule in top_rules.iterrows():
        if '' in rule['items_add'] and len(rule['items_add'])==1:
            continue
        data.append({
            'if_items':list(rule['items_base']) ,
            'then_items':list(rule['items_add']),
            'confidence':str(rule['confidence'])
        })
    return data