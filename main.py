from format import generate
from src import *

IMAGE_FORMAT = ['.jpeg', '.jpg', '.png']

USER_TYPES_NAMES = [
    'estudiantes', 
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

for user_type in USER_TYPES:
    print('Generando credenciales para ' + user_type['name'])
    
    csv_file = read_personas(user_type['csv_file'])
    print(str(len(csv_file)) + ' personas en lista')
    
    files = search_images(user_type['input_images'], IMAGE_FORMAT)
    print(str(len(files)) + ' imagenes')
    
    users, not_found = find_users_for_image(files, csv_file)

    if not_found:
        print('No se encontraron datos para las siguientes imagenes:')
        for file in not_found:
            print('  - ' + file)
    print(str(len(users)) + ' usuarios ok')

    generated = list_generated(user_type['output_folder'])
    print('Generados ' + str(len(generated)) + ' usuarios, omitiendo')
    # users = exclude_ruts(users, generated)

    print('Generando ' + str(len(users)) + ' credenciales')

    for user in users:
        print('- ' + user['rut'] + ' - ' + user['firstname'] + ' ' + user['lastname'])
        generate(user_type['base_image'], user_type['output_folder'], user)
