function total_quarter_units(quarter){
  var units = quarter.querySelectorAll("input.units");
  var total = 0;
  for(var i = 0; i<units.length; i++){
      total+=Number(units[i].value);
  }
  quarter.querySelector("div.total_quarter_units").innerHTML= "Total Units: " + total;
}
