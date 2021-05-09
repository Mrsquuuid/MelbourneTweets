function (doc) {
  if (doc.covid_words > 0 && doc.covid_words > 0){
    month_map = {
      "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
      "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    emit([doc.year, month_map[doc.month]], doc.afinn);
  }
}

