import couchdb

def createView(dbConn, designDoc, viewName1, mapFunction1, reduceFunction1, viewName2, mapFunction2, reduceFunction2, viewName3, mapFunction3, reduceFunction3):
    data = {
        "_id": f"_design/{designDoc}",
        "views": {
            viewName1: {
                "map": mapFunction1,
                "reduce": reduceFunction1
            },
            viewName2: {
                "map": mapFunction2,
                "reduce": reduceFunction2
            },
            viewName3: {
                "map": mapFunction3,
                "reduce": reduceFunction3
            }
        },
        "language": "javascript",
        "options": {"partitioned": False }
    }
    print("creating view " + designDoc + "/" + viewName1)
    print("creating view " + designDoc + "/" + viewName2)
    print("creating view " + designDoc + "/" + viewName3)
    dbConn.save(data)


if __name__ == '__main__':
    # create syd relative views for scenario 1
    url_connect = "http://admin:admin@172.17.0.4:5984"
    couch = couchdb.Server(url_connect)
    db_name = "twitter"
    db = couch[db_name]

    # view: china_covid_stats
    mapFunction1 = '''function (doc) {
                      if (doc.covid_words > 0 && doc.covid_words > 0){
                        month_map = {
                          "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                        }
                        emit([doc.year, month_map[doc.month]], doc.afinn);
                      }
                    }'''
    reduceFunction1 = '''function(key, values, rereduce) {
                          var result = {sum: 0, avg:0, count: 0};
                          for(i=0; i < values.length; i++) {
                            if(rereduce) {
                                result.sum = result.sum + values[i].sum;
                                result.count = result.count + values[i].count;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            } else {
                                result.sum = sum(values);
                                result.count = values.length;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            }
                          }
                          return(result);
                        }'''

    # view: china_stats
    mapFunction2 = '''function (doc) {
                      if (doc.china_words > 0){
                        month_map = {
                          "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                        }
                        emit([doc.year, month_map[doc.month]], doc.afinn);
                      }
                    }'''
    reduceFunction2 = '''function(key, values, rereduce) {
                          var result = {sum: 0, avg:0, count: 0};
                          for(i=0; i < values.length; i++) {
                            if(rereduce) {
                                result.sum = result.sum + values[i].sum;
                                result.count = result.count + values[i].count;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            } else {
                                result.sum = sum(values);
                                result.count = values.length;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            }
                          }
                          return(result);
                        }'''

    # view: china_vulgar_stats
    mapFunction3 = '''function (doc) {
                      if (doc.china_words > 0 && doc.vulgar_words > 0){
                        month_map = {
                          "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
                        }
                        emit([doc.year, month_map[doc.month]], doc.afinn);
                      }
                    }'''
    reduceFunction3 = '''function(key, values, rereduce) {
                          var result = {sum: 0, avg:0, count: 0};
                          for(i=0; i < values.length; i++) {
                            if(rereduce) {
                                result.sum = result.sum + values[i].sum;
                                result.count = result.count + values[i].count;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            } else {
                                result.sum = sum(values);
                                result.count = values.length;
                                result.avg = Math.round(result.sum / result.count * 100) / 100;
                            }
                          }
                          return(result);
                        }'''

    createView(db, "scenario_1", "china_covid_stats", mapFunction1, reduceFunction1, "china_stats", mapFunction2, reduceFunction2, "china_vulgar_stats", mapFunction3, reduceFunction3)