from flask import Blueprint, render_template

blue_print_home = Blueprint('', __name__)

@blue_print_home.route('/', methods=["GET", "POST"])
def home():
    return render_template('home/index.html')