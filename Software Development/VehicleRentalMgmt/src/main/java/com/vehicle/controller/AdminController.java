package com.vehicle.controller;

import com.vehicle.dao.UserDAO;
import com.vehicle.dao.VehicleDAO;
import com.vehicle.pojo.User;
import com.vehicle.pojo.Vehicle;
import java.util.List;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.support.SessionStatus;

@Controller
public class AdminController {

    // admin home page
    @GetMapping("/adminhome.htm")
    public String fetchAdminHomeView(Model model, HttpServletRequest req) {
        return "admin/adminHome";

    }
//list all available users

    @GetMapping("/listofusrs.htm")
    public String fetchUsers(Model model, VehicleDAO vehicleDAO, UserDAO userdao, HttpServletRequest request)
            throws Exception {
    	
    	System.out.println("Before users are fetched");
    	
        List<User> availableUsers = userdao.fetchEveryUsr();
    	System.out.println("After users are fetched size == " + availableUsers.size());

        model.addAttribute("user",availableUsers);
        return "admin/ListofUsrs";

    }

    //modify user details
    @GetMapping("/usermodify.htm")
    public String fetchModifyUsers(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
            throws Exception {

        HttpSession session = request.getSession();

        String usrid = request.getParameter("usrId");
        int castusrid = Integer.parseInt(usrid);

        User user1 = userdao.fetchUsrById(castusrid);

        model.addAttribute("user", user1);
        return "admin/userModify";

    }

    @PostMapping("/usermodify.htm")

    public String ModifyUsersPost(SessionStatus status, VehicleDAO vehicleDAO, HttpServletRequest request, UserDAO userdao, Model model)
            throws Exception {

        HttpSession session = request.getSession();

        int cid = Integer.parseInt(request.getParameter("uid2"));

        User user2 = userdao.fetchUsrById(cid);

        String homeAddr = request.getParameter("userAddress");
        String phonenum = request.getParameter("userPhonenum");

        user2.setUsrId(user2.getUsrId());
        user2.setName(user2.getName());
        user2.setUsrPassword(user2.getUsrPassword());
        user2.setTitle(user2.getTitle());
        user2.setUserAddress(homeAddr);
        user2.setUserPhonenum(phonenum);

        userdao.updateUser(user2);
        return "admin/userModified";

    }
//delete list of users

    @GetMapping("/userdelete.htm")
    public String fetchDeleteUsers(Model model, HttpServletRequest request, VehicleDAO vehicleDAO, UserDAO userdao)
            throws Exception {

        HttpSession session = request.getSession();

        String usrid1 = request.getParameter("usrId");
        int castusrid1 = Integer.parseInt(usrid1);

        User userDelete = userdao.fetchUsrById(castusrid1);
        model.addAttribute("user", userDelete);
        return "admin/userDelete";

    }

    @PostMapping("/userdelete.htm")

    public String postDeleteUsers(SessionStatus status, VehicleDAO vehicleDAO, HttpServletRequest request, UserDAO userdao, BindingResult result)
            throws Exception {
        HttpSession session = request.getSession();

        int cid1 = Integer.parseInt(request.getParameter("usrdel"));
        User userdel = userdao.fetchUsrById(cid1);
        if (userdel != null) {
            System.out.println("got user");
        }

        List<Vehicle> vehiclesCurrentlyInUse = vehicleDAO.fetchVechUsingbyUsr(userdel);
        for (Vehicle vehicle : vehiclesCurrentlyInUse) {
            vehicle.setxUser(null);
            vehicle.setRentStartDate(null);
            vehicle.setRentEndDate(null);
            vehicle.setRentReturnDate(null);
            vehicleDAO.updateVehicle(vehicle);
        }

        List<Vehicle> vehiclesrsvd = vehicleDAO.fetchReservedVehicleofUsr(userdel);
        for (Vehicle vehicle : vehiclesrsvd) {
            vehicle.setReservedByUser(null);
            vehicle.setRentStartDate(null);
            vehicle.setRentEndDate(null);
            vehicle.setRentReturnDate(null);
            vehicleDAO.updateVehicle(vehicle);

        }
        userdao.deleteUser(userdel);

        if (result.hasErrors()) {
            List<FieldError> errors = result.getFieldErrors();
            for (FieldError error : errors) {
                System.out.println(error.getObjectName() + " - " + error.getDefaultMessage());
            }
            return "admin/ListofUsrs";
        }
        status.setComplete();

        return "admin/userDeleted";
    }

}
