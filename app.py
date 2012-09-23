import os
from flask import Flask
from flask import render_template
from flask import request
import random
from numbercreator import rewrite_number


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'public'),
          static_url_path='/public')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", number=random.randrange(-1000, 1000))
    else:
        number = request.form.get("number")
        try:
            number = float(number)
        except ValueError:
            return render_template("index.html", number=number, error="Sorry, try entering a number.")
        try:
            output, result = rewrite_number(number)
        except:
            return render_template("index.html", number=number, error="Sorry, we had a problem with your number.")
        return render_template("index.html", number=number, output=output, result=result)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
