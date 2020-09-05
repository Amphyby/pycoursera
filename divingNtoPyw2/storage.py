import argparse

if __name__ == '__main__':
    storage = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str)
    parser.add_argument("--value", type=str)
    args = parser.parser_args()
    if args.key and args.value:
        pass
    elif args.key:
        pass
    elif args.value:
        pass