from . import mongo
from bson.objectid import ObjectId


class PrivateModel:

    @staticmethod
    def new_private_conversation(li_user, message):
        return mongo.db.private.insert_one({'users': li_user, 'data': [message]})

    @staticmethod
    def get_one_private_conversation_by_li_user(li_user):
        return mongo.db.private.find({
            'users': {
                "$all": li_user,
                "$size": len(li_user)
            }
        })

    @staticmethod
    def get_one_private_conversation_by_id_conv(id_conv):
        return mongo.db.private.find({
            '_id': ObjectId(id_conv)
        })

    @staticmethod
    def add_one_private_message_in_conversation(id_conv, message):
        return mongo.db.private.update({
            "_id": ObjectId(id_conv),
        },
            {"$push": {'data': message}}
        )

    @staticmethod
    def leave_private_conversation(user_id, id_conv):
        return mongo.db.private.update({
            "_id": ObjectId(id_conv),
        },
            {
                "$pull": {
                    'users': user_id
                }
            }
        )

    @staticmethod
    def get_all():
        return mongo.db.private.find()

    @staticmethod
    def get_all_private_conversion_by_user_id(user_id):
        return mongo.db.private.find({
                'users': {
                    "$all": user_id,
                }
            },
            {
                'data': {
                    "$slice": -1
                }
            })

    @staticmethod
    def test():
        return mongo.db.private.remove({})

