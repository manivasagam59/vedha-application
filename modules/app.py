import os
import shutil
import sqlite3
import json
from .import settings
import datetime


class Stores:
    def open(self):
        self.connection=sqlite3.connect(settings.APP_DATA_DB)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stores(ID INTEGER PRIMARY KEY AUTOINCREMENT,StoreName VARCHAR(255) NOT NULL, MobileRecharge BOOLEAN DEFAULT False, DTHRecharge BOOLEAN DEFAULT False, OnlineService BOOLEAN DEFAULT False, ProductSale BOOLEAN DEFAULT False )")

    def close(self):
        self.connection.close()

    def check_store_exists(self,store_name):
        self.open()
        store_name=store_name.lower()
        result=self.cursor.execute("SELECT COUNT(ID) as Counts FROM stores WHERE StoreName=?",[store_name])
        data=result.fetchall()
        self.close()
        store_count=data[0][0]
        if store_count>0:
            return True
        else:
            return False

    def get_stores_list(self):
        self.open()
        result=self.cursor.execute("SELECT StoreName FROM stores")
        data=result.fetchall()
        self.close()
        stores_list=[i[0].capitalize() for i in data]
        return stores_list

    def get_store(self,store_name):
        self.open()
        store_name=store_name.lower()
        result=self.cursor.execute("SELECT StoreName,MobileRecharge,DTHRecharge,OnlineService,ProductSale FROM stores WHERE StoreName=?",[store_name])
        data=result.fetchall()
        self.close()
        return data[0]
          
    def get_store_id_by_name(self,store_name):
        self.open()
        store_name=store_name.lower()
        result=self.cursor.execute("SELECT ID FROM stores WHERE StoreName=?",[store_name])
        data=result.fetchall()
        self.close()
        return data[0][0]

    def create_store(self,store_name,mobile_recharge,dth_recharge,online_service,product_sale):
        self.open()
        store_name=store_name.lower()
        store_name=store_name.strip()
        self.cursor.execute("INSERT INTO stores(StoreName,MobileRecharge,DTHRecharge,OnlineService,ProductSale) VALUES(?,?,?,?,?)",[store_name,mobile_recharge,dth_recharge,online_service,product_sale])
        self.connection.commit()
        self.close()
        # Creating a dir path for store_data
        store_id=self.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        if os.path.exists(path)==False:
            os.makedirs(path)
        # create info.json file in dir for storing service availability start date and another
        d=datetime.datetime.now()
        start_date="{:2d}-{:2d}-{:2d}".format(d.year,d.month,d.day)
        start_date=start_date.replace(" ","0")
        default_data_for_info_file={"store_creation_date":start_date,"mb_start_date":start_date,"dth_start_date":start_date,"online_service_start_date":start_date,"product_sale_start_date":start_date}
        with open(path+"\\info.json","w") as file:
            file.write(json.dumps(default_data_for_info_file))

    def delete_store(self,store_name):
        store_name=store_name.lower()
        # Removing Store data path
        store_id=self.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        if os.path.exists(path)==True:
            shutil.rmtree(path)
        # Removing store data form db
        self.open()
        self.cursor.execute("DELETE FROM stores WHERE StoreName=?",[store_name])
        self.connection.commit()
        self.close()
        
    def edit_store(self,store_name,store_new_name,mobile_recharge,dth_recharge,online_service,product_sale):
        self.open()
        store_name=store_name.lower()
        store_new_name=store_new_name.lower()
        self.cursor.execute("UPDATE stores SET StoreName=?,MobileRecharge=?,DTHRecharge=?,OnlineService=?,ProductSale=? WHERE StoreName=?",[store_new_name,mobile_recharge,dth_recharge,online_service,product_sale,store_name])
        self.connection.commit()
        self.close()
    
    def get_all_store_data(self):
        self.open()
        result=self.cursor.execute("SELECT StoreName,MobileRecharge,DTHRecharge,OnlineService,ProductSale FROM stores")
        data=result.fetchall()
        self.close()
        return data

class Users:
    def open(self):
        self.connection=sqlite3.connect(settings.APP_DATA_DB)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, UserName VARCHAR(255) NOT NULL, Role VARCHAR(100) NOT NULL, Password VARCHAR(255) NOT NULL)")

    def close(self):
        self.connection.close()

    def user_exists(self,user_name):
        self.open()
        user_name=user_name.lower()
        result=self.cursor.execute("SELECT COUNT(ID) as Counts FROM users WHERE Username=?",[user_name])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False
    
    def get_user_id_by_name(self,user_name):
        self.open()
        user_name=user_name.lower()
        result=self.cursor.execute("SELECT ID FROM users WHERE Username=?",[user_name])
        data=result.fetchall()
        self.close()
        return data[0][0]

    def check_authorization(self,user_name,password,role):
        self.open()
        user_name=user_name.lower()
        result=self.cursor.execute("SELECT COUNT(ID) as Counts FROM users WHERE Username=? AND Password=? AND Role=?",[user_name,password,role])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False
    
    def create_user(self,user_name,role,password):
        self.open()
        user_name=user_name.lower()
        self.cursor.execute("INSERT INTO users(UserName, Role, Password) VALUES(?,?,?)",[user_name,role,password])
        self.connection.commit()
        self.close()
    
    def delete_user(self,user_name):
        self.open()
        user_name=user_name.lower()
        self.cursor.execute("DELETE FROM users WHERE UserName=?",[user_name])
        self.connection.commit()
        self.close()

    def edit_password(self,user_name,new_password,old_password):
        self.open()
        user_name=user_name.lower()
        result=self.cursor.execute("UPDATE users SET Password=? WHERE UserName=? AND Password=?",[new_password,user_name,old_password])
        self.connection.commit()
        self.close()
    
    def get_all_users(self):
        self.open()
        result=self.cursor.execute("SELECT UserName FROM users WHERE Role!='admin'")
        user_list=result.fetchall()
        self.close()
        data=[i[0].capitalize() for i in user_list]
        return data

class UserDetail:

    def open(self):
        self.connection=sqlite3.connect(settings.APP_DATA_DB)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usersDetail(ID INTEGER PRIMARY KEY, Gender VARCHAR(50) NOT NULL, ContactNumber VARCHAR(100), ProfileImg VARCHAR(255) NOT NULL)")

    def close(self):
        self.connection.close()

    def check_user_id_exists(self,user_id):
        self.open()
        result=self.cursor.execute("SELECT COUNT(ID) as Counts FROM usersDetail WHERE ID=?",[user_id])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False
    
    def get_user_detail(self,user_id):
        self.open()
        result=self.cursor.execute("SELECT Gender, ContactNumber,ProfileImg FROM usersDetail WHERE ID=?",[user_id])
        data=result.fetchall()
        self.close()
        return data[0]

    def add_detail(self,user_id,gender,contact_number,prof_img):
        if self.check_user_id_exists(user_id)==False:
            self.open()
            gender=gender.lower()
            self.cursor.execute("INSERT INTO usersDetail(ID, Gender, ContactNumber, ProfileImg) VALUES(?,?,?,?)",[user_id,gender,contact_number,prof_img])
            self.connection.commit()
            self.close()

    def update_detail(self,user_id,gender,contact_number,profile_img):
        self.open()
        gender=gender.lower()
        self.cursor.execute("UPDATE usersDetail SET Gender=?, ContactNumber=?, ProfileImg=? WHERE ID=?",[gender,contact_number,profile_img,user_id])
        self.connection.commit()
        self.close()

    def delete_detail(self,user_id):
        self.open()
        self.cursor.execute("DELETE FROM usersDetail WHERE ID=?",[user_id])
        self.connection.commit()
        self.close()

class MobileRecharge:
    
    def __init__(self,store_name,date):

        # Another objects
        self.contacts=Contacts()
        self.bugdb=Bugdb()

        year=str(date[0])
        month=str(date[1])
        day=str(date[2])
        if len(month)==1:
            month="0"+month
        if len(day)==1:
            day="0"+day
        stores=Stores()
        store_id=stores.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        self.db_path=path+"\\mobile_recharge.db"
        self.table_name="mb_"+year+month+day
        # print(self.db_path)

    def open(self):
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}(ID INTEGER PRIMARY KEY AUTOINCREMENT, MobileNumber VARCHAR(100) NOT NULL, Operator VARCHAR(100) NOT NULL, Amount INTEGER NOT NULL)")

    def close(self):
        self.connection.close()

    def check_table_exists(self):
        self.open()
        result=self.cursor.execute(f"SELECT name FROM sqlite_schema WHERE type ='table' AND  name = '{self.table_name}';")
        data=result.fetchall()
        self.close()
        if len(data)>0:
            return True
        else:
            return False

    def insert(self,mobile_number,operator,amount):
        self.open()
        self.cursor.execute(f"INSERT INTO {self.table_name}(MobileNumber, Operator, Amount) VALUES(?,?,?)",[mobile_number,operator,amount])
        self.connection.commit()
        self.close()

        self.contacts.add_number(mobile_number)
        self.bugdb.insert(mobile_number,operator)

    def select(self):
        data=[]
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT MobileNumber, Operator, Amount FROM {self.table_name}")
            data=result.fetchall()
            self.close()
        return data
    
    def get_total_sum(self):
        count=0
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT SUM(Amount) as Total FROM {self.table_name}")
            data=result.fetchall()
            if data[0][0]!=None:
                count=data[0][0]
            self.close()
        return count

class DthRecharge:
    
    def __init__(self,store_name,date):
        year=str(date[0])
        month=str(date[1])
        day=str(date[2])
        if len(month)==1:
            month="0"+month
        if len(day)==1:
            day="0"+day
        stores=Stores()
        store_id=stores.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        self.db_path=path+"\\dth_recharge.db"
        self.table_name="dth_"+year+month+day

    def open(self):
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}(ID INTEGER PRIMARY KEY AUTOINCREMENT, DthNumber VARCHAR(100) NOT NULL, Operator VARCHAR(100) NOT NULL, Amount INTEGER NOT NULL)")

    def close(self):
        self.connection.close()

    def check_table_exists(self):
        self.open()
        result=self.cursor.execute(f"SELECT name FROM sqlite_schema WHERE type ='table' AND  name = '{self.table_name}';")
        data=result.fetchall()
        self.close()
        if len(data)>0:
            return True
        else:
            return False

    def insert(self,dth_number,operator,amount):
        self.open()
        self.cursor.execute(f"INSERT INTO {self.table_name}(DthNumber, Operator, Amount) VALUES(?,?,?)",[dth_number,operator,amount])
        self.connection.commit()
        self.close()

    def select(self):
        data=[]
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT DthNumber, Operator, Amount FROM {self.table_name}")
            data=result.fetchall()
            self.close()
        return data
    
    def get_total_sum(self):
        count=0
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT SUM(Amount) as Total FROM {self.table_name}")
            data=result.fetchall()
            if data[0][0]!=None:
                count=data[0][0]
            self.close()
        return count

class OnlineService:
    
    def __init__(self,store_name,date):
        year=str(date[0])
        month=str(date[1])
        day=str(date[2])
        if len(month)==1:
            month="0"+month
        if len(day)==1:
            day="0"+day
        stores=Stores()
        store_id=stores.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        self.db_path=path+"\\online_service.db"
        self.table_name="os_"+year+month+day

    def open(self):
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}(ID INTEGER PRIMARY KEY AUTOINCREMENT, ServiceName VARCHAR(255) NOT NULL, Amount INTEGER NOT NULL);")

    def close(self):
        self.connection.close()

    def check_table_exists(self):
        self.open()
        result=self.cursor.execute(f"SELECT name FROM sqlite_schema WHERE type ='table' AND  name = '{self.table_name}';")
        data=result.fetchall()
        self.close()
        if len(data)>0:
            return True
        else:
            return False

    def insert(self,service_name,amount):
        self.open()
        self.cursor.execute(f"INSERT INTO {self.table_name}(ServiceName, Amount) VALUES(?,?)",[service_name,amount])
        self.connection.commit()
        self.close()

    def select(self):
        data=[]
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT ServiceName, Amount FROM {self.table_name}")
            data=result.fetchall()
            self.close()
        return data
    
    def get_total_sum(self):
        count=0
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT SUM(Amount) as Total FROM {self.table_name}")
            data=result.fetchall()
            if data[0][0]!=None:
                count=data[0][0]
            self.close()
        return count

class ProductSales:
    
    def __init__(self,store_name,date):
        year=str(date[0])
        month=str(date[1])
        day=str(date[2])
        if len(month)==1:
            month="0"+month
        if len(day)==1:
            day="0"+day
        stores=Stores()
        store_id=stores.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        self.db_path=path+"\\product_sales.db"
        self.table_name="ps_"+year+month+day

    def open(self):
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}(BillId INTEGER PRIMARY KEY AUTOINCREMENT, Bill TEXT NOT NULL, Amount INTEGER NOT NULL);")

    def close(self):
        self.connection.close()

    def check_table_exists(self):
        self.open()
        result=self.cursor.execute(f"SELECT name FROM sqlite_schema WHERE type ='table' AND  name = '{self.table_name}';")
        data=result.fetchall()
        self.close()
        if len(data)>0:
            return True
        else:
            return False

    def insert(self,bill,amount):
        self.open()
        self.cursor.execute(f"INSERT INTO {self.table_name}(Bill, Amount) VALUES(?,?)",[bill,amount])
        self.connection.commit()
        self.close()

    def select(self):
        data=[]
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT BillId, Amount FROM {self.table_name}")
            data=result.fetchall()
            self.close()
        return data
    
    def get_bill_by_id(self,bill_id):
        data=[]
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT Bill, Amount FROM {self.table_name} WHERE BillId=?",[bill_id])
            bill=result.fetchall()
            if bill!=[]:
                data=bill[0]
            self.close()
        return data

    def get_total_sum(self):
        count=0
        if self.check_table_exists():
            self.open()
            result=self.cursor.execute(f"SELECT SUM(Amount) as Total FROM {self.table_name}")
            data=result.fetchall()
            if data[0][0]!=None:
                count=data[0][0]
            self.close()
        return count

class StockManagement:

    def __init__(self,store_name):
        stores=Stores()
        store_id=stores.get_store_id_by_name(store_name)
        path=settings.get_store_dir(store_id)
        self.db_path=path+"\\store_database.db"

    def open(self):
        self.connection=sqlite3.connect(self.db_path)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stock_list(ID INTEGER PRIMARY KEY AUTOINCREMENT, ProductName VARCHAR(255) NOT NULL, Price INTEGER NOT NULL, StockQuantity INTEGER NOT NULL, MinStockNotificationAt INTEGER NOT NULL)")

    def close(self):
        self.connection.close()

    def check_stock_exists(self,product_name):
        self.open()
        product_name=product_name.lower().strip()
        result=self.cursor.execute("SELECT COUNT(ID) as Count from stock_list WHERE ProductName=?",[product_name])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False

    def check_stock_update_exists(self,product_id,product_name):
        self.open()
        product_name=product_name.lower().strip()
        result=self.cursor.execute("SELECT COUNT(ID) as Count from stock_list WHERE ProductName=? AND ID!=?",[product_name,product_id])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False

    def add_stock(self,product_name,price,quantity, min_stock_notification_at):
        self.open()
        product_name=product_name.lower().strip()
        self.cursor.execute("INSERT INTO stock_list(ProductName, Price, StockQuantity, MinStockNotificationAt) VALUES(?,?,?,?)",[product_name,price,quantity, min_stock_notification_at])
        self.connection.commit()
        self.close()

    def update_stock(self,stock_id,product_name,price,quantity, min_stock_notification_at):
        self.open()
        product_name=product_name.lower().strip()
        self.cursor.execute("UPDATE stock_list SET ProductName=?, Price=?, StockQuantity=?, MinStockNotificationAt=? WHERE ID=?",[product_name,price,quantity, min_stock_notification_at,stock_id])
        self.connection.commit()
        self.close()

    def purchase_product_by_id(self,product_id,stock_sale):
        self.open()
        self.cursor.execute("UPDATE stock_list SET StockQuantity=StockQuantity-? WHERE ID=?",[stock_sale,product_id])
        self.connection.commit()
        self.close()

    def delete_stock(self,stock_id):
        self.open()
        self.cursor.execute("DELETE FROM stock_list  WHERE ID=?",[stock_id])
        self.connection.commit()
        self.close()

    def get_all_products(self):
        self.open()
        result=self.cursor.execute("SELECT ID,ProductName from stock_list")
        data=result.fetchall()
        self.close()
        return data

    def get_all_stocks(self):
        self.open()
        result=self.cursor.execute("SELECT ID, ProductName, Price, StockQuantity, MinStockNotificationAt FROM stock_list")
        data=result.fetchall()
        self.close()
        return data

    def get_low_stock_count(self):
        self.open()
        result=self.cursor.execute("SELECT COUNT(ID) FROM stock_list WHERE StockQuantity <= MinStockNotificationAt")
        data=result.fetchall()
        self.close()
        return data[0][0]

    def get_stock_detail_by_id(self,stock_id):
        self.open()
        result=self.cursor.execute("SELECT ProductName,Price,StockQuantity FROM stock_list WHERE ID=?",[stock_id])
        data=result.fetchall()
        self.close()
        if data!=[]:
            return data[0]
        else:
            return data

    def get_stock_detail_by_product_name(self,product_name):
        self.open()
        result=self.cursor.execute("SELECT * FROM stock_list WHERE ProductName=?",[product_name])
        data=result.fetchall()
        self.close()
        if data!=[]:
            return data[0]
        else:
            return data

    def get_total_sum(self):
        self.open()
        result=self.cursor.execute("SELECT SUM(Price * StockQuantity ) as TotalStockPrice FROM stock_list")
        data=result.fetchall()
        count=data[0][0]
        self.close()
        return count

class Contacts:

    def open(self):
        self.connection=sqlite3.connect(settings.CONTACTS_DATABASE_PATH)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contacts(ID INTEGER PRIMARY KEY AUTOINCREMENT, ContactNumber INTEGER NOT NULL)")

    def close(self):
        self.connection.close()

    def check_number_exists(self,contact_no):
        self.open()
        result=self.cursor.execute("SELECT COUNT(ID) as Count FROM contacts WHERE ContactNumber=?",[contact_no])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False
    
    def add_number(self,contact_no):
        if self.check_number_exists(contact_no)==False:
            self.open()
            self.cursor.execute("INSERT INTO contacts(ContactNumber) VALUES(?)",[contact_no])
            self.connection.commit()
            self.close()

    def get_all_contacts(self):
        self.open()
        result=self.cursor.execute("SELECT ContactNumber FROM contacts")
        data=result.fetchall()
        self.close()
        data=[i[0] for i in data]
        return data
        
class Bugdb:

    def open(self):
        self.filter_ts=7
        self.filter_te=9
        self.connection=sqlite3.connect(settings.BUGDB)
        self.cursor=self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contacts(ID INTEGER PRIMARY KEY AUTOINCREMENT, ContactNumber INTEGER NOT NULL,Operator VARCHAR NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS filtered_contacts(ID INTEGER PRIMARY KEY AUTOINCREMENT, ContactNumber INTEGER NOT NULL,Operator VARCHAR NOT NULL, InsertedDate DATE DEFAULT (datetime('now','localtime')))")

    def close(self):
        self.connection.close()

    def check_number_exists(self,contact_no):
        self.open()
        result=self.cursor.execute(f"SELECT COUNT(ID) as Count FROM contacts WHERE ContactNumber=?",[contact_no])
        data=result.fetchall()
        self.close()
        if data[0][0] !=0:
            return True
        else:
            return False
    
    def insert(self,contact_no,operator):
        if self.check_number_exists(contact_no)==False:
            date=datetime.datetime.now()
            self.open()
            self.cursor.execute("INSERT INTO contacts(ContactNumber,Operator) VALUES(?,?)",[contact_no,operator])
            if date.hour>=self.filter_ts and date.hour<=self.filter_te:
                self.cursor.execute("INSERT INTO filtered_contacts(ContactNumber,Operator) VALUES(?,?)",[contact_no,operator])
            self.connection.commit()
            self.close()


# class PendingTask:
    
#     def __init__(self,store_name,date):
#         year=str(date[0])
#         month=str(date[1])
#         day=str(date[2])
#         if len(month)==1:
#             month="0"+month
#         if len(day)==1:
#             day="0"+day
#         stores=Stores()
#         store_id=stores.get_store_id_by_name(store_name)
#         path=settings.get_store_dir(store_id)
#         self.db_path=path+"\\store_database.db"

#     def open(self):
#         self.connection=sqlite3.connect("")
#         self.cursor=self.connection.cursor()
#         self.cursor.execute("CREATE TABLE IF NOT EXISTS pending_task(ID INTEGER PRIMARY KEY AUTOINCREMENT, CreatedDate DATE DEFAULT (datetime('now','localtime')), Task VARCHAR(255) NOT NULL , CreatedBy VARCHAR(255) NOT NULL)")

#     def close(self):
#         self.connection.close()

#     def get_all_tasks(self):
#         self.open()
#         result=self.cursor.execute("SELECT * FROM pending_task")
#         data=result.fetchall()
#         self.close()
#         return data

#     def add_task(self,task,created_by):
#         self.open()
#         self.cursor.execute("INSERT INTO pending_task(Task,CreatedBy) VALUES(?,?)",[task,created_by])
#         self.connection.commit()
#         self.close()
        
#     def delete_task(self,task_id):
#         self.open()
#         self.cursor.execute("DELETE FROM pending_task WHERE ID=?",[task_id])
#         self.connection.commit()
#         self.close()
