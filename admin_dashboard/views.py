from django.shortcuts import render,redirect
from django.http import HttpResponse
from modules.app import Users,Stores,UserDetail

# ==========================================================================================================
# Login Checker function
def check_login(request):
    if (request.session.get("user_id") !=None or request.session.get("user_name") !=None) and request.session.get("user_role")=="admin":
        return True
    else:
        return False
    
# Generate required data for context 
def getContext(request):
    context={}
    user=Users()
    user_detail_obj=UserDetail()
    user_id=user.get_user_id_by_name(request.session["user_name"])
    user_detail=user_detail_obj.get_user_detail(user_id)
    context["user_name"]=request.session["user_name"].capitalize()
    context["user_img"]=user_detail[2]
    if "action_msg" in request.session:
        context["action_msg"]=request.session["action_msg"]
        del request.session["action_msg"]
    if "msg_code" in request.session:
        context["msg_code"]=request.session["msg_code"]
        del request.session["msg_code"]
    return context

# ===========================================================================================================

# Admin Dashboard view
def admin_dashboard(request):
    if check_login(request):
        store=Stores()
        user=Users()
        user_detail_obj=UserDetail()
        store_data=store.get_all_store_data()
        user_data=[]
        users_list=user.get_all_users()
        for u in users_list:
            temp=[]
            temp.append(u)
            user_id=user.get_user_id_by_name(u)
            detail=user_detail_obj.get_user_detail(user_id)
            temp.append(detail[0].capitalize())
            temp.append(detail[1])
            user_data.append(temp)
            
        context=getContext(request)
        context["active_page"]="dashboard"
        context["stores"]=store_data
        context["users"]=user_data
        return render(request,"admin_dashboard.html",context)
    else:
        return redirect("/login")


# Employee create view
def create_employee(request):
    if check_login(request):
        if request.method=="POST":
            user=Users()
            user_detail=UserDetail()
            
            # Validation =============================
            if request.POST["employee_name"] == "":
                request.session["action_msg"]="Employee name is required"
                request.session["msg_code"]="no"
            elif request.POST["gender"] == "":
                request.session["action_msg"]="Gender is required"
                request.session["msg_code"]="no"
            elif user.user_exists(request.POST["employee_name"]):
                request.session["action_msg"]="Employee already exists.\nTry with another name."
                request.session["msg_code"]="no" 
            else:
                user.create_user(request.POST["employee_name"],"employee","123456")
                user_id=user.get_user_id_by_name(request.POST["employee_name"])
                prof_img=""
                if request.POST["gender"]=="Male":
                    prof_img="male_1.png"
                elif request.POST["gender"]=="Female":
                    prof_img="female_1.png"
                user_detail.add_detail(user_id,request.POST["gender"],request.POST["contact_no"],prof_img)
                request.session["action_msg"]="Employee created successfully."
                request.session["msg_code"]="ok"
            return redirect("create_employee")
        context=getContext(request)
        context["active_page"]="add_employee"
        return render(request,"create_employee.html",context)
    else:
        return redirect("/login")


# remove employee view
def remove_employee(request):
    if check_login(request):
        user=Users()

        # POST Method action
        if request.method=="POST":
            # Validate ===================================
            if request.POST["employee_name"] =="":
                request.session["action_msg"]="Employee name is required"
                request.session["msg_code"]="no"
            elif "confirm" not in request.POST:
                request.session["action_msg"]="Please confirm deletion"
                request.session["msg_code"]="no"
            else:
                user.delete_user(request.POST["employee_name"])
                request.session["action_msg"]="Employee deleted successfully"
                request.session["msg_code"]="ok"
            return redirect("remove_employee")
        
        employees_list=user.get_all_users()
        employees_list=[i.capitalize() for i in employees_list]
        context=getContext(request)
        context["active_page"]="remove_employee"
        context["employees_list"]=employees_list
        return render(request,"remove_employee.html",context)
    else:
        return redirect("/login")


# Create store view
def create_store(request):
    if check_login(request):
        if request.method=="POST":
            store=Stores()
            # Validation ================================
            if request.POST.get("store_name")=="":
                request.session["action_msg"]="Store name is required"
                request.session["msg_code"]="no"
            elif store.check_store_exists(request.POST["store_name"]):
                request.session["action_msg"]="Store already exists.\n Try another name"
                request.session["msg_code"]="no"
            else:
                # Parsing data from form
                dth_recharge=False
                mobile_recharge=False
                online_service=False
                product_sale=False
                if "dth_recharge" in request.POST:
                    dth_recharge=True
                if "mobile_recharge" in request.POST:
                    mobile_recharge=True
                if "online_service" in request.POST:
                    online_service=True
                if "product_sale" in request.POST:
                    product_sale=True
                store.create_store(request.POST["store_name"],mobile_recharge,dth_recharge,online_service,product_sale)
                request.session["action_msg"]="Store created successfully"
                request.session["msg_code"]="ok"

            return redirect("create_store")
        
        context=getContext(request)
        context["active_page"]="create_store"
        return render(request,"create_store.html",context)
    else:
        return redirect("/login")


# Edit store view
def edit_store(request):
    if check_login(request):
        store=Stores()
        stores_list=store.get_stores_list()
        stores_list=[i.capitalize() for i in stores_list]
        context=getContext(request)
        context["active_page"]="edit_store"
        context["stores_list"]=stores_list
        
        # Form Post Method Actions
        if request.method=="POST":
            # Validation
            if request.POST.get("selected_store")=="":
                request.session["action_msg"]="Choose store to edit"
                request.session["msg_code"]="no"
            elif request.POST.get("store_new_name")=="":
                request.session["action_msg"]="Store name is required"
                request.session["msg_code"]="no"
            elif store.check_store_exists(request.POST["store_new_name"]) and request.POST["store_new_name"]!=request.POST["selected_store"]:
                request.session["action_msg"]="Store already exists.\n Try another name"
                request.session["msg_code"]="no"
            elif "changes-confirmation" not in request.POST:
                request.session["action_msg"]="Changes confirmation required"
                request.session["msg_code"]="no"
            else:
                # Parsing data from form
                dth_recharge=False
                mobile_recharge=False
                online_service=False
                product_sale=False
                # print(request.POST)
                if "dth_recharge" in request.POST:
                    dth_recharge=True
                if "mobile_recharge" in request.POST:
                    mobile_recharge=True
                if "online_service" in request.POST:
                    online_service=True
                if "product_sale" in request.POST:
                    product_sale=True
                store.edit_store(request.POST["selected_store"],request.POST["store_new_name"],mobile_recharge,dth_recharge,online_service,product_sale)
                request.session["action_msg"]="Store detail and services updated successfully"
                request.session["msg_code"]="ok"
            return redirect("edit_store")

        # Form Get Method Action
        if request.method=="GET" and "store_name" in request.GET:
            stores_data=store.get_store(request.GET["store_name"])
            context["selected_store_name"]=request.GET["store_name"]
            context["mbr_available"]=stores_data[1]
            context["dth_available"]=stores_data[2]
            context["os_Available"]=stores_data[3]
            context["ps_available"]=stores_data[4]    

        return render(request,"edit_store.html",context)
    else:
        return redirect("/login")


# Delete store view
def delete_store(request):
    if check_login(request):
        store=Stores()
        

        # Perform Post action
        if request.method=="POST":
                # Validation ======================================
            if request.POST.get("store_name")=="":
                request.session["action_msg"]="Choose store to delete"
                request.session["msg_code"]="no"
            elif "deletion-confirmation" not in request.POST:
                request.session["action_msg"]="Confirm store deletion"
                request.session["msg_code"]="no"
            else:
                store.delete_store(request.POST["store_name"])
                request.session["action_msg"]="Store deleted successfully."
                request.session["msg_code"]="ok" 
            return redirect("delete_store")
        
        stores_list=store.get_stores_list()
        context=getContext(request)
        context["active_page"]="delete_store"
        context["stores_list"]=stores_list
        return render(request,"delete_store.html",context)
    else:
        return redirect("/login")


# Edit profile view
def edit_profile(request):
    if check_login(request):
        user=Users()
        user_detail_obj=UserDetail()
        user_id=user.get_user_id_by_name(request.session["user_name"])
        detail=user_detail_obj.get_user_detail(user_id)
        
        # Perform POST action
        if request.method=="POST":
            if request.POST["form_type"] == "profile_edit":
                if request.POST["profile-img"]=="":
                    request.session["action_msg"]="No Profile image is selected"
                    request.session["msg_code"]="no"
                else:
                    user_detail_obj.update_detail(user_id,detail[0],request.POST["contact-no"],request.POST["profile-img"])
                    request.session["action_msg"]="Changes updated successfully"
                    request.session["msg_code"]="ok"
            elif request.POST["form_type"] == "password_edit":
                if request.POST["curr_pass"]=="" or  request.POST["new_pass"]=="" or  request.POST["conf_pass"]=="":
                    request.session["action_msg"]="Some field are empty in password changing, please fill it."
                    request.session["msg_code"]="no"
                elif request.POST["new_pass"] != request.POST["conf_pass"]:
                    request.session["action_msg"]="Confirm password not match"
                    request.session["msg_code"]="no"
                else:
                    user.edit_password(request.session["user_name"],request.POST["new_pass"],request.POST["curr_pass"])
                    request.session["action_msg"]="Password changed Successfully"
                    request.session["msg_code"]="ok"
            
            return redirect("edit_profile")

        profile_images=["male_1.png","male_2.png","male_3.png","male_4.png","male_5.png","female_1.png","female_2.png","female_3.png","female_4.png","female_5.png"]
        context=getContext(request)
        context["profile_images"]=profile_images
        context["user_name"]=request.session["user_name"].capitalize()
        context["user_contact_no"]=detail[1]
        context["user_profile_img"]=detail[2]
        return render(request,"profile_edit.html",context)
    else:
        return redirect("/login")
    
