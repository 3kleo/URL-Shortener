from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from random import SystemRandom
from string import ascii_lowercase, digits


def generate_random_string(n):
    string = ''.join(SystemRandom().choice(ascii_lowercase + digits) for i in range(n))
    return string


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app_url = 'http://127.0.0.1:5000/'


class links(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    long_link = db.Column("long", db.String(5000))
    short_link = db.Column("short", db.String(50))

    def __init__(self, long_link, short_link):
        self.long_link = long_link
        self.short_link = short_link


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        str_old_url = request.form["long_url"]
        found_link = links.query.filter_by(long_link=str_old_url).first()

        if found_link:
            str_new_url = found_link.short_link
            return render_template("shortened.html", str_new_url=str_new_url, app_url=app_url)
        else:
            str_new_url = generate_random_string(6)
            new_link = links(str_old_url, str_new_url)
            db.session.add(new_link)
            db.session.commit()
        return render_template("shortened.html", str_new_url=str_new_url, app_url=app_url)
    else:
        return render_template("index.html")


@app.route("/<short_link>")
def test_short_link(short_link):
    found_short_link = links.query.filter_by(short_link=short_link).first()
    if found_short_link:
        long_link = found_short_link.long_link
        if long_link.find("http://") != 0 and long_link.find("https://") != 0:
            long_link = "http://" + long_link
        return redirect(long_link)
    else:
        return render_template("not_found.html")


if __name__ == '__main__':
    db.create_all()
    app.run()

