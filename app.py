from flask import Flask, jsonify, request
from database import get_database

app = Flask(__name__)

@app.route("/")
@app.route("/members", methods = ["GET"])
def members():
    db = get_database()
    allmembers_cursor = db.execute("select * from members")
    allmembers = allmembers_cursor.fetchall()

    final_result = []

    for eachmember in allmembers:
        member_dict = {}
        member_dict["id"] = eachmember["id"]
        member_dict["name"] = eachmember["name"]
        member_dict["email"] = eachmember["email"]
        member_dict["designation"] = eachmember["designation"]
        final_result.append(member_dict)

    return jsonify({"All Members are -" : final_result})


@app.route("/member/<int:id>" , methods = ["GET"])
def get_one_member(id):
    db = get_database()
    onemembers_cursor = db.execute("select * from members where id = ?", [id])
    onemember = onemembers_cursor.fetchone()

    return jsonify({"One Member Fetched -" : 
                    { "id" : onemember["id"] ,
                      "name" : onemember["name"], 
                      "email"  : onemember["email"],
                    "designation" : onemember["designation"]  }})


@app.route("/member/<int:id>" , methods = ["DELETE"])
def deletemember(id):
    db = get_database()
    db.execute("delete from members where id = ?" , [id])
    db.commit()
    return jsonify({ "Message" : "Member got deleted successfully."})


@app.route("/member" , methods = ["POST"])
def add_member():
    new_member_data = request.get_json()
    name = new_member_data["name"]
    email = new_member_data["email"]
    designation = new_member_data["designation"]
    db = get_database()
    db.execute("insert into members (name, email, designation) values (?,?,?)",[name, email, designation])
    db.commit()
    return jsonify({ "Message" : "Member got updated successfully."})

@app.route("/member/<int:id>" , methods = ["PUT"])
def update_member(id):
    new_member_data = request.get_json()
    name = new_member_data["name"]
    email = new_member_data["email"]
    designation = new_member_data["designation"]
    db = get_database()
    db.execute("update members set name = ?, email = ?, designation = ? where id = ?",[name, email, designation, id])
    db.commit()
    return jsonify({ "Message" : "Member got updated successfully."})

if __name__ == "__main__":
    app.run(debug = True)