package com.vehicle.controller;

import com.vehicle.dao.UserDAO;
import com.vehicle.dao.VehicleDAO;
import com.vehicle.pojo.User;
import com.vehicle.pojo.Vehicle;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.support.SessionStatus;
import java.io.File;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Random;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

@Controller
public class ManagerController {

//manager view page
    @GetMapping("/managerhome.htm")
    public String fetchManagerview(Model model) {

        return "Manager/ManagerHome";
    }

    // vehicles add
    @GetMapping("/vehiclesadd.htm")
    public String vehiclesAdd(ModelMap model, Vehicle vehicle, HttpServletRequest request) {
        HttpSession session = request.getSession();
        model.addAttribute("vehicle", vehicle);
        return "Manager/VehiclesAdd";
    }

    @PostMapping("/vehiclesadd.htm")
    public String vehicleSave(@ModelAttribute("vehicle") Vehicle vehicle, BindingResult result, SessionStatus status,
            VehicleDAO vehicleDAO, Model model) throws Exception {
        vehicle.setPickupReady(false);
        if (vehicleDAO.licencsePlateExists(vehicle.getLicensePlate())) {
            String licencsePlateError = "licencsePlate number already exists!";
            System.out.println(licencsePlateError);
            model.addAttribute("licencsePlateError", licencsePlateError);
            return "Manager/VehiclesAdd";
        }
        String imgp = "img_" + System.currentTimeMillis() + "" + new Random().nextInt(100000000) + ""
                + new Random().nextInt(100000000) + ".jpg";

        vehicle.setImagePath(imgp);
        try {

            vehicle.getImgFile().transferTo(new File("src/main/webapp/images/" + imgp));
        } catch (IllegalStateException e1) {

        } catch (IOException e1) {

        }

        vehicleDAO.saveVehicle(vehicle);
        if (result.hasErrors()) {
            return "Manager/VehiclesAdd";
        }
        status.setComplete();
        return "Manager/vehicleAdded";
    }

    //edit vehicle
    @GetMapping("/editvehicle.htm")
    public String fetchEditVehicle(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
            throws Exception {

        HttpSession session = request.getSession();
        String cid = request.getParameter("carId");
        int carId = Integer.parseInt(cid);
        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);
        System.out.println("succesfully fetched - model in edit vehicle" + vehicle.getModel());
        System.out.println("year in edit vehicle" + vehicle.getYear());
        model.addAttribute(vehicle);

        return "Manager/EditVehicle";
    }

    @PostMapping("/editvehicle.htm")
    public String EditVehiclePost(SessionStatus status,
            VehicleDAO vehicleDAO, HttpServletRequest request, UserDAO userdao) throws Exception {
        HttpSession session = request.getSession();
        int carId = Integer.parseInt(request.getParameter("c1"));
        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);
        String model = request.getParameter("model");
        String year1 = request.getParameter("year");
        int castedYear = Integer.parseInt(year1);
        System.out.println("Casted year value - " + castedYear);

        String deleteRsvrtn = request.getParameter("deleteRsvrtn");

        String deleteUsr = request.getParameter("deleteUsr");
        vehicle.setRentStartDate(vehicle.getRentStartDate());
        vehicle.setRentEndDate(vehicle.getRentEndDate());
        vehicle.setRentReturnDate(vehicle.getRentReturnDate());
        vehicle.setPickupReady(vehicle.getPickupReady());
        vehicle.setCarId(vehicle.getCarId());
        vehicle.setModel(model);
        vehicle.setYear(castedYear);

        if (deleteRsvrtn != null) {
            vehicle.setReservedByUser(null);
            vehicle.setRentStartDate(null);
            vehicle.setRentEndDate(null);
            System.out.println("in delete reservation manager controller");
            vehicle.setRentReturnDate(null);
        } else {
            vehicle.setReservedByUser(vehicle.getReservedByUser());
            vehicle.setRentStartDate(vehicle.getRentStartDate());
            vehicle.setRentEndDate(vehicle.getRentEndDate());
            vehicle.setRentReturnDate(vehicle.getRentReturnDate());

        }

        if (deleteUsr != null) {
            System.out.println("in delete user manager controller");
            vehicle.setxUser(null);
            vehicle.setRentStartDate(null);
            vehicle.setRentEndDate(null);
            vehicle.setRentReturnDate(null);
        } else {
            System.out.println("at delete user manager controller null");
            vehicle.setxUser(vehicle.getxUser());
            vehicle.setRentStartDate(vehicle.getRentStartDate());
            vehicle.setRentEndDate(vehicle.getRentEndDate());
            vehicle.setRentReturnDate(vehicle.getRentReturnDate());
        }
        vehicle.setImagePath(vehicle.getImagePath());
        vehicleDAO.updateVehicle(vehicle);

        status.setComplete();

        return "Manager/Edited";
    }

    // delete all
    @GetMapping("/deleteall.htm")
	public String fetchDeleteall(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
			throws Exception {

		HttpSession session = request.getSession();


		System.out.println("IN delete method");

		String cid = request.getParameter("carId");
		


		int carId = Integer.parseInt(cid);
		

		


		Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);
		System.out.println("IN delete method" +carId);

		model.addAttribute(vehicle);
		System.out.println("IN delete method success" +carId);

		return "Manager/DeleteAll";
	}

	@PostMapping("/deleteall.htm")
	public String postDeleteall(SessionStatus status, VehicleDAO vehicleDAO, HttpServletRequest request,
			UserDAO userdao) throws Exception {

		System.out.println("post delete controller");
		HttpSession session = request.getSession();

		
		int carId = Integer.parseInt(request.getParameter("c1"));
		

		Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);

		vehicleDAO.deleteVehicle(vehicle);

		status.setComplete();

		return "Manager/Deleted";
		
	}
    

    // accept pickup
    @GetMapping("/pickup.htm")
    public String fetchPickupdetails(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
            throws Exception {

        HttpSession session = request.getSession();

        String usrEmail = request.getParameter("usrEmail");

        String carid = request.getParameter("carId");

        int carId = Integer.parseInt(carid);

        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);

        User user = userdao.fetchUsrByusrEmail(usrEmail);

        model.addAttribute("vehicle", vehicle);

        model.addAttribute("usrEmail", usrEmail);
        return "Manager/Pickup";

    }

    @PostMapping("/pickup.htm")
    public String postPickupdetails(SessionStatus status, VehicleDAO vehicleDAO, HttpServletRequest request,
            UserDAO userdao) throws Exception {
        HttpSession session = request.getSession();
        String usrEmail = request.getParameter("usrEmail");
        User user = userdao.fetchUsrByusrEmail(usrEmail);

        int carId = Integer.parseInt(request.getParameter("c4"));

        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(carId);
        vehicle.setImagePath(vehicle.getImagePath());
        vehicle.setRentStartDate(vehicle.getRentStartDate());
        vehicle.setRentEndDate(vehicle.getRentEndDate());
        vehicle.setRentReturnDate(vehicle.getRentReturnDate());
        vehicle.setPickupReady(false);
        vehicle.setReservedByUser(null);
        vehicle.setxUser(user);
        vehicle.setCarId(vehicle.getCarId());
        vehicle.setLicensePlate(vehicle.getLicensePlate());
        vehicle.setModel(vehicle.getModel());
        vehicle.setYear(vehicle.getYear());
        vehicleDAO.updateVehicle(vehicle);
        status.setComplete();
        System.out.println("pickup successfull");
        return "Manager/PickedUp";
    }

    //retrun vehicle
    @GetMapping("/returnvehicle.htm")
    public String fetchvehRtn(Model model, VehicleDAO vehicleDAO, HttpServletRequest request) throws Exception {

        HttpSession session = request.getSession();
        String usrEmail = request.getParameter("usrEmail");
        model.addAttribute("usrEmail", usrEmail);

        LinkedHashMap<Vehicle, String> vehiclespickedup = vehicleDAO.fetchVechilesInUse();

        if (vehiclespickedup != null) {
        }

        model.addAttribute("vehicles", vehiclespickedup);
        return "Manager/ReturnVehicle";

    }

    // accept return
    @GetMapping("/return.htm")
    public String fetchAcceptRtn(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
            throws Exception {
        HttpSession session = request.getSession();
        String usrEmail = request.getParameter("usrEmail");
        String id2 = request.getParameter("carId");
        System.out.println(id2 + "in get confrim return id2");
        int cId1 = Integer.parseInt(id2);
        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(cId1);
        User user = userdao.fetchUsrByusrEmail(usrEmail);
        request.setAttribute("vehicle", vehicle);
        request.setAttribute("usrEmail", usrEmail);

        return "Manager/Return";

    }

    @PostMapping("/return.htm")
    public String postAcceptRtn(SessionStatus status,
            VehicleDAO vehicleDAO, HttpServletRequest request, UserDAO userdao) throws Exception {

        HttpSession session = request.getSession();
        String usrEmail = request.getParameter("usrEmail");
        User user = userdao.fetchUsrByusrEmail(usrEmail);

        int cId1 = Integer.parseInt(request.getParameter("c5"));

        Vehicle vehicle = vehicleDAO.fetchVehiclesbyId(cId1);

        vehicle.setRentStartDate(null);
        vehicle.setRentEndDate(null);
        vehicle.setRentReturnDate(null);
        vehicle.setPickupReady(false);
        vehicle.setReservedByUser(null);
        vehicle.setxUser(null);
        vehicle.setCarId(vehicle.getCarId());
        vehicle.setLicensePlate(vehicle.getLicensePlate());
        vehicle.setModel(vehicle.getModel());
        vehicle.setYear(vehicle.getYear());
       
        vehicle.setImagePath(vehicle.getImagePath());

        vehicleDAO.updateVehicle(vehicle);

        status.setComplete();
        return "Manager/ReturnComplete";
    }

    // vehciles list
    @GetMapping("/vehicles.htm")
    public String fetchVehicles(Model model, VehicleDAO vehicleDAO, HttpServletRequest request) throws Exception {

        HttpSession session = request.getSession();
        System.out.println("in manager controller fetchall");
        List<Vehicle> vehicle = vehicleDAO.fetchAllVehicles();
        model.addAttribute("vehicle", vehicle);
        return "Manager/Vehicles";

    }

    // customer reservations
    @GetMapping("/vehiclereserve.htm")
    public String fetchVehicleResrvtns(Model model, VehicleDAO vehicleDAO, HttpServletRequest request, SessionStatus status)
            throws Exception {

        LinkedHashMap<Vehicle, String> vehcilesRsvd = vehicleDAO.fetchAllReservedVechiles();

        if (vehcilesRsvd != null) {
        }
        model.addAttribute("vehicles", vehcilesRsvd);
        return "Manager/VehicleReserve";

    }
}
