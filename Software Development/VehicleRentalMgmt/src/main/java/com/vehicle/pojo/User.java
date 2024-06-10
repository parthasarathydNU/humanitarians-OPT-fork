package com.vehicle.pojo;

import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;

import org.springframework.stereotype.Component;

@Component
@Entity
@Table(name = "USERS")
public class User {
 @OneToMany(mappedBy = "reservedByUser")
    private List<Vehicle> vehilclesReserved;

    @OneToMany(mappedBy = "xUser")
    private List<Vehicle> vehicles;
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
   private int usrId;

    @Column(unique = true)
   private String usrEmail;
    private String usrPassword;
   private String name;
   private String userAddress;
   private String userPhonenum;
   private String title;
    public User() {

    }

    public User(String usrEmail, String usrPassword, String name, String userAddress, String userPhonenum, String title) {
        this.usrEmail = usrEmail;
        this.usrPassword = usrPassword;
        this.userAddress = userAddress;
        this.userPhonenum = userPhonenum;
        this.title = title;

    }

    public int getUsrId() {
        return usrId;
    }

    public void setUsrId(int usrId) {
        this.usrId = usrId;
    }

    public String getUsrEmail() {
        return usrEmail;
    }

    public void setUsrEmail(String usrEmail) {
        this.usrEmail = usrEmail;
    }

    public String getUsrPassword() {
        return usrPassword;
    }

    public void setUsrPassword(String usrPassword) {
        this.usrPassword = usrPassword;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUserAddress() {
        return userAddress;
    }

    public void setUserAddress(String userAddress) {
        this.userAddress = userAddress;
    }

    public String getUserPhonenum() {
        return userPhonenum;
    }

    public void setUserPhonenum(String userPhonenum) {
        this.userPhonenum = userPhonenum;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

}
