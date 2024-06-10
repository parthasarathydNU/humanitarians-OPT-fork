<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<%@taglib prefix="form" uri="http://www.springframework.org/tags/form"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix = "c"%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>vehicles</title>
</head>
<body>
<jsp:include page="ManagerNav.jsp"/>
<h2 align="center">Vehicles</h2>

<p align="center">
<a href="vehiclesadd.htm">Add Vehicles</a></p>
<br><br>
<c:choose>
<c:when test="${vehicle.size() gt 0}">

<table id="tablestyle" align="center" border="1" cellpadding="1" cellspacing="1">

	<th>Vehicle</th>
	<th>licensePlate</th>
	<th>model</th>
	<th>year</th>
	<th>Reserved From</th>
	<th>Reserved Until</th>
	<th>Return By</th>
	
	<th>Reserved By</th>
<th>In Use By</th>
	<th>Action</th>
	 

	<c:forEach items="${vehicle}" var="v1">
	<tr>
		<td><img width="100" height="100" src="/vehicle/images/${v1.imagePath}"/></td>
		<td>${v1.licensePlate}</td>
		<td>${v1.model}</td>
		<td>${v1.year}</td>
		<td>${v1.rentStartDate}</td>
		<td>${v1.rentEndDate}</td>
		<td>${v1.rentReturnDate}</td>
		<td>${v1.getReservedByUser().getUsrEmail()}</td>
		<td>${v1.getxUser().getUsrEmail()}</td>
		
		
	<td><a href="editvehicle.htm?carId=${v1.carId}">Edit</a> |
		
		<a href="deleteall.htm?carId=${v1.carId}">Delete</a>
		
		
		
		
		</td>
	</tr>
	</c:forEach>
	

</table>
</c:when>
<c:otherwise><p align="center">There are no Vehicles in the catalog. Click Add Vehicles to add Vehicles.</c:otherwise>
</c:choose>
</body>
</html>