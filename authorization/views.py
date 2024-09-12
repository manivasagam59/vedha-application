from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from modules.app import Users,Stores

def home(request):
    return redirect("/login")

def login(request):
    error=""
    if request.method=="POST":
        users=Users()   
        result=users.check_authorization(request.POST["username"],request.POST["password"],"employee")
        if result:
            user_id=users.get_user_id_by_name(request.POST["username"])
            request.session["user_id"]=user_id
            request.session["user_role"]="employee"
            request.session["user_name"]=request.POST["username"]
            request.session["store_name"]=request.POST["store"]
            return redirect("/dashboard")
        else:
            error="Invalid user name or password"
    store_obj=Stores()
    stores_list=store_obj.get_stores_list()
    stores_list=[i.capitalize() for i in stores_list]
    return render(request,"store_login.html",{"error":error,"stores_list":stores_list})
    
def admin_login(request):
    error=""
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
            error="Invalid user name or password"
    return render(request,"admin_login.html",{"error":error})
    
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