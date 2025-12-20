
import os
import openai
import httpx
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
headers = {"Authorization": f"Bearer {api_key}"}

print("-" * 20)
print("TEST 1: requests library (verify=False)")
try:
    r = requests.get("https://api.openai.com/v1/models", headers=headers, verify=False, timeout=10)
    print(f"Requests Status: {r.status_code}")
    if r.status_code == 200:
        print("Requests SUCCESS!")
    else:
        print(f"Requests Failed: {r.text[:100]}")
except Exception as e:
    print(f"Requests Exception: {e}")

print("-" * 20)
print("TEST 2: httpx library (verify=False, http2=False)")
try:
    with httpx.Client(verify=False, http2=False) as client:
        r = client.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
        print(f"HTTPX Status: {r.status_code}")
        if r.status_code == 200:
            print("HTTPX SUCCESS!")
        else:
            print(f"HTTPX Failed: {r.text[:100]}")
except Exception as e:
    print(f"HTTPX Exception: {e}")

print("-" * 20)
