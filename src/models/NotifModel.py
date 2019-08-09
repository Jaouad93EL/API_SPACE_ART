from . import mongo
from bson.objectid import ObjectId


class NotifModel:

    @staticmethod
    def init_by_user_id(user_id):
        return mongo.db.notif.insert_one({
            'user_id': user_id,
            'data': []
        })

    @staticmethod
    def get_all_notif_by_user_id(user_id):
        return mongo.db.notif.find({
            'user_id': user_id,
        })

    @staticmethod
    def save_notif_by_id_user(user_id, notif):
        return mongo.db.notif.update({
            "user_id": user_id,
        },
            {
                "$push": {
                    'data': {
                        '_id': ObjectId(),
                        'notif': notif
                    }
                }
            })

    @staticmethod
    def delete_all_notif_by_id_user(user_id):
        return mongo.db.notif.remove({
            'user_id': user_id
        })

    @staticmethod
    def delete_one_notif_by_notif_id_and_user_id(user_id, notif_id):
        return mongo.db.notif.update({
                "user_id": user_id,
            },
            {
                "$pull": {
                    'data': {
                        '_id': ObjectId(notif_id)
                    }
                }
            })


    @staticmethod
    def get_all():
        return mongo.db.notif.find()


    @staticmethod
    def test():
        return mongo.db.notif.remove({})

