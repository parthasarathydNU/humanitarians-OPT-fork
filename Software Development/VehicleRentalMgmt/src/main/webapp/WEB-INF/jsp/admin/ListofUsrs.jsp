<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>All Users</title>
<style><%@include file="/WEB-INF/css/style.css"%></style>
</head>
<body>
    <div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif>   
   <a style="color:black;text-decoration:none" href="adminhome.htm?usrEmail=${sessionScope.usrEmail}">Home</a> |
 <a style="color:black;text-decoration:none" href="listofusrs.htm?usrEmail=${sessionScope.usrEmail}">Manage-Users</a>
    <a style="color:black;text-decoration:none;float:right" href="signout.htm?usrEmail=${sessionScope.usrEmail}">Logout</a> 
     <label style="float:right">Hi ${sessionScope.usrEmail} |</label>
     
</div>
<h2 align="center">All Users</h2>
<br>
<table id="tablestyle" border="1" cellpadding="1" cellspacing="1" align="center">
	<th>User ID</th>
	<th>User Email</th>
	<th>User Name</th>
	<th>Address</th>
	<th>Phone Number</th>
	<th>Title</th>
	<th>Action</th>
	
	<c:forEach items="${user}" var="user">
	<c:if test="${user.title ne 'admin'}">
	<tr>
		<td>${user.usrId}</td>
		<td>${user.usrEmail}</td>
		<td>${user.name}</td>
		<td>${user.userAddress}</td>
		<td>${user.userPhonenum}</td>
		<td>${user.title}</td>
		<td><a href="usermodify.htm?usrId=${user.usrId}">Edit</a> | 
		<a href="userdelete.htm?usrId=${user.usrId}">Delete</a>
		</td>
	</tr>
	</c:if>
	</c:forEach>

</table>

</body>
</html>