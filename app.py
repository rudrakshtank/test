import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Codeforces Submission Viewer", layout="centered")
st.title("📦 Codeforces Submission Code Viewer")

url = st.text_input("Enter Codeforces Submission URL", placeholder="https://codeforces.com/contest/1807/submission/327055474")

def extract_code(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Referer": "https://codeforces.com/",
        }

        session = requests.Session()
        proxy_url = f"https://corsproxy.io/?{url}"
        res = session.get(proxy_url, headers=headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        code_lines = soup.select("pre#program-source-text ol.linenums > li")

        if not code_lines:
            return None, "❌ Could not find code lines. Is the submission public?"

        code = "\n".join([line.get_text() for line in code_lines])
        return code, None

    except requests.exceptions.HTTPError as http_err:
        return None, f"🚫 HTTP Error: {http_err}"
    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"

