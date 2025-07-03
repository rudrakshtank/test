import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Codeforces Submission Viewer", layout="centered")
st.title("📦 Codeforces Submission Code Viewer")

url = st.text_input("Enter Codeforces Submission URL", placeholder="https://codeforces.com/contest/1872/submission/231399139")

def extract_code(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        code_lines = soup.select("pre#program-source-text ol.linenums > li")

        if not code_lines:
            return None, "❌ Could not find code lines. Check the URL or submission page structure."

        code = "\n".join([line.get_text() for line in code_lines])
        return code, None

    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"

if url:
    if not url.startswith("https://codeforces.com/contest/") or "/submission/" not in url:
        st.warning("🚫 Invalid Codeforces submission URL format.")
    else:
        with st.spinner("Fetching submission code..."):
            code, error = extract_code(url)

        if error:
            st.error(error)
        else:
            st.success("✅ Code fetched successfully:")
            st.code(code, language="cpp")
