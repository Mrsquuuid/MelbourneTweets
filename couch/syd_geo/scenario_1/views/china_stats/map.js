function (doc) {
  if (doc.china_words > 0){
    emit(doc.SA2_names, doc.afinn);
  }
}