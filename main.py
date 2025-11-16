import argparse
import os
from agent import answer_offline, answer_online


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["online", "offline"], required=False,
                        help="Operation mode. If omitted, will attempt to read AGENT_MODE env var.")
    parser.add_argument("query", type=str)
    args = parser.parse_args()

    mode = args.mode or os.getenv("AGENT_MODE")
    if not mode:
        parser.error("Missing --mode and AGENT_MODE environment variable. Specify one.")

    if mode == "offline":
        print(answer_offline(args.query))
    else:
        print(answer_online(args.query))


if __name__ == "__main__":
    main()
