import requests
import json
import pandas as pd


# helper method for s1 ab
def date_view_to_json(url):
    res = requests.get(url)
    json_text = json.loads(res.text)
    date,total,avg,count = [],[],[],[]
    for data in json_text['rows']:
        date.append(data['key'][0]+'-'+str(data['key'][1]))
        total.append(data['value']['sum'])
        avg.append(data['value']['avg'])
        count.append(data['value']['count'])
    return {"date": date, "total": total, "avg": avg, "count": count}


# return china stats, china covid stats, china vulgar stats, new cases stats
def get_s1_ab_data():
    china_url = "http://admin:admin@172.26.133.54:5984/sydney-relative/_design/scenario_1/_view/china_stats?group=true"
    china_covid_url = "http://admin:admin@172.26.133.54:5984/sydney-relative/_design/scenario_1/_view/china_covid_stats?group=true"
    china_vulgar_url = "http://admin:admin@172.26.133.54:5984/sydney-relative/_design/scenario_1/_view/china_vulgar_stats?group=true"
    china_json = date_view_to_json(china_url)
    china_covid_json = date_view_to_json(china_covid_url)
    china_vulgar_json = date_view_to_json(china_vulgar_url)
    # global out_df
    out_df = pd.read_csv('out.csv', dtype=str, header=0, encoding='ascii', engine='python')
    out_df['date'] = '20' + out_df['Year'] + '-' + out_df['Month']
    out_df = out_df.drop(['Month', 'Year'],axis=1)
    new_case_json = {'date': out_df['date'].tolist(), 'new_cases': out_df['New cases / day'].tolist()}
    return {"china_stats":china_json, "china_covid_stats":china_covid_json, "china_vulgar_stats":china_vulgar_json, "new_cases_stats":new_case_json}


# helper method for s1 cd
def clean_up(result):
    suburb,total,avg,count = [],[],[],[]
    for data in result:
        suburb.append(data['key'][0])
        total.append(data['value']['sum'])
        avg.append(data['value']['avg'])
        count.append(data['value']['count'])
    return({"suburb": suburb, "total": total, "avg": avg, "count": count})


# return the top 5 and last 5 suburb stats based on the avg of china tweets (except those have count = 1)
def get_s1_c_data():
    china_url = "http://admin:admin@172.26.133.54:5984/sydney-geo/_design/scenario_1/_view/china_stats?group=true"
    res = requests.get(china_url)
    json_text = json.loads(res.text)
    temp = json_text['rows'][1:]
    temp.sort(key = lambda x:x['value']['avg'], reverse=True)
    useful = []
    for t in temp:
        if t['value']['count'] != 1:
            useful.append(t)
    if len(useful) < 10:
        result = clean_up(useful)
    else:
        result = clean_up(useful[:5] + useful[-5:])
    return result


# return the top 10 suburb stats that have greatest count of china tweets (except those have count = 1)
def get_s1_d_data():
    china_url = "http://admin:admin@172.26.133.54:5984/sydney-geo/_design/scenario_1/_view/china_stats?group=true"
    res = requests.get(china_url)
    json_text = json.loads(res.text)
    temp = json_text['rows'][1:]
    temp.sort(key = lambda x:x['value']['count'], reverse=True)
    useful = []
    for t in temp:
        if t['value']['count'] != 1:
            useful.append(t)
    if len(useful) < 10:
        result = clean_up(useful)
    else:
        result = clean_up(useful[:10])
    return result


# return the avg china stats along with aurin economic & population stats
def get_s1_ef_data():
    # global out_aurin_df
    out_aurin_df = pd.read_csv('out_aurin.csv', dtype=str, header=0, encoding='ascii', engine='python')
    out_aurin_df = out_aurin_df.fillna(0)
    s1_df = pd.DataFrame(out_aurin_df, columns=['sa2_maincode_2016', 'mean_income_1e', 'speak_chinese_total_1f'])
    china_url = "http://admin:admin@172.26.133.54:5984/sydney-geo/_design/scenario_1/_view/china_stats?group=true"
    res = requests.get(china_url)
    json_text = json.loads(res.text)
    view_df = pd.DataFrame.from_dict(json_text['rows'][1:], orient="columns")
    view_df['sa2_name_2016'] = view_df['key'].map(lambda x : x[0])
    view_df['sa2_maincode_2016'] = view_df['key'].map(lambda x : x[1])
    view_df['avg'] = view_df['value'].map(lambda x : x['avg'])
    merged_df = pd.merge(s1_df, view_df, on='sa2_maincode_2016')
    result = {'suburb': merged_df['sa2_name_2016'].tolist(), 'avg': merged_df['avg'].tolist(), 'mean_income': merged_df['mean_income_1e'].tolist(), 'speak_chinese_total': merged_df['speak_chinese_total_1f'].tolist()}
    return result


# return the top 10 suburb stats that have greatest avg of bad word tweets (except those have count = 1)
def get_s2_a_data():
    badword_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/bad_words_stats?group=true"
    res = requests.get(badword_url)
    json_text = json.loads(res.text)
    temp = json_text['rows'][1:]
    temp.sort(key = lambda x:x['value']['avg'], reverse=True)
    useful = []
    for t in temp:
        if t['value']['count'] != 1:
            useful.append(t)
    if len(useful) < 10:
        result = clean_up(useful)
    else:
        result = clean_up(useful[:10])
    return result


# return the top 10 suburb stats that have greatest count of bad word tweets (except those have count = 1)
def get_s2_b_data():
    badword_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/bad_words_stats?group=true"
    res = requests.get(badword_url)
    json_text = json.loads(res.text)
    temp = json_text['rows'][1:]
    temp.sort(key = lambda x:x['value']['count'], reverse=True)
    useful = []
    for t in temp:
        if t['value']['count'] != 1:
            useful.append(t)
    if len(useful) < 10:
        result = clean_up(useful)
    else:
        result = clean_up(useful[:10])
    return result


# return the last 10 suburb stats based on the avg of afinn sentiment
def get_s2_c_data():
    afinn_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/afinn_stats?group=true"
    res = requests.get(afinn_url)
    json_text = json.loads(res.text)
    temp = json_text['rows'][1:]
    temp.sort(key = lambda x:x['value']['avg']) # 后十位
    useful = []
    for t in temp:
        if t['value']['count'] != 1:
            useful.append(t)
    if len(useful) < 10:
        result = clean_up(useful)
    else:
        result = clean_up(useful[:10])
    return result


# return the suburb stats, avg bad words stats VS avg afinn stats
def get_s2_d_data():
    badword_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/bad_words_stats?group=true"
    res = requests.get(badword_url)
    json_text = json.loads(res.text)
    afinn_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/afinn_stats?group=true"
    afinn_res = requests.get(afinn_url)
    afinn_json_text = json.loads(afinn_res.text)
    badword_df = pd.DataFrame.from_dict(json_text['rows'][1:], orient="columns")
    afinn_df = pd.DataFrame.from_dict(afinn_json_text['rows'][1:], orient="columns")
    afinn_df['suburb'] = afinn_df['key'].map(lambda x : x[0])
    afinn_df['code'] = afinn_df['key'].map(lambda x : x[1])
    afinn_df['afinn_avg'] = afinn_df['value'].map(lambda x : x['avg'])
    afinn_df = afinn_df.drop(['key', 'value'],axis=1)
    badword_df['code'] = badword_df['key'].map(lambda x : x[1])
    badword_df['bad_words_avg'] = badword_df['value'].map(lambda x : x['avg'])
    badword_df = badword_df.drop(['key', 'value'],axis=1)
    merged_df = pd.merge(afinn_df, badword_df, on='code')
    result = {'suburb':merged_df['suburb'].tolist(), 'afinn_avg':merged_df['afinn_avg'].tolist(), 'bad_words_avg':merged_df['bad_words_avg'].tolist()}
    return result


# return the avg badword stats along with aurin economic & population stats
def get_s2_ef_data():
    out_aurin_df = pd.read_csv('out_aurin.csv', dtype=str, header=0, encoding='ascii', engine='python')
    out_aurin_df = out_aurin_df.fillna(0)
    s2_df = pd.DataFrame(out_aurin_df, columns=['sa2_maincode_2016', 'gini_index_2e', 'unemployment_rate_2f'])
    badword_url = "http://admin:admin@172.26.133.54:5984/melbourne-geo/_design/scenario_2/_view/bad_words_stats?group=true"
    res = requests.get(badword_url)
    json_text = json.loads(res.text)
    view_df = pd.DataFrame.from_dict(json_text['rows'][1:], orient="columns")
    view_df['sa2_name_2016'] = view_df['key'].map(lambda x : x[0])
    view_df['sa2_maincode_2016'] = view_df['key'].map(lambda x : x[1])
    view_df['avg'] = view_df['value'].map(lambda x : x['avg'])
    merged_df = pd.merge(s2_df, view_df, on='sa2_maincode_2016')
    result = {'suburb': merged_df['sa2_name_2016'].tolist(), 'avg': merged_df['avg'].tolist(), 'gini_index': merged_df['gini_index_2e'].tolist(), 'unemployment_rate': merged_df['unemployment_rate_2f'].tolist()}
    return result


# return the avg nonenglish stats of 6 main cities, sorted by avg
def get_s3_a_data():
    nonenglish_url = "http://admin:admin@172.26.133.54:5984/all/_design/scenario_3/_view/nonenglish_stats?group=true"
    res = requests.get(nonenglish_url)
    json_text = json.loads(res.text)
    temp = json_text['rows']
    temp.sort(key = lambda x:x['value']['avg'], reverse=True)
    city,avg = [],[]
    for data in temp:
        city.append(data['key'])
        avg.append(data['value']['avg'])
    return {"city": city, "avg": avg}


# return the avg nonenglish stats and avg afinn stats of 6 main cities
def get_s3_b_data():
    nonenglish_url = "http://admin:admin@172.26.133.54:5984/all/_design/scenario_3/_view/nonenglish_stats?group=true"
    res = requests.get(nonenglish_url)
    json_text = json.loads(res.text)
    afinn_url = "http://admin:admin@172.26.133.54:5984/all/_design/scenario_3/_view/afinn_stats?group=true"
    afinn_res = requests.get(afinn_url)
    afinn_json_text = json.loads(afinn_res.text)
    nonenglish_df = pd.DataFrame.from_dict(json_text['rows'], orient="columns")
    afinn_df = pd.DataFrame.from_dict(afinn_json_text['rows'], orient="columns")
    merged_df = pd.merge(afinn_df, nonenglish_df, on='key')
    merged_df['afinn_avg'] = merged_df['value_x'].map(lambda x : x['avg'])
    merged_df['nonenglish_avg'] = merged_df['value_y'].map(lambda x : x['avg'])
    result = {'city': merged_df['key'].tolist(), 'afinn_avg': merged_df['afinn_avg'].tolist(), 'nonenglish_avg': merged_df['nonenglish_avg'].tolist()}
    return result


# return the avg nonenglish stats along with aurin economic & population stats
def get_s3_cd_data():
    s3_df = pd.read_csv('out_aurin_city.csv', dtype=str, header=0, encoding='ascii', engine='python')
    nonenglish_url = "http://admin:admin@172.26.133.54:5984/all/_design/scenario_3/_view/nonenglish_stats?group=true"
    res = requests.get(nonenglish_url)
    json_text = json.loads(res.text)
    view_df = pd.DataFrame.from_dict(json_text['rows'], orient="columns")
    view_df.rename(columns={"key": "city_name"}, inplace=True)
    view_df['avg'] = view_df['value'].map(lambda x : x['avg'])
    merged_df = pd.merge(s3_df, view_df, on='city_name')
    result = {'city': merged_df['city_name'].tolist(), 'avg': merged_df['avg'].tolist(), 'total_businesses_num': merged_df['total_businesses_num_3c'].tolist(), 'speak_other_langs_percentage': merged_df['speak_other_langs_percentage_3d'].tolist()}
    return result





