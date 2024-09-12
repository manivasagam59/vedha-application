import os

# Application Path
APPLICATION_PATH="C:\\Users\\Manivasagam\\Documents\\vapp\\application"

# Application Data stored Path
APPLICATION_DATA_PATH=APPLICATION_PATH+"\\data"

# Application Data Database
# Contains User Login Data, Store and Service availability Data
APP_DATA_DB=APPLICATION_DATA_PATH+"\\app_data.db"


# Application stores data path
APPLICATION_STORE_DATA_PATH=APPLICATION_DATA_PATH+"\\stores"

# Path of cache file
APP_CACHE_PATH=APPLICATION_DATA_PATH+"\\cache"

# Contact Number Database
CONTACTS_DATABASE_PATH=APP_CACHE_PATH+"\\contact.db"

# Bugdb path
BUGDB=APP_CACHE_PATH+"\\bugdb.db"

# get store dir path function
def get_store_dir(store_id):
    return APPLICATION_STORE_DATA_PATH+"\\STORE_"+str(store_id)