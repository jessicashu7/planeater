function check_units(units){
  if (units.value.length > 3){
    units.value = units.value.slice(0,3)
  }
  if (units.value < 0){
    units.value = 0
  }
  else if (units.value > 8){
    units.value = 8
  }
  total_quarter_units(units.parentElement.parentElement)
}

function total_quarter_units(quarter){
  var units = quarter.querySelectorAll("input.units");
  var total = 0;
  for(var i = 0; i<units.length; i++){
      total+=Number(units[i].value);
  }
  quarter.querySelector("div.total_quarter_units").innerHTML= "Total Units: " + total;
  total_units()
}

function total_units(){
  var units = document.querySelectorAll("input.units")
  var total = 0;
  for(var i = 0; i<units.length; i++){
      total+=Number(units[i].value);
  }
  document.getElementById("total_units").innerHTML= "Total Units: " + total;
}
