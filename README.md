# 🎛️ GPUQueue

A lightweight CLI + dashboard tool to help small AI teams **coordinate GPU usage** without confusion or conflict.

> 🔧 Built for teams tired of asking “who’s using GPU 0?”

---

## 🚀 Features

- ✅ View GPU usage status (free, in use, reserved)
- 📅 Soft-reserve GPUs for a set time period
- 🔔 Slack notifications when GPUs become free
- 🖥️ Streamlit dashboard for visual monitoring
- 🖥️ CLI interface for fast terminal access

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/gpuqueue.git
cd gpuqueue
pip install -r requirements.txt
```

---

## 🖥️ CLI Usage

```
# View current GPU status
python gpuqueue.py status

# Reserve GPU 0 for 2 hours
python gpuqueue.py reserve 0 --user alice --hours 2 --note "Training LLM"

# Release GPU 0 (only by the reserving user)
python gpuqueue.py release 0 --user alice
```
---

## 📊 Dashboard (Optional)
```
streamlit run dashboard.py
```
---

## 🔔 Slack Integration (Optional)
Get notified when a GPU becomes free!
Create a Slack Incoming Webhook.
Add the webhook URL to your environment:
```
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/your-webhook"
```
Now, when a GPU is released, your team will get a notification in Slack like:

🔔 GPU 2 is now available!
Last used by Bob. Use gpuqueue reserve 2 to claim it.

---

## 📁 File Structure
```
gpuqueue/
├── gpuqueue.py          # CLI tool
├── dashboard.py         # Streamlit dashboard UI
├── gpu_status.json      # Lightweight local status database
├── requirements.txt     # Python dependencies
├── .env.example         # Slack webhook template
└── README.md            # You're here
```

---

## 🤖 Dependencies
```
streamlit
requests
```

---

## 🧪 Example Output
```
$ python gpuqueue.py status
GPU 0: FREE     | User: -      | Until: -           | Note: -
GPU 1: RESERVED | User: alice  | Until: 2:45 PM     | Note: Training GPT-2
GPU 2: IN USE   | User: bob    | Until: 3:30 PM     | Note: Finetuning
GPU 3: FREE     | User: -      | Until: -           | Note: -
```

---

## 🌱 Roadmap (Optional / WIP)
 ⏹️ Add web-based reservation UI
 
 ⏹️ Add user authentication (Google login)
 
 ⏹️ Add time-based expiration + cleanup
 
 ⏹️ Dockerize the project
 
 ⏹️ Sync with GPU server via nvidia-smi + cron

---

## 🧑‍💻 Contributing
Pull requests welcome — especially for dashboard improvements or Slack/Discord integrations.

---

## 📫 Feedback / Contact
Built by Rajanit Navapara — feedback welcome via GitHub Issues or [rajanitnavapara9999@gmail.com].
Follow progress on X/Twitter or LinkedIn.
LinkedIn : https://www.linkedin.com/in/rajanit-navapara-285298135/
