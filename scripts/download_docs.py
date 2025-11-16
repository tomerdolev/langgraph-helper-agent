from pathlib import Path
import requests

URLS = {
    "langgraph_llms.txt": "https://langchain-ai.github.io/langgraph/llms.txt",
    "langgraph_llms_full.txt": "https://langchain-ai.github.io/langgraph/llms-full.txt",
    "langchain_llms.txt": "https://python.langchain.com/llms.txt",
}

def main():
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "agent" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    for name, url in URLS.items():
        print(f"Downloading {name} from {url} ...")
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        (data_dir / name).write_text(resp.text, encoding="utf-8")
        print(f"Saved to {data_dir / name}")

    print("\nDone. Local docs are ready for offline mode.")

if __name__ == "__main__":
    main()
