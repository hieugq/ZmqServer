import zmq
import threading
from worker import Worker
from worker import Worker


class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        context = zmq.Context()
        #tao mot lien ket tai tcp://*:5570 de client ket noi den no
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')
        # tao mot lien ket tai inproc://backend de cho worker ket noi
        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')
        # Chay 5 worker co nhiem vu nhan message tu client
        workers = list()
        for _ in range(5):
            w = Worker(context)
            w.start()
            workers.append(w)
        # Ket noi frontend va backend
        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()