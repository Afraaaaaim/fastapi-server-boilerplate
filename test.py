import requests
import json

# ─── CONSTANTS ───────────────────────────────────────────────
PHONE_NUMBER_ID = "1126190603915708"
ACCESS_TOKEN    = "EAAMPAeTvVagBRrDAdUpNVBCb5hayCpRsIomy48kepVNvIZBctjqlFgtlqKkVI9yQSl2ZCfUPUzrZBZA5t4Mx751nH7ZAvEHJWdgoEzdyTqqZBoq4lrcwHKsjQDWnyfTztbjFQRLTBtaDzXKlybc3Ps1bZCQWSUneIrZCpLUZBQEEXwgS10BlPueXaOd0HoRHd5AZDZD"
RECIPIENT_PHONE = "971551780854"  # E.164 format, no +
MESSAGE_TEXT    = "Hello! Testing outbound message from aldar.."
# ─────────────────────────────────────────────────────────────

API_VERSION = "v21.0"
URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

PAYLOAD = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {
        "preview_url": False,
        "body": MESSAGE_TEXT,
    },
}

print("=" * 60)
print("WABA Message Send Test")
print("=" * 60)
print(f"URL     : {URL}")
print(f"To      : {RECIPIENT_PHONE}")
print(f"Message : {MESSAGE_TEXT}")
print(f"Payload : {json.dumps(PAYLOAD, indent=2)}")
print("-" * 60)

try:
    response = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=10)

    print(f"Status Code : {response.status_code}")
    print(f"Headers     : {dict(response.headers)}")

    try:
        response_json = response.json()
        print(f"Response    : {json.dumps(response_json, indent=2)}")
    except json.JSONDecodeError:
        print(f"Response (raw): {response.text}")

    response.raise_for_status()
    print("-" * 60)
    print("✅ Message sent successfully!")
    print(f"Message ID  : {response_json.get('messages', [{}])[0].get('id', 'N/A')}")

except requests.exceptions.HTTPError as e:
    print("-" * 60)
    print(f"❌ HTTP Error: {e}")
except requests.exceptions.ConnectionError as e:
    print("-" * 60)
    print(f"❌ Connection Error: {e}")
except requests.exceptions.Timeout:
    print("-" * 60)
    print("❌ Request timed out after 10 seconds.")
except requests.exceptions.RequestException as e:
    print("-" * 60)
    print(f"❌ Unexpected request error: {e}")

print("=" * 60)