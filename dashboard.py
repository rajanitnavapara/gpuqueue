# # dashboard.py

# import streamlit as st
# import json
# from datetime import datetime
# import os

# DATA_FILE = "gpu_status.json"

# def load_data():
#     if not os.path.exists(DATA_FILE):
#         st.error("GPU data file not found.")
#         return {}
#     with open(DATA_FILE, "r") as f:
#         return json.load(f)

# st.title("🎛️ GPUQueue Dashboard")

# data = load_data()
# if not data:
#     st.stop()

# for gpu_id, info in data.items():
#     col1, col2 = st.columns([1, 4])
#     with col1:
#         st.markdown(f"### GPU {gpu_id}")
#         status_color = "green" if info["status"] == "free" else "red"
#         st.markdown(f"<span style='color:{status_color}; font-weight:bold'>{info['status'].upper()}</span>", unsafe_allow_html=True)
#     with col2:
#         st.write(f"**User:** {info['user'] or '—'}")
#         st.write(f"**Until:** {info['until'] or '—'}")
#         st.write(f"**Note:** {info['note'] or '—'}")
#         if info["status"] == "free":
#             if st.button(f"Reserve GPU {gpu_id}"):
#                 st.warning("Reservation feature in UI coming soon.")
#         else:
#             if st.button(f"Release GPU {gpu_id}"):
#                 st.warning("Release feature in UI coming soon.")
# dashboard.py

import streamlit as st
import json
from datetime import datetime, timedelta
import os
import requests

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DATA_FILE = "gpu_status.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        st.error("GPU data file not found.")
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

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



st.title("🎛️ GPUQueue Dashboard")

data = load_data()
if not data:
    st.stop()

st.markdown("---")

for gpu_id, info in data.items():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"### GPU {gpu_id}")
        status_color = "green" if info["status"] == "free" else "red"
        st.markdown(f"<span style='color:{status_color}; font-weight:bold'>{info['status'].upper()}</span>", unsafe_allow_html=True)

    with col2:
        st.write(f"**User:** {info['user'] or '—'}")
        st.write(f"**Until:** {info['until'] or '—'}")
        st.write(f"**Note:** {info['note'] or '—'}")

        if info["status"] == "free":
            with st.expander(f"Reserve GPU {gpu_id}"):
                with st.form(key=f"reserve_form_{gpu_id}"):
                    user = st.text_input("Your name", key=f"user_{gpu_id}")
                    hours = st.number_input("Duration (in hours)", min_value=1, max_value=24, value=1, key=f"hours_{gpu_id}")
                    note = st.text_input("Reservation note (optional)", key=f"note_{gpu_id}")
                    submit = st.form_submit_button("Reserve")

                    if submit:
                        if not user.strip():
                            st.error("User name is required.")
                        else:
                            end_time = (datetime.now() + timedelta(hours=hours)).isoformat()
                            data[gpu_id].update({
                                "status": "reserved",
                                "user": user.strip(),
                                "until": end_time,
                                "note": note.strip()
                            })
                            save_data(data)
                            st.success(f"GPU {gpu_id} reserved by {user} for {hours} hour(s).")
                            st.rerun()
        else:
            with st.expander(f"Release GPU {gpu_id}"):
                with st.form(key=f"release_form_{gpu_id}"):
                    user = st.text_input("Your name", key=f"release_user_{gpu_id}")
                    submit = st.form_submit_button("Release")

                    if submit:
                        if user.strip() != info["user"]:
                            st.error("You can only release GPUs you reserved.")
                        else:
                            data[gpu_id].update({
                                "status": "free",
                                "user": None,
                                "until": None,
                                "note": ""
                            })
                            save_data(data)
                            send_slack_notification(gpu_id)
                            st.success(f"GPU {gpu_id} released.")
                            st.rerun()
st.markdown("---")
st.write("This dashboard allows you to view and manage GPU reservations. Use the forms to reserve or release GPUs as needed.")
# Note: This code assumes that the JSON file `gpu_status.json` exists and is structured correctly.
