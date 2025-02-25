import os
class FileManager():
    
    def create_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, 777)
            print(f"Folder {folder_name} created.")
        else:
            print(f"Folder {folder_name} already exists.")
    
    def checkExistence(self,folder_name):
        if not folder_name:
            return False
        else :
            if os.path.exists(folder_name):
                return True
            else:
                return False
    def save_data(self, data, path):
        if not os.path.exists(path):
            return (False, "Path does not exist")
        else:
            fileName = os.path.normpath(os.path.join(path, "data.txt"))
            with open(fileName, "w") as file:
                file.write(data)
                return (True, "Data saved")
    def open_file(self, path):
        if not os.path.exists(path):
            return (False, None)

        fileName = os.path.normpath(os.path.join(path, "data.txt"))  # Ensures cross-platform compatibility
    
        try:
            with open(fileName, "r") as file:  # Explicitly set mode to "r" for reading
                data = file.read()
                return (True, data)
        except Exception as e:
            print(f"Error reading data from {path}: {str(e)}")
            return (False, str(e))  # Ensure e is converted to a string safely
        
    def delete(self, path):
        if not os.path.exists(path):
            return (False,"Could not delete {path}")
        else:
            try:
                fileName = os.path.normpath(os.path.join(path, "data.txt"))  # Ensures cross-platform compatibility
                if os.path.isdir(path):
                    os.remove(fileName) 
                    os.rmdir(path)  
                    return (True, "Directory deleted successfully")
                else:
                    return (False, "Path is neither a file nor a directory")
            except Exception as e:
                return (False,str(e))