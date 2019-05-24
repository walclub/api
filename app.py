# -*- coding: utf-8 -*-
from flask import Flask, Response, request
from os import environ as env
from dbm import Connector_DBM
import jsonify
import json

app = Flask(__name__)

dbm = Connector_DBM(env["DBM_HOST"],
                    env["DBM_PORT"],
                    env["DBM_USER"],
                    env["DBM_PASSWORD"], 
                    env["DBM_DB"])

@app.route("/products", methods=["GET"])
def products():
    products = dbm.get_products(4)
    list_products = []
    for product in products:
        del product["_id"]
        list_products.append(product)
    response = {"products": list_products}
    return Response(json.dumps(response), mimetype="application/json", status=200)

@app.route("/transfer", methods=["POST"])
def transfer():
    if request.json["phoneNumberDestination"] == request.json["phoneNumberOrigin"]:
        return Response(json.dumps({"status": "Bad request"}), mimetype="application/json", status=400)
    result = dbm.transfer(request.json, env["FIREBASE"])
    if result is None:
        return Response(json.dumps({"message": "No tiene saldo suficiente", "success": False}), mimetype="application/json", status=200)
    return Response(json.dumps({"message": "Transferencia exitosa", "success": True} if result else {"message": "Problema para transferir", "success": False}), mimetype="application/json", status=200)

@app.route("/users/<phone>/points", methods=["GET"])
def points(phone):
    result = dbm.points(int(phone))
    return Response(json.dumps({"success": True, "message": int(result)} if result else {"success": False, "message": "Usuario sin cuenta"}), mimetype="application/json", status=200)

@app.route("/tokens", methods=["POST"])
def token():
    result = dbm.save_token(request.json)
    return Response(json.dumps({"success": True, "message": "Token saved"} if result else {"success": False, "message": "error"}), mimetype="application/json", status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)