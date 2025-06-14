# gpuqueue.py

import json
import argparse
import os
from datetime import datetime, timedelta
import requests


SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
DATA_FILE = "gpu_status.json"
NUM_GPUS = 4

def load_data():
    if not os.path.exists(DATA_FILE):
        return {str(i): {"status": "free", "user": None, "until": None, "note": ""} for i in range(NUM_GPUS)}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    # Add missing GPUs if NUM_GPUS increased
    for i in range(NUM_GPUS):
        if str(i) not in data:
            data[str(i)] = {"status": "free", "user": None, "until": None, "note": ""}
    # Remove extra GPUs if NUM_GPUS decreased
    keys_to_remove = [k for k in data if int(k) >= NUM_GPUS]
    for k in keys_to_remove:
        del data[k]
    # Save updated data if changed
    if keys_to_remove or any(str(i) not in data for i in range(NUM_GPUS)):
        save_data(data)
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def status():
    data = load_data()
    for gpu, info in data.items():
        status = info["status"]
        user = info["user"] or "-"
        until = info["until"] or "-"
        note = info["note"]
        print(f"GPU {gpu}: {status.upper()} | User: {user} | Until: {until} | Note: {note}")

def reserve(gpu_id, user, hours, note):
    data = load_data()
    gpu = data[str(gpu_id)]

    if gpu["status"] != "free":
        print(f"GPU {gpu_id} is not available.")
        return

    end_time = (datetime.now() + timedelta(hours=hours)).isoformat()
    gpu.update({"status": "reserved", "user": user, "until": end_time, "note": note})
    save_data(data)
    print(f"GPU {gpu_id} reserved by {user} for {hours} hour(s).")

def release(gpu_id, user):
    data = load_data()
    gpu = data[str(gpu_id)]

    if gpu["user"] != user:
        print("You can only release GPUs you reserved.")
        return

    gpu.update({"status": "free", "user": None, "until": None, "note": ""})
    save_data(data)
    print(f"GPU {gpu_id} released.")

def send_slack_notification(gpu_id):
    if not SLACK_WEBHOOK_URL:
        return

    message = {
        "text": f"🔔 *GPU {gpu_id} is now available!* Use `gpuqueue reserve {gpu_id}` to claim it."
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=message)
    except Exception as e:
        print(f"Slack notification failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPUQueue CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_status = subparsers.add_parser("status")

    parser_reserve = subparsers.add_parser("reserve")
    parser_reserve.add_argument("gpu_id", type=int, choices=range(NUM_GPUS), help="GPU ID to reserve (0-3)")
    parser_reserve.add_argument("--user", required=True)
    parser_reserve.add_argument("--hours", type=int, default=1)
    parser_reserve.add_argument("--note", default="")

    parser_release = subparsers.add_parser("release")
    parser_release.add_argument("gpu_id", type=int)
    parser_release.add_argument("--user", required=True)

    args = parser.parse_args()

    if args.command == "status":
        status()
    elif args.command == "reserve":
        reserve(args.gpu_id, args.user, args.hours, args.note)
    elif args.command == "release":
        release(args.gpu_id, args.user)
        # Send Slack notification if the GPU is released
        send_slack_notification(args.gpu_id)
    else:
        parser.print_help()
