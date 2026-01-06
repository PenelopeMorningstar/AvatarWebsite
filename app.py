import struct
from database import close_connection, init_db, insert_record, get_latest_record
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# API: robot status
@app.route("/data", methods=["GET", "POST"])
def about():
    data_format = "<BBBHHBBBff"
    expected_length = struct.calcsize(data_format)
    mo_convert = lambda v: -v if v < 256 else v - 256

    # post
    if request.method == "POST":
        if request.content_length != expected_length:
            return "", 400
        values = list(struct.unpack(data_format, request.get_data()))
        values[3] = mo_convert(values[3])
        values[4] = mo_convert(values[4])
        status = 204 if insert_record(values) else 400

        return "", status
    # get
    else:
        keys = [
            "row",
            "ts",
            "id",
            "st",
            "ln",
            "mo_l",
            "mo_r",
            "ul_f",
            "ul_r",
            "gr",
            "gy_z",
            "hd",
        ]
        values = get_latest_record()
        return jsonify(dict(zip(keys, values)))


with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
