import os
from flask import Flask
from flask import render_template
from flask import request

from numbercreator import rewrite_number


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'public'),
          static_url_path='/public')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        number = request.form.get("number")
        try:
            number = float(number)
        except ValueError:
            return render_template("index.html", error="Sorry, try entering a number.")
        output, result = rewrite_number(number)
            # return render_template("index.html", error="Sorry, we had a problem with your number.")
        return render_template("index.html", number=number, output=output, result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
