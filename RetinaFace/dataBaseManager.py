from fileManager import FileManager

class DataBaseManager():
    def __init__(self, db_path):
        self.db_path = db_path
        self.fileManager = FileManager()
    
    
    
    def create_database(self,databaseName):
        if self.is_data_base_Exist(databaseName):
            print("Database already exists.")
        else:
            #create new folder
            self.fileManager.create_folder(databaseName)
            print("Database created.")
            
    def create_table(self,table_name, db_name = None):
        
        if db_name is None:
            db_name = self.db_path
            table_path = db_name + "/" + table_name
            if( self.fileManager.checkExistence(table_path)):
                print("Table already exists.")
            else:
                #create new folder
                self.fileManager.create_folder(table_path)
                print("Table created.")
            return True
        
        else:
            if(db_name == self.db_path):
                table_path = db_name + "/" + table_name
                if( self.fileManager.checkExistence(table_path)):
                    print("Table already exists.")
                else:
                    #create new folder
                    self.fileManager.create_folder(table_path)
                    print("Table created.")
                return True
            else:
                print("Database does not exist.")
                return False
    
    def insert(self,data, table_name, db_name):
        tablePath = db_name + "/" + table_name
        print("Inserting data into table ",table_name)
        if(self.fileManager.checkExistence(tablePath)):
            result = self.fileManager.save_data(data, tablePath)
            print(result)
        else:
            print("Table does not exist.")
            
    def get(self, table_name, db_name=None):
    
        if db_name is None: 
            db_name = self.db_path
            tablePath = db_name +'/' + table_name
            return self.fileManager.open_file(tablePath)
        else:
            tablePath = db_name +'/' + table_name
            return self.fileManager.open_file(tablePath)
    def delete_table(self, table_name, db_name=None):
        if db_name is not None:
            tablePath = db_name + '/' + table_name
            try:
                if(self.fileManager.delete(tablePath)):
                    print("Table {table_name} was successfully deleted")
            except Exception as e:
                print(f"can not delete table {table_name}: {str(e)}")
        else:
            tablePath = self.db_path + "/" + table_name
            try:
                if(self.fileManager.delete(tablePath)):
                    print("Table {table_name} was successfully deleted")
            except Exception as e:
                print(f"can not delete table {table_name}: {str(e)}")
        
        
        
        
    def is_data_base_Exist(self, db_name):
        return self.fileManager.checkExistence(db_name)