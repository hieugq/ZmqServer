from server import ServerTask
from client import ClientTask


def main() -> None:
    """main function"""
    server = ServerTask()
    server.start()
    # for i in range(3):
    #     client = ClientTask(i)
    #     client.start()
    server.join()


if __name__ == "__main__":
    main()
