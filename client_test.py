from client import ClientTask


def main() -> None:
	client = ClientTask(0)
	client.start()


if __name__ == '__main__':
	main()