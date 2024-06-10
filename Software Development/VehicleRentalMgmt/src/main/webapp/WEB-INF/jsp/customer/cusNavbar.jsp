<style><%@include file="/WEB-INF/css/style.css"%></style>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif>   
    <a style="color:black;text-decoration:none" href="cusHome.htm?usrEmail=${sessionScope.usrEmail}">Home</a> |
   	<a style="color:black;text-decoration:none" href="fetchVehicles.htm?usrEmail=${sessionScope.usrEmail}">Browse vehicles</a> | 
    <a style="color:black;text-decoration:none" href="orders.htm?usrEmail=${sessionScope.usrEmail}">Vehicles In Use</a> | 
    <a style="color:black;text-decoration:none" href="bookedVehicles.htm?usrEmail=${sessionScope.usrEmail}">My Reservations</a>
     <a style="color:black;text-decoration:none;float:right" href="signout.htm?usrEmail=${sessionScope.usrEmail}">Logout</a> 
     <label style="float:right">Hi ${sessionScope.usrEmail} |</label>
</div>