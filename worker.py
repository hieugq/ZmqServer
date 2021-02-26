import zmq
import threading
import time
import json
from random import randint


class Worker(threading.Thread):
    """ServerWorker"""

    def __init__(self, context):
        threading.Thread.__init__(self)
        self.context = context
        self.sentTimes = 0
        self.maxPackageSize = 2
        with open('user_list.json') as json_file:
            self.users_list = json.load(json_file)

    def run(self) -> None:
        worker = self.context.socket(zmq.DEALER)
        # Kết nối socket của backend để gửi và nhận dữ liệu từ nó
        worker.connect('inproc://backend')
        print('Worker started')
        # Cho nhung ket noi tu phia client
        while True:
            # nhan id worker va message tu server(HGQ - tu client)
            ident, msg = worker.recv_multipart()
            print('Worker received %s from %s' % (msg, ident))
            # Worker gui lai cho server so reply ngau nhien tu 0-4
            # replies = randint(0, 4)
            # for _ in range(replies):
            #     time.sleep(1. / (randint(1, 10)))
            #     worker.send_multipart([ident, msg])

            # Gui lai phan hoi cho client
            # "b[b'R01', b'TraCuu', b'DSNhanVien', 'ALL']"
            splain = msg.__str__().strip('b[]')
            lRes = [el for el in splain.split(',')]
            lRes.append(None)
            lRes.append(None)
            # contingent packages: phat sinh so luong goi tin ngau nhien
            # can phai gui lai cho phia client
            cont_pack_num = randint(1, len(self.users_list))
            self.sentTimes = 0

            print('So user can gui: %d - goi tin: %f' %(cont_pack_num, (cont_pack_num/self.maxPackageSize)))
            if cont_pack_num > self.maxPackageSize:
                # Gui tung goi tin cho den khi hoan thanh
                while cont_pack_num > (self.sentTimes * self.maxPackageSize):
                    fr = self.sentTimes * self.maxPackageSize
                    to = self.sentTimes * self.maxPackageSize + self.maxPackageSize
                    # Index of sending package
                    if to >= cont_pack_num:
                        to = cont_pack_num
                        i_package = -1
                    else:
                        i_package = self.sentTimes + 1
                    lRes[3] = i_package
                    lRes[4] = self.users_list[fr:to]
                    lRes[5] = 'SUCCESS'
                    worker.send_multipart([ident, lRes.__str__().encode('utf-8')])
                    self.sentTimes += 1

            elif cont_pack_num == self.maxPackageSize:
                lRes[3] = -1
                lRes[4] = self.users_list[0:self.maxPackageSize]
                lRes[5] = 'SUCCESS'
                worker.send_multipart([ident, lRes.__str__().encode('utf-8')])
            else:
                lRes[3] = -1
                lRes[4] = self.users_list[0:1]
                lRes[5] = 'SUCCESS'
                worker.send_multipart([ident, lRes.__str__().encode('utf-8')])

        worker.close()
