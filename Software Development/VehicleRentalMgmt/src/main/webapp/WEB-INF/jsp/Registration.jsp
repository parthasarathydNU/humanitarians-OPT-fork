<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>

<html>
<head>
    <title>Registartion Form</title>
</head>
<body>
<style><%@include file="/WEB-INF/css/style.css"%></style>
<div style="background-color: #FFDD33;color:black;font-family: Times New Roman", Times, serif;height:60px;line-height:2.5em">   

<h2 align="center">Vehicle Rental Management System</h2>
</div>
<h2 align="center">Register a New User</h2>
<p align="center" style="color:red">${error}</p>
<form:form modelAttribute="user" method="post">
<table id="tablestyle" align="center" cellpadding="1" cellspacing="1">
<tr>
 <td>User Email:</td>
    <td><form:input type="email" path="usrEmail" size="30" required="required" placeholder="Enter email id" /> 
    <font color="red"><form:errors path="usrEmail"/></font></td>
</tr><tr>
    <td>User Password:</td>
    <td><form:input type="password" path="usrPassword" size="30" minlength="6" maxlength="8" required="required" placeholder="6 to 8 chars" /> 
    <font color="red"><form:errors path="usrPassword"/></font></td>
</tr>
<tr>
    <td>User Name:</td>
    <td><form:input path="name" size="30" required="required"/> 
    <font color="red"><form:errors path="name"/></font></td>
</tr>
<tr>
    <td>Address:</td>
    <td><form:input path="userAddress" size="30" required="required" />
     <font color="red"><form:errors path="userAddress"/></font></td>
</tr>
<tr>
    <td>Phone number</td>
    <td><form:input path="userPhonenum" pattern="[0-9]{3}[0-9]{3}[0-9]{4}" size="30"  maxlength="10" required="required" placeholder="10 digits number"/> 
    <font color="red"><form:errors path="userPhonenum"/></font></td>
</tr>
<tr>
<td>Title:</td>
<td>
    <form:radiobutton path="title" value="customer" required="required"/>Customer
    <br><br>
        <form:radiobutton path="title" value="employee" required="required" />Manager
      <br><br>
        <form:radiobutton path="title" value="admin" required="required"/>Admin
</td>
</tr>
<tr>
<td></td>
<td><input  type="submit" value="Create" /></td>
</tr>
</table>
</form:form>
</body>
</html>