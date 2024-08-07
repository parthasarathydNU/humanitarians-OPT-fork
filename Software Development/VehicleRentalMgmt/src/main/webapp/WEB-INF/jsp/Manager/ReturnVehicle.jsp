<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>Vehicle Returns</title>
</head>
<body>
<jsp:include page="ManagerNav.jsp"/>
<h2 align="center">Vehicle Returns</h2>
<c:choose>
<c:when test="${vehicles.size() gt 0}">
<table id="tablestyle" border="1" cellpadding="1" cellspacing="1" align="center">

	
	<th></th>
	<th>licensePlate</th>
	<th>model</th>
	<th>year</th>
	<th>Reserved From</th>
	<th>Reserved Until</th>
	<th>Return Date</th>
	<th>Reserved By</th>
	<th>Action</th>
	
	<c:forEach items="${vehicles}" var="vehicle">
	<tr>
		<td><img width="100" height="100" src="/vehicle/images/${vehicle.key.imagePath}"/></td>
		
		<td>${vehicle.key.licensePlate}</td>
		<td>${vehicle.key.model}</td>
		<td>${vehicle.key.year}</td>
		<td>${vehicle.key.rentStartDate}</td>
		<td>${vehicle.key.rentEndDate}</td>
		<td>${vehicle.key.rentReturnDate}</td>
		<td>${vehicle.value}</td>
		
		<td>	
 		<a href="return.htm?carId=${vehicle.key.carId}&usrEmail=${vehicle.value}">Returned By Customer</a>
		</td>
	</tr>
	</c:forEach>

</table>
</c:when>
<c:otherwise><p align="center"> No Vehicles in use as of now!.</p></c:otherwise>
</c:choose>
</body>
</html>