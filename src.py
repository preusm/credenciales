from format import OUTPUT_FORMAT
import os
import csv
    
# Read users from csv
def read_personas(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        users = list(reader)
    
    for user in users:
        rut = user['rut']
        user['rut'] = rut.split('-')[0]
        user['rut_dv'] = rut.split('-')[1].upper()
        
    return users

# Exclude ruts from list
def exclude_ruts(users, ruts):
    filtered = users
    
    for rut in ruts:
        for user in users:
            if user['rut'] == rut:
                filtered.remove(user)
        
    return filtered

# List generated credentials in folder
def list_generated(folder):
    files = []
    
    for file in os.listdir(folder):
        if file.endswith(OUTPUT_FORMAT):
            files.append(file)
            
    users = []
            
    for file in files:
        users.append(file.split('.')[0])
            
    return users

# Truncate string to length
def truncate(string, length):
    if len(string) > length:
        return string.split(' ')[0]
    else:
        return string
    
def search_images(path, image_format):
    files = []
    
    for file in os.listdir(path):
        if file.endswith(tuple(image_format)):
            files.append(path + '/' + file)
            
    return files

def find_users_for_image(files, csv):
    users = []
    not_found = []

    for file in files:
        rut_file = file.split('.')[0]
        rut_file = rut_file.split('/')[-1]
        
        rut = rut_file.split('-')[0]
        
        for persona in csv:            
            found = False
            if rut == persona['rut']:
                found = True
                
                user = {
                    'firstname': truncate(persona['nombre'], 14),
                    'lastname': truncate(persona['apellido'], 14),
                    'rut': persona['rut'],
                    'rut_dv': persona['rut_dv'],
                    'image': file
                }
                
                users.append(user)
                
                break
                
        if not found:
            not_found.append(rut_file)
        
    return (users, not_found)