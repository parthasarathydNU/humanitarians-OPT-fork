<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>Edit Success</title>
</head>
<body>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif>   
   <a style="color:black;text-decoration:none" href="adminhome.htm?usrEmail=${sessionScope.usrEmail}">Home</a> |
 <a style="color:black;text-decoration:none" href="listofusrs.htm?usrEmail=${sessionScope.usrEmail}">Manage Users</a>
    <a style="color:black;text-decoration:none;float:right" href="signout.htm?usrEmail=${sessionScope.usrEmail}">Logout</a> 
     <label style="float:right">Hi ${sessionScope.usrEmail} |</label>
     
</div>

<h3 align="center">User Details Changed Successfully</h3>
</body>
</html>