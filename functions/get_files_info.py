import os

def get_files_info(working_directory, directory="."):
    
    target_directory = os.path.join(working_directory, directory)
   
    if os.path.commonpath([os.path.abspath(target_directory), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
         
    
    if os.path.isdir(target_directory) is False:
        return f'Error: "{directory}" is not a directory'
        
    
    files_info = []

    try: 
        directory_items = os.listdir(target_directory)
    

        for item in directory_items:
                
            item_path = os.path.join(target_directory, item)
            item_size = os.path.getsize(item_path)
            
            if os.path.isfile(item_path):
                files_info.append({
                    "item_name": item,
                    "is_dir": False,
                    "size_bytes": item_size
                })
            else:
                files_info.append({
                    "item_name": item,
                    "is_dir": True,
                    "size_bytes": item_size
                })
    except Exception as e:
        return f"Error: {e}"
        
    
    files_info_string = "\n".join([f"- {item['item_name']}: file_size={item['size_bytes']} bytes, is_dir={item['is_dir']}" for item in files_info])
    
    return files_info_string