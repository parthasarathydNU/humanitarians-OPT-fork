<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form" %>
<html>
<head>
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>SignIn</title>
</head>
<body>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif">   

<h2 align="center">Vehicle Rental Management System</h2>
<img src="https://cdn-icons-png.flaticon.com/512/632/632682.png" alt="logo" width="50" height="50">
</div>

<h2 align="center">Sign In</h2>

<form:form modelAttribute="user" method="post">
<p style="color:red" align="center">${error}</p>
<div align="center">

    <label>User Email:</label>
    <td><form:input path="usrEmail" size="30" required="required" /></td>
    <br><br>
    <label>User Password:</label>
    <td><form:password path="usrPassword" size="30" required="required" /></td>
     <br><br>
	<a href="register.htm">New user?</a>
	<p align="center"><input type="submit" value="Login" /></p>
	 <br>   <br>
	
</form:form>
</body>
</html>
