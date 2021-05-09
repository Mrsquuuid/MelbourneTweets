import requests
import json
import pandas as pd

# test combine aurin data with view
def test():
    url = "http://admin:8185050@127.0.0.1:5984/twitter%2Fhist%2Fsydney%2Frelative/_design/designs/_view/sa2_sentiment?group=true"
    res = requests.get(url)
    json_text = json.loads(res.text)
    view_df = pd.DataFrame.from_dict(json_text['rows'], orient="columns")
    view_df.columns = ['sa2_main16','afinn']
    aurin_df = pd.read_csv('syd_data.csv', dtype=str, header=0, encoding='ascii', engine='python')
    merged_df = pd.merge(aurin_df, view_df,on='sa2_main16')
    jdata = merged_df.to_json(orient='records', force_ascii=False)
    return json.loads(jdata)


def get_s1_data():
    url = "http://admin:12345@47.91.45.223:5984/twitter%2Ftest%2Frelative/_design/scenario_1/_view/china_covid_stats?group=true"
    res = requests.get(url)
    json_text = json.loads(res.text)
    date,total,avg,count = [],[],[],[]
    for data in json_text['rows']:
        date.append(data['key'][0]+'-'+str(data['key'][1]))
        total.append(data['value']['sum'])
        avg.append(data['value']['avg'])
        count.append(data['value']['count'])
    return {"date": date, "total": total, "avg": avg, "count": count}

