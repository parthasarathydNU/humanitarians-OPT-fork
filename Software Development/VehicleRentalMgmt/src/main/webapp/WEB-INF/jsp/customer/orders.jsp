<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<style><%@include file="/WEB-INF/css/style.css"%></style>
<meta charset="UTF-8">
<title>My Vehicles</title>
</head>
<body>
<jsp:include page="cusNavbar.jsp"/>
<h2 align="center">vehicles in use</h2>
<c:choose>
<c:when test="${vehicles.size() gt 0}"> 
<table id="tablestyle" border="1" cellpadding="1" cellspacing="1" align="center">
	<th></th>
	<th>licensePlate</th>
	<th>model</th>
	<th>Year</th>
	<th>Reserved Date</th>
	<th>Reserved Until</th>
	<th>Return Date</th>	
	
	<c:forEach items="${vehicles}" var="vehicle">
	<tr>
		<td><img width="100" height="100" src="/vehicle/images/${vehicle.imagePath}"/></td>
		<td>${vehicle.licensePlate}</td>
		<td>${vehicle.model}</td>
		<td>${vehicle.year}</td>
		<td>${vehicle.rentStartDate}</td>
		<td>${vehicle.rentEndDate}</td>
		<td>${vehicle.rentReturnDate}</td>
	</tr>
	</c:forEach>
</table>
</c:when>
<c:otherwise><p align="center">You have no vehciles in use.</p></c:otherwise>
</c:choose>
</body>
</html>