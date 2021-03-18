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
  var x = document.forms["myform"]["fullname"].value;
  var e = document.forms["myform"]["email"].value;
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