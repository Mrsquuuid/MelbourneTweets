function (doc) {
  if (doc.lang !== "en" && doc.lang !== "und"){
    emit(doc.location, 1);
  }else{
    emit(doc.location, 0);
  }
}