import datetime
import json
from django.shortcuts import render,redirect
from modules.app import Users,UserDetail,Stores,MobileRecharge,DthRecharge,OnlineService,ProductSales,StockManagement
from modules.settings import get_store_dir
from django.http import JsonResponse

# =====================================================================================
# Login Checker function
def check_login(request):
    if (request.session.get("user_id") !=None or request.session.get("user_name") !=None) and request.session.get("user_role") =="employee" and request.session["store_name"] !=None:
        return True
    else:
        return False


# Service availability Checker
def check_service(request,service):
    store_object=Stores()
    store_detail=store_object.get_store(request.session["store_name"])
    all_services={"mobile_recharge":store_detail[1],"dth_recharge":store_detail[2],"online_services":store_detail[3],"product_sale":store_detail[4]}
    return all_services[service]
        
    
# Generate required data for context 
def getContext(request):
    context={}
    user=Users()
    user_detail_obj=UserDetail()
    store_object=Stores()
    user_id=user.get_user_id_by_name(request.session["user_name"])
    user_detail=user_detail_obj.get_user_detail(user_id)
    store_detail=store_object.get_store(request.session["store_name"])
    context["user_name"]=request.session["user_name"].capitalize()
    context["store_name"]=request.session["store_name"].capitalize()
    context["user_img"]=user_detail[2]

    context["mb_recharge"]=store_detail[1]
    context["dth_recharge"]=store_detail[2]
    context["online_services"]=store_detail[3]
    context["product_sales"]=store_detail[4]

    # Check Message available
    if "action_msg" in request.session:
        context["action_msg"]=request.session["action_msg"]
        del request.session["action_msg"]
    if "msg_code" in request.session:
        context["msg_code"]=request.session["msg_code"]
        del request.session["msg_code"]
    return context
# =====================================================================================

# Store Dashboard View 
def store_dashboard(request):
    if check_login(request):
        context=getContext(request)
        context["active_page"]="dashboard"

        store_object=Stores()
        store_detail=store_object.get_store(request.session["store_name"])
        date=datetime.datetime.now()
        context["current_month"]=date.strftime("%B")
        context["current_year"]=date.strftime("%Y")


        totals={"mb_total":0,"dth_total":0,"os_total":0,"ps_total":0,"all_total":0}
        reports=[]
        for day in range(1,date.day+1):
            report_data={"date":"","mb":0,"dth":0,"os":0,"ps":0,"total":0}
            report_data["date"]=str(day)+date.strftime(" %b %Y")
            if store_detail[1]:
                mbr_obj=MobileRecharge(request.session["store_name"],[date.year,date.month,day])
                sum=mbr_obj.get_total_sum()
                report_data["mb"]=sum
                totals["mb_total"]+=sum
            if store_detail[2]:
                dth_obj=DthRecharge(request.session["store_name"],[date.year,date.month,day])
                sum=dth_obj.get_total_sum()
                report_data["dth"]=sum
                totals["dth_total"]+=sum
            if store_detail[3]:
                os_obj=OnlineService(request.session["store_name"],[date.year,date.month,day])
                sum=os_obj.get_total_sum()
                report_data["os"]=sum
                totals["os_total"]+=sum
            if store_detail[4]:
                ps_obj=ProductSales(request.session["store_name"],[date.year,date.month,day])
                sum=ps_obj.get_total_sum()
                report_data["ps"]=sum
                totals["ps_total"]+=sum
            report_data["total"]=report_data["mb"]+report_data["dth"]+report_data["os"]+report_data["ps"]
            reports.append(report_data)
        
        totals["all_total"]=totals["mb_total"]+totals["dth_total"]+totals["os_total"]+totals["ps_total"]
        context["monthly_overview"]=totals
        context["monthly_reports"]=reports


        return render(request,"dashboard.html",context)
    else:
        return redirect("/login")


# Mobile Recharge View
def mobile_recharge(request):
    if check_login(request):
        if check_service(request,"mobile_recharge")==False:
            return redirect("store_dashboard")
        if request.method == "POST":
            if request.POST["mobile_no"]=="":
                request.session["action_msg"]="Mobile number required"
                request.session["msg_code"]="no"
            elif len(request.POST["mobile_no"])!=10:
                request.session["action_msg"]="Mobile number must be 10 digit"
                request.session["msg_code"]="no"
            elif request.POST["operator_name"]=="":
                request.session["action_msg"]="Operator is required"
                request.session["msg_code"]="no"
            elif request.POST["amount"]=="" or request.POST["amount"]==0:
                request.session["action_msg"]="Invalid recharge amount"
                request.session["msg_code"]="no"
            else:
                request.session["action_msg"]="Recharge amount paid Successfully"
                request.session["msg_code"]="ok"
                date=datetime.datetime.now()
                mb_recharge_obj=MobileRecharge(request.session["store_name"],[date.year,date.month,date.day])
                mb_recharge_obj.insert(request.POST["mobile_no"],request.POST["operator_name"],request.POST["amount"])
            
            return redirect("mobile_recharge")

        context=getContext(request)
        context["active_page"]="mobile_recharge"
        return render(request,"mobile_recharge.html",context)
    else:
        return redirect("/login")


# Dth Recharge View 
def dth_recharge(request):
    if check_login(request):
        if check_service(request,"dth_recharge")==False:
            return redirect("store_dashboard")
        if request.method=="POST":
            if request.POST["dth_no"]=="":
                request.session["action_msg"]="DTH number required"
                request.session["msg_code"]="no"
            elif len(request.POST["dth_no"])<=5:
                request.session["action_msg"]="Invalid DTH number"
                request.session["msg_code"]="no"
            elif request.POST["operator_name"]=="":
                request.session["action_msg"]="Operator is required"
                request.session["msg_code"]="no"
            elif request.POST["amount"]=="" or request.POST["amount"]==0:
                request.session["action_msg"]="Invalid recharge amount"
                request.session["msg_code"]="no"
            else:
                request.session["action_msg"]="Recharge amount paid Successfully"
                request.session["msg_code"]="ok"
                date=datetime.datetime.now()
                dth_recharge_obj=DthRecharge(request.session["store_name"],[date.year,date.month,date.day])
                dth_recharge_obj.insert(request.POST["dth_no"],request.POST["operator_name"],request.POST["amount"])
            
            return redirect("dth_recharge")

        context=getContext(request)
        context["active_page"]="dth_recharge"
        return render(request,"dth_recharge.html",context)
    else:
        return redirect("/login")


# Online Services view
def online_services(request):
    if check_login(request):
        if check_service(request,"online_services")==False:
            return redirect("store_dashboard")
        if request.method=="POST":
            service_name=request.POST["service_name"]
            if request.POST["service_name"]=="":
                request.session["action_msg"]="DTH number required"
                request.session["msg_code"]="no"
            elif request.POST["service_name"]=="Other" and len(request.POST["service-description"])<8:
                service_name=request.POST["service-description"]
                request.session["action_msg"]="Description is required, it must be greater than 8 characters"
                request.session["msg_code"]="no"
            elif request.POST["amount"]=="" or request.POST["amount"]==0:
                request.session["action_msg"]="Invalid recharge amount"
                request.session["msg_code"]="no"
            else:
                request.session["action_msg"]="Service amount paid Successfully"
                request.session["msg_code"]="ok"
                date=datetime.datetime.now()
                online_service_obj=OnlineService(request.session["store_name"],[date.year,date.month,date.day])
                online_service_obj.insert(service_name,request.POST["amount"])

            return redirect("online_services")
        
        context=getContext(request)
        context["active_page"]="online_services"
        return render(request,"online_services.html",context)
    else:
        return redirect("/login")


# Product sale view
def product_sales(request):
    if check_login(request):
        if check_service(request,"product_sale")==False:
            return redirect("store_dashboard")
        
        context=getContext(request)
        context["active_page"]="product_sales"
        date=datetime.datetime.now()
        sm=StockManagement(request.session["store_name"])
        ps=ProductSales(request.session["store_name"],[date.year,date.month,date.day])
        
        if request.method=="POST":
            if "product_id" in request.POST:
                result=sm.get_stock_detail_by_id(request.POST["product_id"])
                send_data={"rate":result[1],"max_quantity":result[2]}
                return JsonResponse(send_data)
            elif "purchase_list" in request.POST:
                data=json.loads(request.POST["purchase_list"])
                if data==[]:
                    request.session["action_msg"]="No items Purchased, please fill"
                    request.session["msg_code"]="no"
                else:
                    amount=0
                    for i in data:
                        sm.purchase_product_by_id(i["id"],i["quantity"])
                        amount+=(i["quantity"]*i["rate"])
                    ps.insert(request.POST["purchase_list"],amount)
                    request.session["action_msg"]="Amount successfully paid."
                    request.session["msg_code"]="ok"

        products=sm.get_all_products()
        products=[{"id":i[0],"product_name":i[1].capitalize()} for i in products]
        context["products"]=products
        return render(request,"product_sales.html",context)
    
    else:
        return redirect("/login")

# Bill view
def bill_view(request,id):
    if check_login(request):
        if check_service(request,"product_sale")==False:
            return redirect("store_dashboard")
        
        context={"title":id}
        context["bill"]=[]
        context["total"]=""
        
        bill=[]
        if len(id)>=15:
            year=int(id[6:10])
            month=int(id[10:12])
            day=int(id[12:14])
            billing_id=int(id[14:])
            sm=ProductSales(request.session["store_name"],[year,month,day])
            data=sm.get_bill_by_id(billing_id)
            if data!=[]:
                temp=json.loads(data[0])
                bill=[{"product_name":i["product_name"].capitalize(),"rate":i["rate"],"quantity":i["quantity"],"total":i["rate"]*i["quantity"]} for i in temp ]
            context["bill"]=bill
            context["total"]=data[1]
        


        return render(request,"bill_view.html",context)

# Stock management app
def stock_management(request):
    if check_login(request):
        if check_service(request,"product_sale")==False:
            return redirect("store_dashboard")
        
        context=getContext(request)
        context["active_page"]="stock_management"
        sm=StockManagement(request.session["store_name"])

        # POST METHOD ACTIONS
        if request.method=="POST":
            if request.POST["action"]=="add":
                if len(request.POST["product_name"])<=2:
                    request.session["action_msg"]="Product name is required"
                    request.session["msg_code"]="no"
                elif int(request.POST["price"]) == 0:
                    request.session["action_msg"]="Price is required"
                    request.session["msg_code"]="no"
                elif sm.check_stock_exists(request.POST["product_name"])==True:
                    request.session["action_msg"]="Product name already found, try with another name"
                    request.session["msg_code"]="no"
                else:
                    sm.add_stock(request.POST["product_name"],request.POST["price"],request.POST["quantity"],request.POST["min_stock"])
                    request.session["action_msg"]="Product added to stocks"
                    request.session["msg_code"]="ok"
            
            elif request.POST["action"]=="update":
                if request.POST["product_id"]=="":
                    request.session["action_msg"]="Something went wrong, try again"
                    request.session["msg_code"]="no"
                elif len(request.POST["product_name"])<=2:
                    request.session["action_msg"]="Product name is required"
                    request.session["msg_code"]="no"
                elif int(request.POST["price"]) == 0:
                    request.session["action_msg"]="Price is required"
                    request.session["msg_code"]="no"
                elif sm.check_stock_update_exists(request.POST["product_id"],request.POST["product_name"])==True:
                    request.session["action_msg"]="Product name already found, try with another name"
                    request.session["msg_code"]="no"
                else:
                    sm.update_stock(request.POST["product_id"],request.POST["product_name"],request.POST["price"],request.POST["quantity"],request.POST["min_stock"])
                    request.session["action_msg"]="Product detail updated successfully"
                    request.session["msg_code"]="ok"
            elif request.POST["action"]=="delete":
                if request.POST["product_id"]=="":
                    request.session["action_msg"]="Something went wrong, try again"
                    request.session["msg_code"]="no"
                else:
                    sm.delete_stock(request.POST["product_id"])
                    request.session["action_msg"]="Product deleted successfully"
                    request.session["msg_code"]="ok"

            return redirect("stock_management")
        
        stocks=sm.get_all_stocks()
        stocks=[{"id":i[0],"product_name":i[1].capitalize(), "price":i[2], "stock_quantity":i[3], "notification_at":i[4],"stock_price":i[2]*i[3]} for i in stocks]
        context["stocks"]=stocks
        context["total_stock_price"]=sm.get_total_sum()
        return render(request,"stock_management.html",context)
    else:
        return redirect("/login")

# Online Services view
def accounting(request):
    if check_login(request):
        context=getContext(request)
        context["active_page"]="accounting"

        if request.method=="GET":

            d=datetime.datetime.now()
            date_format="{:2d}-{:2d}-{:2d}".format(d.year,d.month,d.day)
            date_format=date_format.replace(" ","0")       
            context["max_date"]=date_format

            # Read info json for setting min_date
            store=Stores()
            store_id=store.get_store_id_by_name(request.session["store_name"])
            store_path=get_store_dir(store_id)
            with open(store_path+"\\info.json","r") as file:
                file_data=file.read()
            json_data=json.loads(file_data)
            context["min_date"]=json_data["store_creation_date"]

            if "report_date" in request.GET and "service_name" in request.GET:
                service_name=request.GET["service_name"]
                date=request.GET["report_date"].split("-")
                    
                context["select_date"]=request.GET["report_date"]
                context["select_service"]=service_name
                    
                
                if service_name =="Mobile recharge":
                    mb_r_obj=MobileRecharge(request.session["store_name"],date)
                    data_list=mb_r_obj.select()
                    context["view"]="mobile_recharge"
                    context["total_amount"]=mb_r_obj.get_total_sum()
                    context["data_list"]=data_list
                elif service_name =="Dth recharge":
                    dth_r_obj=DthRecharge(request.session["store_name"],date)
                    data_list=dth_r_obj.select()
                    context["view"]="dth_recharge"
                    context["total_amount"]=dth_r_obj.get_total_sum()
                    context["data_list"]=data_list
                elif service_name =="Online service":
                    os_obj=OnlineService(request.session["store_name"],date)
                    data_list=os_obj.select()
                    context["view"]="services"
                    context["total_amount"]=os_obj.get_total_sum()
                    context["data_list"]=data_list
                elif service_name =="Product sale":
                    os_obj=ProductSales(request.session["store_name"],date)
                    data=os_obj.select()
                    data_list=[{"id":"BILLNO"+d.strftime("%Y%m%d")+str(i[0]),"amount":i[1]} for i in data]
                    context["view"]="product_sale"
                    context["total_amount"]=os_obj.get_total_sum()
                    context["data_list"]=data_list

        return render(request,"accounting.html",context)
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
            
            return redirect("emp_edit_profile")

        profile_images=["male_1.png","male_2.png","male_3.png","male_4.png","male_5.png","female_1.png","female_2.png","female_3.png","female_4.png","female_5.png"]
        context=getContext(request)
        context["profile_images"]=profile_images
        context["user_name"]=request.session["user_name"].capitalize()
        context["user_contact_no"]=detail[1]
        context["user_profile_img"]=detail[2]
        return render(request,"emp_profile_edit.html",context)
    else:
        return redirect("/login")
