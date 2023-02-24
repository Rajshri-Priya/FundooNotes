import redis
import json

import self as self

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)


class RedisStore:

    def set(self, key, value):
        return redis_client.set(key, value)

    def get(self, key):
        return redis_client.get(key)
#

class RedisCrud:
    def __init__(self):
        self.redis = RedisStore()

    def save_note_in_redis(self, notes, user_id):
        notes_dict = self.redis.get(user_id)
        if notes_dict is None:
            notes_dict = {}
        else:
            notes_dict = json.loads(notes_dict)
        # notes_dict = {note['id']: note for note in notes_dict}
        note_id = notes.get('id')
        notes_dict.update({note_id: notes})
        self.redis.set(user_id, json.dumps(notes_dict))

    def get_notes_by_user_id(self, user):
        user_id = user.id
        notes_dict = json.loads(self.redis.get(str(user_id)))
        if notes_dict is None:
            return {}
        return notes_dict.values()

    def update_note_in_redis(self, note_id, new_note_data, user_id):
        notes_dict = self.redis.get(str(user_id))
        if notes_dict is None:
            return {}
        else:
            notes_dict = json.loads(notes_dict)
            n_id = str(note_id)
            if n_id in notes_dict.keys():
                notes_dict.update({n_id: new_note_data})
                self.redis.set(user_id, json.dumps(notes_dict))
                return True
        return False

    def delete_note_in_redis(self, note_id, user):
        user_id = str(user.id)
        notes_dict = self.redis.get(user_id)
        if notes_dict is not None:
            notes_dict = json.loads(notes_dict)
            note = notes_dict.get(str(note_id))
            if note:
                notes_dict.pop(str(note_id))
                self.redis.set(user_id, json.dumps(notes_dict))
