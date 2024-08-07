package com.vehicle.dao;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import org.hibernate.Criteria;
import org.hibernate.HibernateException;
import org.hibernate.Query;
import com.vehicle.exception.VehicleException;
import com.vehicle.pojo.User;
import com.vehicle.pojo.Vehicle;

public class VehicleDAO extends DAO {

    public VehicleDAO() {
    }
// Fetch all available vehicles

    public List<Vehicle> fetchAllVehicles() throws VehicleException {
        List<Vehicle> vehicles = new ArrayList<Vehicle>();
        System.out.println("In fetch all vehicles method");
        try {
            begin();
            Criteria criteria = getSession().createCriteria(Vehicle.class);
            vehicles = criteria.list();
            System.out.println("In fetch all vehicles method try block");
            commit();
        } catch (HibernateException e) {
            e.printStackTrace();
        } finally {
            System.out.println("In fetch all vehicles finally block");
            close();
        }
        return vehicles;

    }
    // fetch every reserved vehicle

    public LinkedHashMap<Vehicle, String> fetchAllReservedVechiles() throws VehicleException {
        LinkedHashMap<Vehicle, String> vehicles = new LinkedHashMap<Vehicle, String>();
        for (Vehicle vehicle : this.fetchAllVehicles()) {
            if (vehicle.getReservedByUser() != null && vehicle.getxUser() == null) {
                String UsrEmail = vehicle.getReservedByUser().getUsrEmail();
                vehicles.put(vehicle, UsrEmail);
            }
        }
        return vehicles;
    }
// Fetch reserved vehicles

//	public List<Vehicle> fetchReservedVehicles() throws VehicleException {
//
//		List<Vehicle> reservedVehicles = new ArrayList<Vehicle>();
//
//		for (Vehicle vehicle : this.fetchAllVehicles()) {
//
//			if (vehicle.getPickupReady() == true) {
//				reservedVehicles.add(vehicle);
//			}
//		}
//
//		return reservedVehicles;
//
//	}
    
// fetch vehicles currently using
    public LinkedHashMap<Vehicle, String> fetchVechilesInUse() throws VehicleException {
        LinkedHashMap<Vehicle, String> vehicles = new LinkedHashMap<Vehicle, String>();
        for (Vehicle vehicle : this.fetchAllVehicles()) {
            if (vehicle.getxUser() != null && vehicle.getReservedByUser() == null) {
                String UsrEmail = vehicle.getxUser().getUsrEmail();
                vehicles.put(vehicle, UsrEmail);
            }
        }
        return vehicles;
    }

 // fetch reserved vehicles by user
    public List<Vehicle> fetchReservedVehicleofUsr(User user) throws VehicleException {

        List<Vehicle> vehicles = new ArrayList<Vehicle>();
        try {
            begin();
            Query q = getSession().createQuery("from Vehicle where reservedByUser =:user");
            q.setEntity("user", user);
            vehicles = (List<Vehicle>) q.list();
            commit();
        } catch (HibernateException e) {

            e.printStackTrace();
        } finally {
            close();
        }
        return vehicles;
    }

    //vehicles in use by usr
    public List<Vehicle> fetchVechUsingbyUsr(User user) throws VehicleException {
        List<Vehicle> vehicles = new ArrayList<Vehicle>();
        try {
            begin();
            Query q = getSession().createQuery("from Vehicle where xUser =:user");
            q.setEntity("user", user);
            vehicles = (List<Vehicle>) q.list();
            commit();
        } catch (HibernateException e) {
            e.printStackTrace();
        } finally {
            close();
        }
        return vehicles;
    }

//FETCH VEHICLES BY ID
    public Vehicle fetchVehiclesbyId(int carId) throws VehicleException {
        try {
            begin();
            Query q = getSession().createQuery("from Vehicle where carId = :carId");
            q.setLong("carId",carId);
            Vehicle vehicle = (Vehicle) q.uniqueResult();
            commit();
            return vehicle;

        } catch (HibernateException e) {
            rollback();
            throw new VehicleException("unable to fetch vehicle by vehicle id: ", e);
        } finally {
            close();
        }

    }

    //fetchby liscence plate
    public boolean licencsePlateExists(String licensePlate) throws VehicleException {
        try {

            Query q = getSession()
                    .createQuery("from Vehicle where licensePlate = :licensePlate");
            q.setString("licensePlate", licensePlate);
            Object obj = q.uniqueResult();
            if (obj == null) {
                return false;
            }

        } catch (Exception e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
        return true;

    }

    // CRUD FOR vehicles
    public void saveVehicle(Vehicle vehicle) throws VehicleException {

        try {
            begin();
            getSession().save(vehicle);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }

    }

    public void updateVehicle(Vehicle vehicle) throws VehicleException {
        try {
            begin();
            getSession().update(vehicle);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
    }

    public void deleteVehicle(Vehicle vehicle) throws VehicleException {
        try {
            begin();
            getSession().delete(vehicle);
            commit();
        } catch (HibernateException e) {
            rollback();
            e.printStackTrace();
        } finally {
            close();
        }
    }

}
