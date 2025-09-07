import camera
import util
import os
from flask import Flask, render_template, request, redirect, url_for, session
from util import auth_required, get_current_dates_from_sd_page
from user import user_bp
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("USER_SECRET_KEY")

app = Flask(__name__)
app.secret_key = secret_key
app.register_blueprint(user_bp)

@app.route("/")
def index():
    print(session["credentials"])
    cam_index = camera.get_index_page()
    dates = util.format_dates(util.get_current_dates_from_sd_page(cam_index))
    return render_template("index.html", items=dates)


@app.route("/<date>/<mediafolder>")
def media_list(date): # Media folder is the name of the folder, e.g. record000, or image000 (000 can be xxx)
    return ""



app.run()
