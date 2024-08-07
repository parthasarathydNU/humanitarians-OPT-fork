<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<style><%@include file="/WEB-INF/css/style.css"%></style>
<meta charset="UTF-8">
<title>User Modify Page</title>
</head>
<body>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif>   
   <a style="color:black;text-decoration:none" href="adminhome.htm?usrEmail=${sessionScope.usrEmail}">Home</a> |
 <a style="color:black;text-decoration:none" href="listofusrs.htm?usrEmail=${sessionScope.usrEmail}">Manage Users</a>
    <a style="color:black;text-decoration:none;float:right" href="signout.htm?usrEmail=${sessionScope.usrEmail}">Logout</a> 
     <label style="float:right">Hi ${sessionScope.usrEmail} |</label>
     
</div>

<h3 align="center">Modify User </h3>

<form action="usermodify.htm"" method="POST">

<input type="hidden" name="uid2" value="${user.getUsrId()}"/>

<table id="tablestyle" cellpadding="1" cellspacing="1" align="center">
	<tr>
	<td>Email:</td>
	<td>${user.getUsrEmail()}</td>
	</tr>
	<tr>
	<td>Name:</td>
	<td>${user.getName()}</td>
	</tr>
	<tr>
	<td>Address:</td>	
	<td><input type="text" name="userAddress" value="${user.getUserAddress()}" 
                   style="font-weight: bold" required="required"/>
	<p style="color:red">${addressErr}</p>
	</td>
	</tr>
	<tr>
	<td>Contact: (10 digits)</td>
	<td><input type="tel" pattern="[0-9]{3}[0-9]{3}[0-9]{4}" maxlength="10"
	 name="userPhonenum" value="${user.getUserPhonenum()}" 
         style="font-weight: bold" required="required"/>
	<p style="color:red">${contactErr}</p>
	</td>
	</tr>
	<tr>
	<td>Title:</td>
	<td>${user.getTitle()}</td>
	</tr>
</table>
<br>
	<p align="center"><input style="width:100px"  type="submit" value="Edit"></p>
</form>
</body>
</html>