import argparse
from agent import answer_offline, answer_online

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["online", "offline"], required=True)
    parser.add_argument("query", type=str)
    args = parser.parse_args()

    if args.mode == "offline":
        print(answer_offline(args.query))
    else:
        print(answer_online(args.query))


if __name__ == "__main__":
    main()
