<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>User Delete page</title>
</head>
<body>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif>   
   <a style="color:black;text-decoration:none" href="adminhome.htm?usrEmail=${sessionScope.usrEmail}">Home</a> |
 <a style="color:black;text-decoration:none" href="listofusrs.htm?usrEmail=${sessionScope.usrEmail}">Manage Users</a>
    <a style="color:black;text-decoration:none;float:right" href="signout.htm?usrEmail=${sessionScope.usrEmail}">Logout</a> 
     <label style="float:right">Hi ${sessionScope.usrEmail} |</label>
     
</div>
<h2 align="center">Delete User Details</h2>
<br>
<form style="text-align:center" action="userdelete.htm" method="POST">

<input type="hidden" name="usrdel" value="${user.usrId}"/>

<table id="tablestyle" align="center">

	<tr><td>Email:</td><td>${user.usrEmail}</td></tr>
	<tr><td>Name:</td><td>${user.name}</td></tr>
	<tr><td>Address:</td><td>${user.userAddress}</td></tr>
	<tr><td>Contact:</td><td>${user.userPhonenum}</td></tr>
	<tr><td>Role:</td><td>${user.title}</td></tr>
</table>
<input type="hidden" name="usrEmail" value="${user.usrEmail}"/>
<input type="hidden" name="name" value="${user.name}"/>
<input type="hidden" name="usrPassword" value="${user.usrPassword}"/>
<input type="hidden" name="userAddress" value="${user.userAddress}"/>
<input type="hidden" name="userPhonenum" value="${user.userPhonenum}"/>
<input type="hidden" name="title" value="${user.title}"/>
<br>
<input style="width:100px"  type="submit" value="Delete"> 
</form>
</body>
</html>