<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://www.springframework.org/tags/form" prefix="form"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style><%@include file="/WEB-INF/css/style.css"%></style>
<title>add Vehicles</title>
</head>
<body>
<jsp:include page="ManagerNav.jsp"/>
<h2 align="center">Add Vehicles</h2>

<p align="center" style="color:red">${licencsePlateError}</p>

<form:form modelAttribute="vehicle" method="post" enctype="multipart/form-data">

<table id="tablestyle" align="center" cellpadding="1" cellspacing="1">
	<tr><td>
	licensePlate(4-8): 
	</td><td>
	<form:input path="licensePlate" required="required" minlength="4" maxlength="8"/>
	</td></tr>
	<tr><td>
	model: 
	</td><td>
	<form:input path="model" required="required"/>
	</td></tr>
	<tr><td>
	year: 
	</td><td>
	<form:input path="year" required="required"/>
	</td></tr>
	<tr><td>
    choose Image of vehicle:
    </td><td>
    <input type="file" name="imgFile" accept="image/*" required="required"/>
    </td></tr>
</table>	
	<p align="center"><input type="submit" value="Add"/></p>

</form:form>

</body>
</html>