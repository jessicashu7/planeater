
$(document).ready(function(){

  var $input = $(".typeahead");
  $input.typeahead({
     source: course_source,
     autoSelect: false
  });

  $input.change(function() {
    //console.log("input name " + this.name);
    var current = $(this).typeahead("getActive");
    //console.log("current active is " + current.name);
    if (current) {
      // Some item from your model is active!
      if (current.name == $(this).val()) {
        // This means the exact match is found. Use toLowerCase() if you want case insensitive match.
        //console.log("currently active matches");
        var units_input_name = this.name + "_units";
        //console.log(units_input_name);
        //console.log(current.course_units);
        units_input = $(document).get(0).getElementsByName(units_input_name)[0];
        units = current.course_units.split("-")[0].trim()
        //console.log("min: " + units)
        // error checking because this assumes it is in form like 2-5
        units_input.value = parseInt(units);
        check_units(units_input);
      } else {
        //console.log("partial match with " + current.name);
        // This means it is only a partial match, you can either add a new item
        // or take the active if you don't want new items
      }
    } else {
      // Nothing is active so it is a new value (or maybe empty value)
      //console.log("EMPTY");
    }

  });
});
