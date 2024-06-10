package com.vehicle.dao;
import org.hibernate.HibernateException;
import org.hibernate.Query;
import org.springframework.stereotype.Component;
import com.vehicle.exception.VehicleException;

@Component
public class LoginDAO extends DAO {

    public LoginDAO() {
    }

    //validate users
    public boolean checkCustmer(String userEmail, String usrPassword) throws VehicleException {
        try {
            Query qry = getSession().createQuery("from User where usrEmail=:usrEmail and usrPassword=:usrPassword and title='customer'");
            qry.setString("usrEmail", userEmail);
            qry.setString("usrPassword", usrPassword);
            Object res = qry.uniqueResult();
            if (res == null) {
                return false;
            }
        } catch (HibernateException e) {
            throw new VehicleException("exception in customercheck  ", e);
        } finally {
            close();
        }
        return true;

    }

    public boolean checkAdmin(String userEmail, String usrPassword) throws VehicleException {
        try {
            Query qry = getSession().createQuery("from User where  usrEmail=:usrEmail and usrPassword=:usrPassword and title='admin'");
            qry.setString("usrEmail", userEmail);
            qry.setString("usrPassword", usrPassword);
            Object res = qry.uniqueResult();
            if (res == null) {
                return false;
            }

        } catch (Exception e) {
            throw new VehicleException("Admincheck exception ", e);
        } finally {
            close();
        }
        return true;
    }

    public boolean checkEmployee(String userEmail, String usrPassword) throws VehicleException {
        try {
            Query qry = getSession().createQuery("from User where usrEmail=:usrEmail and usrPassword=:usrPassword and title='employee'");
            qry.setString("usrEmail", userEmail);
            qry.setString("usrPassword", usrPassword);
            Object obj = qry.uniqueResult();
            if (obj == null) {
                return false;
            }
        } catch (Exception e) {
            throw new VehicleException("checkEmployee exception ", e);
        } finally {
            close();
        }

        return true;

    }
}
