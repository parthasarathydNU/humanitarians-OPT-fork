package com.vehicle.controller;

import com.vehicle.dao.LoginDAO;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.support.SessionStatus;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import com.vehicle.dao.UserDAO;
import com.vehicle.pojo.User;

@Controller
public class LoginController {
    
     //signin
    @RequestMapping("/")
    public String initializeForm() {
        return "redirect:/login.htm";
    }
    
    
//user validation check
    
     @GetMapping("/login.htm")
    public String fetchSignIn(Model model, User user) {
        return "login";
    }
    
    @PostMapping("/login.htm")
    public String userValidation(@ModelAttribute("user") User user, BindingResult result, SessionStatus status,
            HttpServletRequest req, LoginDAO logindao, Model model) {
        HttpSession session = req.getSession();
        String usrEmail = req.getParameter("usrEmail");
        String usrPassword = req.getParameter("usrPassword");

        boolean checkCustomer = false;
	boolean checkAdmin = false;
        boolean checkEmp = false;
        try {

            checkCustomer = logindao.checkCustmer(usrEmail, usrPassword);
            System.out.println("customer validation check completed");
	     checkAdmin = logindao.checkAdmin(usrEmail, usrPassword);
            System.out.println("admin validation completed");
            checkEmp = logindao.checkEmployee(usrEmail, usrPassword);
            System.out.println("emp validation check completed");
        } catch (Exception e) {
            System.out.println("exception in customer/manager validation DAO ");
        }

        if (checkCustomer) {
            System.out.println(" customer-User");
            session.setAttribute("usrEmail", usrEmail);
            return "customer/cusHome";

        } else if (checkEmp) {
            System.out.println("Manager-User");
            session.setAttribute("usrEmail", usrEmail);
            model.addAttribute(usrEmail);
            return "Manager/ManagerHome";
        }
        
        else if (checkAdmin) {
            System.out.println("admin-user");
            session.setAttribute("usrEmail", usrEmail);
            model.addAttribute(usrEmail);
            return "admin/adminHome";
        }
        
        

        String excep = "enter valid userEmail/user Pwd";
        model.addAttribute("error", excep);
        return "login";
    }
//signout

    @GetMapping("/signout.htm")
    public String signout(HttpSession session) {
        session.invalidate();
        return "redirect:/login.htm";
    }
//new user signup?

    @GetMapping("/register.htm")
    public String fetchNewUser(ModelMap model, User user) {
        model.addAttribute("user", user);
        return "Registration";
    }

    @PostMapping("/register.htm")
    public String addNewUser(@ModelAttribute("user") User newUser, HttpServletRequest request, BindingResult result, SessionStatus status,
            UserDAO userdao, Model model) throws Exception {
        HttpSession session = request.getSession();
        User existingUser = userdao.fetchUsrByusrEmail(newUser.getUsrEmail());
        if (existingUser != null) {
            String excep = "user email already exits!!";
            model.addAttribute("error", excep);
            return "Registration";
        }
        userdao.saveUser(newUser);
        if (result.hasErrors()) {
            System.out.println("faced error during registartion");
            return "Registration";
        }
        System.out.println("before login success is returned");
        status.setComplete();
        System.out.println("new user registered");
        return "loginSuccess";
    }

}
