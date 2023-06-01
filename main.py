from PIL import Image, ImageDraw, ImageFont
import os
import csv

IMAGE_FORMAT = ['.jpeg', '.jpg', '.png']
OUTPUT_FORMAT = '.png'

USER_TYPES_NAMES = [
    # 'estudiantes', 
    'colaboradores'
]

LISTS_FOLDER = 'listas'
INPUT_IMAGES = 'imagenes'
OUTPUT_FOLDER = 'credenciales'
BASE_IMAGES = 'src/images'

def user_type_generate(user_types_names):
    user_types = []
    for user_type in user_types_names:
        user_type = {
            'name': user_type,
            'csv_file': LISTS_FOLDER + '/' + user_type + '.csv',
            'output_folder': OUTPUT_FOLDER + '/' + user_type,
            'base_image': BASE_IMAGES + '/' + user_type + '.png',
            'input_images': INPUT_IMAGES + '/' + user_type
        }    
        
        user_types.append(user_type)
    
    return user_types

USER_TYPES = user_type_generate(USER_TYPES_NAMES)
    
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

def generate(base_image, output_folder, user, output_format=OUTPUT_FORMAT):
    firstname = user['firstname']
    lastname = user['lastname']
    rut = user['rut'] + '-' + user['rut_dv']
    foto = user['image']   
    
    font=ImageFont.truetype('src/fonts/ebold.ttf', size=69)
    font_rut=ImageFont.truetype('src/fonts/medium.ttf', size=31)

    image = Image.open(base_image)
    draw = ImageDraw.Draw(image)
    
    (x,y)=(30,425)
    message = firstname
    color='rgb(0,0,0)'
    draw.text((x,y),message,fill=color,font=font)

    img = Image.open(foto)
    basewidth = 290
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize))
    img = img.rotate(-90, expand=1)
    
    (x,y)=(175,25)
    image.paste(img,(x,y))

    (x,y)=(30,525)
    message = lastname
    color='rgb(0,0,0)'
    draw.text((x,y),message,fill=color,font=font)

    (x,y)=(30,620)
    message = rut
    color='rgb(0,0,0)'
    draw.text((x,y),message,fill=color,font=font_rut)
    
    image = image.rotate(-90, expand=1)
    
    image.save(output_folder + '/' + rut + output_format)
    
# Truncate string to length
def truncate(string, length):
    if len(string) > length:
        return string.split(' ')[0]
    else:
        return string
    
def search_images(path, image_format=IMAGE_FORMAT):
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

for user_type in USER_TYPES:
    print('Generando credenciales para ' + user_type['name'])
    
    csv = read_personas(user_type['csv_file'])
    print(str(len(csv)) + ' personas en lista')
    
    files = search_images(user_type['input_images'], IMAGE_FORMAT)
    print(str(len(files)) + ' imagenes')
    
    users, not_found = find_users_for_image(files, csv)

    if not_found:
        print('No se encontraron datos para las siguientes imagenes:')
        for file in not_found:
            print('  - ' + file)
    print(str(len(users)) + ' usuarios ok')

    generated = list_generated(user_type['output_folder'])
    print('Generados ' + str(len(generated)) + ' usuarios, omitiendo')

    users = exclude_ruts(users, generated)
    print('Generando ' + str(len(users)) + ' credenciales')

    for user in users:
        print('- ' + user['rut'] + ' - ' + user['firstname'] + ' ' + user['lastname'])
        generate(user_type['base_image'], user_type['output_folder'], user)
