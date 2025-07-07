import streamlit as st
from pathlib import Path

# Attempt to import the core evaluation system.
try:
    from teacher_evaluation_ai.main import TeacherEvaluationSystem
    CORE_AVAILABLE = True
except ModuleNotFoundError:
    CORE_AVAILABLE = False
    st.warning("teacher_evaluation_ai package not found. Core analysis will be disabled.")

st.set_page_config(page_title="AI Teacher Evaluation", layout="wide")
st.title("📊 AI-Driven Teacher Evaluation System")

st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Choose input mode", ("Upload Lesson Recording", "Real-time Webcam"))

MAX_DURATION = st.sidebar.slider("Max analysis duration (minutes)", 1, 60, 30)
FRAME_STRIDE = st.sidebar.slider("Frame stride (every N frames)", 1, 30, 5)

if "results" not in st.session_state:
    st.session_state.results = None

if mode == "Upload Lesson Recording":
    video_file = st.file_uploader("Upload lesson video (MP4)", type=["mp4", "mov", "mkv"])
    if st.button("Run Analysis") and video_file and CORE_AVAILABLE:
        with st.spinner("Processing lesson… this may take a while 🕒"):
            tmp_path = Path("uploaded_video.mp4")
            tmp_path.write_bytes(video_file.read())
            system = TeacherEvaluationSystem()
            st.session_state.results = system.analyze_lesson(str(tmp_path), max_duration_minutes=MAX_DURATION, frame_stride=FRAME_STRIDE)
        st.success("Analysis complete!")
elif mode == "Real-time Webcam" and CORE_AVAILABLE:
    if st.button("Start webcam analysis"):
        with st.spinner("Analysing webcam feed… press Q in the opened window to quit"):
            system = TeacherEvaluationSystem()
            st.session_state.results = system.analyze_real_time(camera_index=0, max_duration_minutes=MAX_DURATION)
        st.success("Analysis complete!")

# Display results if available
if st.session_state.results:
    results = st.session_state.results
    rubric = results.get("rubric_evaluation", {})
    overall = rubric.get("overall_score", 0)
    st.metric("Overall Effectiveness", f"{overall*100:.0f}%")

    # Category breakdown
    category_scores = rubric.get("category_scores", {})
    if category_scores:
        import pandas as pd
        df = pd.DataFrame({"Category": [c.replace("_", " ").title() for c in category_scores.keys()],
                           "Score %": [round(v.get("score",0)*100,1) for v in category_scores.values()]})
        st.bar_chart(df.set_index("Category"))

    # Strengths & improvements
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌟 Strengths")
        for s in rubric.get("strengths", []) or ["No strengths detected"]:
            st.write(f"✔️ {s}")
    with col2:
        st.subheader("🛠️ Areas for Improvement")
        for s in rubric.get("areas_for_improvement", []) or ["No issues detected"]:
            st.write(f"❌ {s}")

    # Recommendations
    recs = rubric.get("recommendations", [])
    if recs:
        st.subheader("💡 Recommendations")
        for i, r in enumerate(recs, 1):
            st.write(f"{i}. {r}")

    # Download buttons
    report = results.get("report", {}) or results.get("report_generation", {})
    if report:
        html_bytes = report.get("html", "").encode()
        text_bytes = report.get("text", "").encode()
        st.download_button("Download HTML report", data=html_bytes, file_name="evaluation_report.html", mime="text/html")
        st.download_button("Download text report", data=text_bytes, file_name="evaluation_report.txt", mime="text/plain")
else:
    st.info("Upload a video or start real-time analysis to see results.")
