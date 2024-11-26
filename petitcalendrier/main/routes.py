from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/apropos")
def apropos():
    return render_template("apropos.j2")