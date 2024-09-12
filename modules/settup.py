import os
import settings
from app import Users,UserDetail

def create_admin_account():
    users_object=Users()
    user_detail=UserDetail()
    users_object.create_user("admin","admin","admin")
    user_id=users_object.get_user_id_by_name("admin")
    user_detail.add_detail(user_id,"male","","male_1.png")

def create_store_directory():
    if os.path.exists(settings.APPLICATION_STORE_DATA_PATH)==False:
        os.makedirs(settings.APPLICATION_STORE_DATA_PATH)

def create_cache_dir():
    if os.path.exists(settings.APP_CACHE_PATH)==False:
        os.makedirs(settings.APP_CACHE_PATH)

# create_admin_account()
# create_store_directory()
# create_cache_dir()