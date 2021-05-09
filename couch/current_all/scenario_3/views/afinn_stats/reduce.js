function(key, values, rereduce) {
  var result = {sum: 0, avg:0, count: 0};
  for(i=0; i < values.length; i++) {
    if(rereduce) {
        result.sum = result.sum + values[i].sum;
        result.count = result.count + values[i].count;
        result.avg = Math.round(result.sum / result.count * 10000) / 10000;
    } else {
        result.sum = sum(values);
        result.count = values.length;
        result.avg = Math.round(result.sum / result.count * 10000) / 10000;
    }
  }
  return(result);
}