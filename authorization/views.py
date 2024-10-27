from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from modules.app import Users,Stores


def getContext(request):
    context={"error":""}
    if "error" in request.session:
        context["error"]=request.session.get("error")
        del request.session["error"]
    return context

def home(request):
    return redirect("/login")

def login(request):
    if request.method=="POST":
        users=Users()   
        result=users.check_authorization(request.POST["username"],request.POST["password"],"employee")
        if request.POST["store"]=="":
            request.session["error"]="Store field is required to login"
            return redirect("/login")
        elif result:
            user_id=users.get_user_id_by_name(request.POST["username"])
            request.session["user_id"]=user_id
            request.session["user_role"]="employee"
            request.session["user_name"]=request.POST["username"]
            request.session["store_name"]=request.POST["store"]
            return redirect("/dashboard")
        else:
            request.session["error"]="Invalid user name or password"
            return redirect("/login")
    store_obj=Stores()
    stores_list=store_obj.get_stores_list()
    context=getContext(request)
    context["stores_list"]=[i.capitalize() for i in stores_list]
    return render(request,"store_login.html",context)
    
def admin_login(request):
    if request.method=="POST":
        users=Users()  
        result=users.check_authorization(request.POST["username"],request.POST["password"],"admin")
        if result:
            user_id=users.get_user_id_by_name(request.POST["username"])
            request.session["user_id"]=user_id
            request.session["user_role"]="admin"
            request.session["user_name"]=request.POST["username"]
            return redirect("/admin_dashboard")
        else:
            request.session["error"]="Invalid user name or password"
            return redirect("/admin_login")
    context=getContext(request)
    return render(request,"admin_login.html",context)

def stock_manager_login(request):
    if request.method=="POST":
        users=Users()   
        result=users.check_authorization(request.POST["username"],request.POST["password"],"stock manager")
        if request.POST["store"]=="":
            request.session["error"]="Store field is required to login"
            return redirect("/stock_manager_login")
        elif result:
            user_id=users.get_user_id_by_name(request.POST["username"])
            request.session["user_id"]=user_id
            request.session["user_role"]="stock manager"
            request.session["user_name"]=request.POST["username"]
            request.session["store_name"]=request.POST["store"]
            return redirect("/stock_management")
        else:
            request.session["error"]="Invalid user name or password"
            return redirect("/stock_manager_login")
    store_obj=Stores()
    stores_list=store_obj.get_product_sale_stores_list()
    context=getContext(request)
    context["stores_list"]=[i.capitalize() for i in stores_list]
    return render(request,"stock_manager_login.html",context)

def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    if "user_name" in request.session:
        del request.session["user_name"]
    if "user_role" in request.session:
        del request.session["user_role"]
    if "store_name" in request.session:
        del request.session["store_name"]
    return redirect("/login")