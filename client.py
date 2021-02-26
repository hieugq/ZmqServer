import zmq
import threading


class ClientTask(threading.Thread):

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self) -> None:
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        # Id cho worker
        identity = u'woker-%s' % self.id
        socket.identity = identity.encode('ascii')
        # Ket noi den server
        socket.connect('tcp://localhost:5570')
        print(f'Client {identity} started')
        # Khai bao 1 poller co nhiem vu nhan cac reply tu server
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        reqs = 0
        #[b'R01', b'TraCuu', 'DSNhanVien', 'ALL']
        req = [b'R01', b'TraCuu', 'DSNhanVien', 'ALL']
        #while True:
        reqs += 1
        # gui request toi server voi id cua request tang dan
        print(f'Req {reqs} of client {self.id}')
        # socket.send_string(u'request #%d' % (reqs))
        #socket.send_multipart([b'{self.id}', str(req).encode('utf-8')])
        socket.send_string(req.__str__())
        # msg = [b'R01', b'TraCuu', b'DSNhanVien', 'ALL']
        # socket.send_string(msg.__str__())
        # Nhan message tu server
        for _ in range(5):
            sockets = dict(poller.poll(1000))
            if socket in sockets:
                msg = socket.recv()
                print(f'Client {identity} received: {msg}')
        socket.close()
        context.term()
