from flask import Flask, render_template, request
from datetime import datetime
import requests
import smtplib

my_email = "pythonautomationapp@gmail.com"
password = "dxabiogqxlleamrw"

app = Flask(__name__)

response = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
now = datetime.now()
date = now.strftime("%B %m, %Y")


def send_message(name, email, phone, message):
    message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="automation.python@yahoo.com", msg=message)


@app.route("/")
def home():
    return render_template("index.html", posts=response, date=date)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post/<int:post_id>")
def post(post_id):
    requested_post = None
    for x in response:
        if x["id"] == post_id:
            requested_post = x
    return render_template("post.html", post=requested_post, date=date)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_message(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", msg_sent=False)


if __name__ == "__main__":
    app.run(debug=True)
