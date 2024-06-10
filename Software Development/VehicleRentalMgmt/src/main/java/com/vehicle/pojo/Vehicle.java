package com.vehicle.pojo;

import java.time.LocalDate;
import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.Transient;

import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Component
@Entity
@Table(name = "VEHICLES")
public class Vehicle {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	int carId;

	@Column(unique = true)
	String licensePlate;
	String model;
	Integer year;
	LocalDate rentReturnDate = null;
	LocalDate rentStartDate = null;
	LocalDate rentEndDate = null;
	Boolean pickupReady = false;

	
	@ManyToOne(cascade = {CascadeType.DETACH, CascadeType.MERGE, CascadeType.PERSIST, CascadeType.REFRESH},
			fetch = FetchType.EAGER)
	private User reservedByUser;
	
	@ManyToOne(cascade = {CascadeType.DETACH, CascadeType.MERGE, CascadeType.PERSIST, CascadeType.REFRESH},
			fetch = FetchType.EAGER)
	private User xUser;
	
	@Column(name = "pic")
	private String imagePath;
	
	@Transient
	private MultipartFile imgFile;

	public int getCarId() {
		return carId;
	}

	public void setCarId(int carId) {
		this.carId = carId;
	}

	public String getLicensePlate() {
		return licensePlate;
	}

	public void setLicensePlate(String licensePlate) {
		this.licensePlate = licensePlate;
	}

	public String getModel() {
		return model;
	}

	public void setModel(String model) {
		this.model = model;
	}

	public Integer getYear() {
		return year;
	}

	public void setYear(Integer year) {
		this.year = year;
	}

	public LocalDate getRentReturnDate() {
		return rentReturnDate;
	}

	public void setRentReturnDate(LocalDate rentReturnDate) {
		this.rentReturnDate = rentReturnDate;
	}

	public LocalDate getRentStartDate() {
		return rentStartDate;
	}

	public void setRentStartDate(LocalDate rentStartDate) {
		this.rentStartDate = rentStartDate;
	}

	public LocalDate getRentEndDate() {
		return rentEndDate;
	}

	public void setRentEndDate(LocalDate rentEndDate) {
		this.rentEndDate = rentEndDate;
	}

	public Boolean getPickupReady() {
		return pickupReady;
	}

	public void setPickupReady(Boolean pickupReady) {
		this.pickupReady = pickupReady;
	}

	public User getReservedByUser() {
		return reservedByUser;
	}

	public void setReservedByUser(User reservedByUser) {
		this.reservedByUser = reservedByUser;
	}

	public User getxUser() {
		return xUser;
	}

	public void setxUser(User xUser) {
		this.xUser = xUser;
	}

	public String getImagePath() {
		return imagePath;
	}

	public void setImagePath(String imagePath) {
		this.imagePath = imagePath;
	}

	public MultipartFile getImgFile() {
		return imgFile;
	}

	public void setImgFile(MultipartFile imgFile) {
		this.imgFile = imgFile;
	}

}
