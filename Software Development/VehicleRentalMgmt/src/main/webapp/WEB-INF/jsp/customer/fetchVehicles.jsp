<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<style><%@include file="/WEB-INF/css/style.css"%></style>
<meta charset="UTF-8">
<title>fetch vehicles</title>
</head>
<body>
<jsp:include page="cusNavbar.jsp"/>
<h3 align="center">Browse Cars</h3>

<c:if test="${usrvehicles.size() eq 3}">

<p style="color:red" align="center"user can reserve only three cars</p>
</c:if>
<c:choose>
<c:when test="${vehicles.size() gt 0}">
<table id="tablestyle" border="1" cellpadding="1" cellspacing="1" align="center">
	<th></th>
	<th>licensePlate</th>
	<th>model</th>
	<th>year</th>
	<th>Return Date</th>
	<th>Reserved Until</th>
	<th>Action</th>
	
	
	<c:forEach items="${vehicles}" var="vehicle">
	<tr>
		<td><img width="100" height="100" src="/vehicle/images/${vehicle.imagePath}"/></td>
		<td>${vehicle.licensePlate}</td>
		<td>${vehicle.model}</td>
		<td>${vehicle.year}</td>
		<td>${vehicle.rentReturnDate}</td>
		<td>${vehicle.rentEndDate}</td>
		<td>	
 		<c:choose>
		<c:when test= "${vehicle.rentEndDate != null || vehicle.rentReturnDate !=null}">
		
		Reserved
		</c:when>
		<c:when test="${usrvehicles.size() eq 3}">
		</c:when>
		<c:otherwise>
		
		<a href="reservationconfirm.htm?carId=${vehicle.carId} & usrEmail=${sessionScope.usrEmail}">Select</a>
		
		</c:otherwise>
		</c:choose>
		</td>
	</tr>
	</c:forEach>
</table>
</c:when>
	<c:otherwise>
	<p align="center">There are no vehciles available.</p>
	</c:otherwise>
</c:choose>
</body>
</html>