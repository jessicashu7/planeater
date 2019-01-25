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
  total = total.toFixed(1)
  quarter.querySelector("div.total_quarter_units").innerHTML= "Total Units: " + total;
  total_units()
}

function total_units(){
  var units = document.querySelectorAll("input.units")
  var total = 0;
  for(var i = 0; i<units.length; i++){
      total+=Number(units[i].value);
  }
  total = total.toFixed(1);
  document.getElementById("total_units").innerHTML= "Total Units: " + total;
}



function onSignIn(googleUser) {
  // var profile = googleUser.getBasicProfile();
  // $(".g-signin2").css("display","none");
  // //$(".data").css("display","block")
  //
  // $("#pic").attr('src', profile.getImageUrl())
  //profile.getEmail()

  // console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  // console.log('Name: ' + profile.getName());
  // console.log('Image URL: ' + profile.getImageUrl());
  // console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}


// //implemennt sign out next
// function signOut() {
//     var auth2 = gapi.auth2.getAuthInstance();
//     auth2.signOut().then(function () {
//       console.log('User signed out.');
//     });
// }
