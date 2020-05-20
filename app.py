from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def read_file(filename):
    opened_file = open(filename, 'r')
    config_content = opened_file.read()
    data = json.loads(config_content)
    opened_file.close()
    return data


@app.route("/api/v1.0/districts/", methods=["GET"])
def get_district():
    f = open('districts.json', 'r')
    data = json.load(f)
    f.close()
    districts_list = []

    for k, v in data.items():
        districts_dict = {'id': k, 'title': v['title']}
        districts_list.append(districts_dict)
    return jsonify(districts_list)


@app.route("/api/v1.0/streets/", methods=["GET"])
def get_streets():
    district = request.args.get("district")
    districts_data = read_file("districts.json")
    streets_data = read_file("streets.json")

    if district in districts_data.keys():
        streets_list = []
        for k, v in districts_data.items():
            if district == k:
                for x, y in streets_data.items():
                    for i in v["streets"]:
                        if int(i) == int(x):
                            st = {"id": x, "title": y["title"], "volunteer": y["volunteer"]}
                            streets_list.append(st)
        return jsonify(streets_list)
    else:
        return jsonify(), 404


@app.route("/api/v1.0/volunteers")
def get_volunteers():
    streets = request.args.get("streets")
    volunteers = read_file("volunteers.json")
    street = read_file("streets.json")
    if streets in street.keys():
        volunteers_list = []

        for k, v in street.items():
            if streets == k:
                for i in v["volunteer"]:
                    for x, y in volunteers.items():
                        if int(i) == int(x):
                            volunteer_item = {"id": x, "name": y["name"], "userpic": y["userpic"], "phone": y["phone"]}
                            volunteers_list.append(volunteer_item)
        return jsonify(volunteers_list)
    else:
        return jsonify(), 404


@app.route("/api/v1.0/helpme/", methods=["POST"])
def get_help():
    if not request.json:
        abort(400)
    response = {
        "district": request.json['district'],
        "street": request.json['street'],
        "volunteer": request.json['volunteer'],
        "address": request.json['address'],
        "name": request.json['name'],
        "surname": request.json['surname'],
        "phone": request.json['phone'],
        "text": request.json['text']}

    with open('helpme.json') as f:
        data = json.load(f)
    data.append(response)
    with open("helpme.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

    return jsonify({"status": "success"}), 201


app.run(debug=True)
