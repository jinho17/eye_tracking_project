import base64
from io import BytesIO
from PIL import Image
import os

def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error: Creating directory.'+dir)

def img_to_str(img):
    res = base64.b64encode(img.getvalue())
    return res

def str_to_img(data):
    res = base64.b64decode(data)
    return res

def img_show(img):
    image = Image.open(BytesIO(img))
    image.show()

def img_save(img, user, num):
    image = Image.open(BytesIO(img))
    createFolder('./data')
    image.save('data/'+user+'_'+str(num)+'.png')
