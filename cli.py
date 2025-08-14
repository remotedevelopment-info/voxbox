# cli.py
import argparse
import requests

API_URL = "http://localhost:8000"

def list_voices():
    """Fetch and display available voices."""
    r = requests.get(f"{API_URL}/voices")
    for v in r.json():
        print(f"{v['id']}: {v['name']} - {v['description']}")

def send_question(mode, question):
    """Send a question to the API and print the response."""
    payload = {"mode_id": mode, "prompt": question}
    r = requests.post(f"{API_URL}/chat", json=payload)
    if r.status_code == 200:
        print(r.json()["response"])
    else:
        print(f"Error: {r.status_code} - {r.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vox Box CLI")
    parser.add_argument("--list", action="store_true", help="List available voices")
    parser.add_argument("--mode", type=str, help="Mode ID to use")
    parser.add_argument("--question", type=str, help="Question to send")
    args = parser.parse_args()

    if args.list:
        list_voices()
    elif args.mode and args.question:
        send_question(args.mode, args.question)
    else:
        parser.print_help()