/* admin page*/

function showpass() {
  var x = document.getElementById("mypassword");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

/*register page*/

function validateForm() {
  var x = document.forms["myForm"]["fullname"].value;
  var e = document.forms["myForm"]["email"].value;
  if (x == "") 
    alert("Name must be filled out");
     
  else if (e == "") 
    
    alert("Email must be filled out");
    
  return false;
}

function resetFun() {  
 document.getElementById("myForm").reset();
}

/*admin page*/

function validateAdmin() {
  var x = document.forms["adminForm"]["username"].value;
  var e = document.forms["adminForm"]["mypassword"].value;
  if (x == "") 
    alert("User Name must be filled out");
     
  else if (e == "") 
    
    alert("Password must be filled out");
    
  return false;
}


/*register validation*/

bootstrapValidate('fullname','required:please fill out this field')
bootstrapValidate('fullname','alpha:you can only input alphabetic characters')
bootstrapValidate('studentid','numeric:please only enter numeric characters')
bootstrapValidate('studentid','required:please fill out this field')
bootstrapValidate('email','email:Enter a valid email address')
bootstrapValidate('email','required:please fill out this field')
bootstrapValidate('courses','required:please fill out this field')
bootstrapValidate('courses','alphanumeric:you can only input alphanumeric characters') 
