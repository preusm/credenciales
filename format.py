from PIL import Image, ImageDraw, ImageFont

OUTPUT_FORMAT = '.png'

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
    