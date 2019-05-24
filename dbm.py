from pymongo import MongoClient
import requests

class Connector_DBM:

    def __init__(self, host, port, user, password, database):
        URI = ("mongodb://" + user + \
              ":" + password + "@" + \
              host + ":" + port + "/")
        __conn = MongoClient(URI)
        self.__db = __conn.products

    def get_products(self, number):
        return self.__db.product.find({}).limit(number)

    def transfer(self, data, firebase):
        origin = self.__db.users.find_one({"phone.number":data["phoneNumberOrigin"]["number"]})
        destination_token = self.__db.tokens.find_one({"phoneNumber":int(data["phoneNumberDestination"]["number"])})["token"]
        destination = self.__db.users.find_one({"phone.number":data["phoneNumberDestination"]["number"]})
        if origin["amount"] - data["amount"] >= 0 and destination is not None:
                self.__db.users.update({"_id": origin["_id"]}, {"$set":{"amount": origin["amount"] - data["amount"]}} , upsert=False)
                self.__db.users.update({"_id": destination["_id"]}, {"$set":{"amount" :data["amount"] + destination["amount"]}} , upsert=False)
                data_firebase = \
                {
                  "notification":{
                    "title":"WalClub - Tu Walmart",
                    "body":"Has recibido una transferencia de " + str(data["amount"]),
                    "sound":"default",
                    "click_action":"FCM_PLUGIN_ACTIVITY",
                    "icon":"fcm_push_icon"
                  },
                  "data":{
                    "landing_page":"second",
                    "price":"$" + str(data["amount"])
                  },
                    "to": destination_token,
                    "priority":"high",
                    "restricted_package_name":""
                }
                headers = \
                {
                "Content-Type":"application/json",
                "Authorization":"key=" + str(firebase)
                }
                requests.post("https://fcm.googleapis.com/fcm/send", json=data_firebase, headers=headers)

                return True
        else:
            return None
        return False

    def points(self, number):
        result = self.__db.users.find_one({"phone.number": number})
        return str(result["amount"])

    def save_token(self, data):
        try:
            origin = self.__db.tokens.find_one({"phoneNumber":int(data["phoneNumber"])})
            print(origin)
            print(data)
            self.__db.tokens.update({"_id": origin["_id"]}, {"$set":{"token": data["token"]}} , upsert=False)
            return True
        except:
            return False