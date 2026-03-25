from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    data = load_data()
    return render_template("index.html", groups=data)


@app.route("/create_group", methods=["POST"])
def create_group():
    group_name = request.form["group_name"]

    data = load_data()

    if group_name not in data:
        data[group_name] = {"members": []}

    save_data(data)
    return redirect("/")


@app.route("/add_member", methods=["POST"])
def add_member():
    group_name = request.form["group_name"]
    member_name = request.form["member_name"]

    data = load_data()

    if group_name in data:
        data[group_name]["members"].append(member_name)

    save_data(data)
    return redirect("/")
@app.route("/set_habit", methods=["POST"])
def set_habit():
    group_name = request.form["group_name"]
    habit = request.form["habit"]

    data = load_data()

    if group_name in data:
        data[group_name]["habit"] = habit
        data[group_name]["progress"] = {}

    save_data(data)
    return redirect("/")
@app.route("/mark_done", methods=["POST"])
def mark_done():
    group_name = request.form["group_name"]
    member_name = request.form["member_name"]

    data = load_data()

    if "progress" not in data[group_name]:
        data[group_name]["progress"] = {}

    data[group_name]["progress"][member_name] = True

    save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

