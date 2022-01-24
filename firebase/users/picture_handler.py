import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username)+'.'+ext_type

    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)

    # output_size = (200, 200)   # to make size of image as width : 200px and height : 200px

    pic = Image.open(pic_upload)
    # pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename

def add_post_pic(pic_upload, username, count):

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username)+str(count)+'.'+ext_type

    filepath = os.path.join(current_app.root_path, 'static\post_pics', storage_filename)
    pic = Image.open(pic_upload)
    pic.save(filepath)

    return storage_filename