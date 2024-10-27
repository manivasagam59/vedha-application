from django.shortcuts import render,redirect
from modules.app import Users,UserDetail,Stores,StockManagement,ProductSupplier,StockBuying
from django.http import JsonResponse

# Create your views here.
# Login Checker function
def check_login(request):
    if (request.session.get("user_id") !=None or request.session.get("user_name") !=None) and request.session.get("user_role") =="stock manager" and request.session["store_name"] !=None:
        return True
    else:
        return False


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

    # Check Message available
    if "action_msg" in request.session:
        context["action_msg"]=request.session["action_msg"]
        del request.session["action_msg"]
    if "msg_code" in request.session:
        context["msg_code"]=request.session["msg_code"]
        del request.session["msg_code"]
    return context

# Stock management dashboard
def stock_management(request):
    if check_login(request):        
        context=getContext(request)
        context["active_page"]="dashboard"
        
        return render(request,"stock_dashboard.html",context)
    else:
        return redirect("/stock_manager_login")

# Stocks 
def stocks(request):
    if check_login(request):        
        context=getContext(request)
        context["active_page"]="stocks"
        sm=StockManagement(request.session["store_name"])
        ps=ProductSupplier(request.session["store_name"])

        # POST METHOD ACTIONS
        if request.method=="POST":

            if request.POST["action"]=="get_detail":
                response_json={}
                if request.POST["product_name"].strip()!="":
                    data=sm.get_stock_detail_by_product_name(request.POST["product_name"])
                    if data!=[]:
                        response_json["status"]="ok"
                        response_json["product_id"]="PRODUCT"+str(data[0])
                        response_json["product_name"]=data[1].capitalize()
                        response_json["buying_price"]=data[2]
                        response_json["price"]=data[3]
                        response_json["in_stock"]=data[4]
                        response_json["stock_notification_count"]=data[5]
                return JsonResponse(response_json)
                    

            if request.POST["action"]=="add":
                if request.POST["product_name"].strip()=="":
                    request.session["action_msg"]="Product name is required"
                    request.session["msg_code"]="no"
                elif request.POST["buying_date"] == "":
                    request.session["action_msg"]="Buying date is required"
                    request.session["msg_code"]="no"
                elif request.POST["supplier_name"].strip() == "":
                    request.session["action_msg"]="Supplier name is required"
                    request.session["msg_code"]="no"
                elif request.POST["buying_price"]!="" and int(request.POST["buying_price"]) == 0:
                    request.session["action_msg"]="Buying price is required"
                    request.session["msg_code"]="no"
                elif request.POST["selling_price"]!="" and int(request.POST["selling_price"]) == 0:
                    request.session["action_msg"]="Selling price is required"
                    request.session["msg_code"]="no"
                elif request.POST["buying_quantity"]!="" and int(request.POST["buying_quantity"]) == 0:
                    request.session["action_msg"]="Buying quantity is required"
                    request.session["msg_code"]="no"
                else:
                    stock_notified_count=0
                    stock_buy_obj=StockBuying(request.session["store_name"])
                    if request.POST["stock_notification_count"]!="":
                        stock_notified_count=int(request.POST["stock_notification_count"])

                    if request.POST["product_id"].strip()!="" and sm.check_stock_exists(request.POST["product_name"])==True:
                        prd_id=request.POST["product_id"][7:]
                        sm.update_all_stock_detail(prd_id,request.POST["product_name"],request.POST["buying_price"],request.POST["selling_price"],request.POST["buying_quantity"],stock_notified_count)
                        request.session["action_msg"]="Product stock updated"
                        request.session["msg_code"]="ok"
                    else:   
                        sm.add_stock(request.POST["product_name"],request.POST["buying_price"],request.POST["selling_price"],request.POST["buying_quantity"],stock_notified_count)
                        request.session["action_msg"]="Product added to stocks"
                        request.session["msg_code"]="ok"
                    
                    stock_buy_obj.purchase_new_product(request.POST["buying_date"],request.POST["supplier_name"],request.POST["product_name"],request.POST["buying_price"],request.POST["buying_quantity"])
            
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
                    sm.update_stock_basic(request.POST["product_id"],request.POST["product_name"],request.POST["price"],request.POST["min_stock"])
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

            return redirect("stocks")
        
        suppliers=ps.get_all_supplier_detail()
        suppliers_list=[i[1].capitalize() for i in suppliers]
        context["suppliers"]=suppliers_list
        stocks=sm.get_all_stocks()
        stocks=[{"id":i[0],"product_name":i[1].capitalize(),"buy_price":i[2], "price":i[3], "stock_quantity":i[4], "notification_at":i[5],"stock_price":i[3]*i[4]} for i in stocks]
        context["stocks"]=stocks
        context["total_stock_price"]=sm.get_total_sum()
        return render(request,"stocks.html",context)
    else:
        return redirect("/stock_manager_login")

# Dealers
def supplier(request):
    if check_login(request):        
        context=getContext(request)
        context["active_page"]="product_supplier"
        ps=ProductSupplier(request.session["store_name"])

        # POST METHOD ACTIONS
        if request.method=="POST":
            if request.POST["action"]=="add":
                if len(request.POST["supplier_name"])<=2:
                    request.session["action_msg"]="Supplier name is required"
                    request.session["msg_code"]="no"
                elif ps.check_supplier_exists(request.POST["supplier_name"]):
                    request.session["action_msg"]="Supplier name already exists"
                    request.session["msg_code"]="no"
                elif request.POST["contact_number"] == "":
                    request.session["action_msg"]="Contact number is required"
                    request.session["msg_code"]="no"
                elif len(request.POST["contact_number"]) != 10:
                    request.session["action_msg"]="Invalid contact number detected"
                    request.session["msg_code"]="no"
                else:
                    ps.add_supplier(request.POST["supplier_name"],request.POST["contact_number"],request.POST["alternate_number"])
                    request.session["action_msg"]="New Supplier is added"
                    request.session["msg_code"]="ok"
            
            elif request.POST["action"]=="update":
                if request.POST["supplier_id"]=="":
                    request.session["action_msg"]="Something went wrong, try again"
                    request.session["msg_code"]="no"
                elif len(request.POST["supplier_name"])<=2:
                    request.session["action_msg"]="Supplier name is required"
                    request.session["msg_code"]="no"
                elif ps.check_supplier_exists(request.POST["supplier_name"]):
                    request.session["action_msg"]="Supplier name already exists"
                    request.session["msg_code"]="no"
                elif request.POST["contact_number"] == "":
                    request.session["action_msg"]="Contact number is required"
                    request.session["msg_code"]="no"
                elif len(request.POST["contact_number"]) != 10:
                    request.session["action_msg"]="Invalid contact number detected"
                    request.session["msg_code"]="no"
                else:
                    id=int(request.POST["supplier_id"][8:])
                    ps.update_supplier(id,request.POST["supplier_name"],request.POST["contact_number"],request.POST["alternate_number"])
                    request.session["action_msg"]="Supplier detail updated successfully"
                    request.session["msg_code"]="ok"
            
            elif request.POST["action"]=="delete":
                if request.POST["supplier_id"]=="":
                    request.session["action_msg"]="Something went wrong, try again"
                    request.session["msg_code"]="no"
                else:
                    id=int(request.POST["supplier_id"][8:])
                    ps.delete_supplier(id)
                    request.session["action_msg"]="Supplier deleted successfully"
                    request.session["msg_code"]="ok"

            return redirect("supplier")
        
        context["suppliers"]=[]
        temp=ps.get_all_supplier_detail()
        for i in temp:
            context["suppliers"].append({"id":"SUPPLIER"+str(i[0]),"name":i[1].capitalize(),"contact_no":i[2],"alternate_no":i[3]})
        return render(request,"supplier.html",context)
    else:
        return redirect("/stock_manager_login")

# Buying history
def buying_history(request):
    if check_login(request):        
        context=getContext(request)
        context["active_page"]="buying_history"
        purchase_book_obj=StockBuying(request.session["store_name"])
        context["purchase_details"]=purchase_book_obj.get_all_purchase_detail()

        return render(request,"buying_history.html",context)
    else:
        return redirect("/stock_manager_login")

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
            
            return redirect("stock_manager_emp_edit")

        profile_images=["male_1.png","male_2.png","male_3.png","male_4.png","male_5.png","female_1.png","female_2.png","female_3.png","female_4.png","female_5.png"]
        context=getContext(request)
        context["profile_images"]=profile_images
        context["user_name"]=request.session["user_name"].capitalize()
        context["user_contact_no"]=detail[1]
        context["user_profile_img"]=detail[2]
        return render(request,"stock_manager_emp_profile_edit.html",context)
    else:
        return redirect("/login")
