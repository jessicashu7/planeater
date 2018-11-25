function total_units_quarter(){
    var array = document.getElementsByName("num_units");
    var total = 0;
    for(var i = 0; i<array.length; i++){
        total+=Number(array[i].value);
    }
    document.getElementById("total_fall_quarter").innerHTML= "Total Units: " + total;
}
