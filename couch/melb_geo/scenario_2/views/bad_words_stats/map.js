function (doc) {
  if (doc.vulgar_words > 0 || doc.crime_words > 0 || doc.alcohol_words > 0){
    emit(doc.SA2_names, 1);
  }else{
    emit(doc.SA2_names, 0);
  }
}