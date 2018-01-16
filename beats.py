__author__ = 'zach barr'
import zmq

def get_active():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://e7heartbeat:5589")
    zmqfilter = u""
    socket.setsockopt_string(zmq.SUBSCRIBE, zmqfilter)

    inbound_data = socket.recv_string()
    res = []

    for line in inbound_data.splitlines():
        words = line.split()
        host = str(words.pop(0))
        if "concord" in host:
            host = host.split(".")[0]
        app = ' '.join(words)
        res.append(host + ":" + app)
    return res

if __name__ == "__main__":
    x = get_active()
    import pprint
    pprint.pprint(x)
