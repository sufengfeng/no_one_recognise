import json


class MessageType:
    def __init__(self, message_id, role, v_x, v_y, shut, speed):
        self.message_id = message_id
        self.role = role
        self.v_x = v_x
        self.v_y = v_y
        self.shut = shut
        self.speed = speed


def MessageType2dict(msg):
    return {
        'message_id': msg.message_id,
        'role': msg.role,
        'v_x': msg.v_x,
        'v_y': msg.v_y,
        'shut': msg.shut,
        'speed': msg.speed
    }


def dict2MessageType(d):
    return MessageType(d['message_id'], d['role'], d['v_x'], d['v_y'], d['shut'],
                       d['speed'])


if __name__ == "__main__":
    s = MessageType("132", "2", "3", "4", "5", "6")
    json_str = json.dumps(s, default=MessageType2dict)
    print(json_str)
    message = json.loads(json_str, object_hook=dict2MessageType)
    print(message.message_id)
