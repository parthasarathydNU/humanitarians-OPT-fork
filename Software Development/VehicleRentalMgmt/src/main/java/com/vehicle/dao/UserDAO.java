package com.vehicle.dao;

import java.util.ArrayList;
import java.util.List;
import org.hibernate.Criteria;
import org.hibernate.HibernateException;
import org.hibernate.Query;
import org.springframework.stereotype.Component;
import com.vehicle.exception.VehicleException;
import com.vehicle.pojo.User;

@Component
public class UserDAO extends DAO {

    public UserDAO() {
    }

    //USER CRUD  
    public void saveUser(User user) throws VehicleException {
        try {
            begin();
            getSession().save(user);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
    }

    public void updateUser(User user) throws VehicleException {
        try {
            begin();
            getSession().update(user);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
    }

    public void deleteUser(User user) throws VehicleException {
        try {
            begin();
            getSession().delete(user);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
    }

    public User fetchUsrById(int usrId) throws VehicleException {
        try {
            begin();
            Query q = getSession().createQuery("from User where usrId = :usrId");
            q.setLong("usrId", usrId);
            User user = (User) q.uniqueResult();
            commit();
            return user;
        } catch (HibernateException e) {
            rollback();
            throw new VehicleException("unable to fetch user with user id: ", e);
        } finally {
            close();
        }

    }

    public User fetchUsrByusrEmail(String usrEmail) throws VehicleException {
        try {

            Query q = getSession().createQuery("from User where usrEmail = :usrEmail");

            q.setString("usrEmail", usrEmail);
            User user = (User) q.uniqueResult();

            return user;
        } catch (Exception e) {
            rollback();
            throw new VehicleException("unable to fetch user with user user email: ", e);
        } finally {
            close();
        }
    }

    public List<User> fetchEveryUsr() throws VehicleException {
        List<User> users = new ArrayList<User>();
        try {
            begin();
            Criteria criteria = getSession().createCriteria(User.class);
            users = criteria.list();
            commit();
            return users;
        } catch (Exception e) {
            throw new VehicleException("unable to fetch all users: ", e);
        } finally {
            close();
        }

    }

//    public List<Vehicle> fetchAllReservedVehicles() throws VehicleException {
//        List<Vehicle> vehicles = new ArrayList<Vehicle>();
//        try {
//            Criteria criteria = getSession().createCriteria(Vehicle.class);
//            vehicles = criteria.list();
//
//            return vehicles;
//        } catch (Exception e) {
//            throw new VehicleException("Could not fetch all books: ", e);
//        } finally {
//            close();
//        }
//
//    }
}
