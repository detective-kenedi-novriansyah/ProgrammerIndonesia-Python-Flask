import secrets
import os
from PIL import Image
from flask import current_app

def save_profile(index):
    x = secrets.token_hex(8)
    _,f = os.path.splitext(index.filename)
    # filename.jpg
    # ["filename","jpg"]
    filename = x + f 
    path = os.path.join(current_app.root_path, "static/" + filename)
    i = Image.open(index)
    size = (125,125)
    i.thumbnail(size)
    i.save(path)
    return filename