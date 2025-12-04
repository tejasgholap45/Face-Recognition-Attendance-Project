"""
Professional Streamlit Face Recognition Attendance System
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

from face_recognition_system import FaceRecognitionSystem
from attendance_manager import AttendanceManager

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for professional styling
# -----------------------------
st.markdown("""
    <style>
    .main-header {font-size:2.5rem; font-weight:bold; color:#1f77b4; text-align:center; margin-bottom:2rem;}
    .success-box {padding:1rem; border-radius:0.5rem; background-color:#d4edda; border:1px solid #c3e6cb; color:#155724; margin:1rem 0;}
    .error-box {padding:1rem; border-radius:0.5rem; background-color:#f8d7da; border:1px solid #f5c6cb; color:#721c24; margin:1rem 0;}
    .info-box {padding:1rem; border-radius:0.5rem; background-color:#d1ecf1; border:1px solid #bee5eb; color:#0c5460; margin:1rem 0;}
    .sidebar-header {font-size:1.2rem; font-weight:bold; color:#333;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Initialize session state
# -----------------------------
if 'face_system' not in st.session_state:
    st.session_state.face_system = FaceRecognitionSystem()
    st.session_state.attendance_manager = AttendanceManager()
    st.session_state.camera_active = False

# -----------------------------
# Developer Info
# -----------------------------
DEVELOPER_NAME = "Tejas Gholap"
DEVELOPER_ROLE = "Data analyst"
Linkdin = "https://www.linkedin.com/in/tejas-gholap-bb3417300/"
GITHUB_URL = "https://github.com/tejasgholap45/Face-Recognition-Attendance-Project"

# -----------------------------
# Main Function
# -----------------------------
def main():
    st.markdown(f'<div class="main-header">👤 Face Recognition Attendance System</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown(f"<div class='sidebar-header'>👨‍💻 Developer Info</div>", unsafe_allow_html=True)
    st.sidebar.text(f"Name: {Tejas Gholap}")
    st.sidebar.text(f"Role: {Data Analyst}")
    st.sidebar.text(f"Linkdin: {https://www.linkedin.com/in/tejas-gholap-bb3417300/}")
    st.sidebar.markdown(f"[GitHub Repo]({https://github.com/tejasgholap45/Face-Recognition-Attendance-Project})")

    st.sidebar.markdown("---")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["🏠 Home", "✅ Mark Attendance", "📊 View Attendance", "➕ Register Face", "⚙️ Settings"])

    # Sidebar extra info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**📅 Date:** {datetime.now().strftime('%Y-%m-%d')}")
    st.sidebar.markdown(f"**🕐 Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.sidebar.markdown(f"**👥 Registered Users:** {len(st.session_state.face_system.get_known_names())}")

    # Route page
    if page == "🏠 Home":
        show_home_page()
    elif page == "✅ Mark Attendance":
        show_mark_attendance_page()
    elif page == "📊 View Attendance":
        show_view_attendance_page()
    elif page == "➕ Register Face":
        show_register_face_page()
    elif page == "⚙️ Settings":
        show_settings_page()

# -----------------------------
# Home Page
# -----------------------------
def show_home_page():
    st.header("Welcome to Face Recognition Attendance System")

    col1, col2, col3 = st.columns(3)
    col1.info("✅ Mark Attendance\nUse your webcam to mark attendance automatically")
    col2.info("📊 View Records\nCheck daily & historical attendance")
    col3.info("➕ Register Faces\nAdd new people to the system")

    st.markdown("---")
    st.subheader("📋 Today's Attendance Summary")
    today_attendance = st.session_state.attendance_manager.get_today_attendance()

    if not today_attendance.empty:
        st.dataframe(today_attendance, use_container_width=True)
        st.success(f"**Total Present Today:** {len(today_attendance)}")
    else:
        st.info("No attendance marked yet today.")

    st.markdown("---")
    st.subheader("👥 Registered Users")
    known_names = st.session_state.face_system.get_known_names()
    if known_names:
        cols = st.columns(4)
        for idx, name in enumerate(sorted(known_names)):
            with cols[idx % 4]:
                st.markdown(f"✓ {name}")
    else:
        st.warning("No users registered yet.")

# -----------------------------
# Mark Attendance Page
# -----------------------------
def show_mark_attendance_page():
    st.header("✅ Mark Attendance")
    st.info("📸 Position your face and click 'Take Photo'.")

    img_file = st.camera_input("Take Photo")
    if img_file:
        bytes_data = img_file.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        face_results = st.session_state.face_system.recognize_faces(cv2_img)
        frame_with_faces = st.session_state.face_system.draw_faces(cv2_img.copy(), face_results)
        st.image(frame_with_faces, channels="BGR", caption="Processed Image", use_container_width=True)

        marked_any = False
        for result in face_results:
            if result['name'] != "Unknown" and result['confidence'] > 0.5:
                attendance_result = st.session_state.attendance_manager.mark_attendance(result['name'])
                if attendance_result['success']:
                    st.success(f"✅ Attendance marked for **{result['name']}** at {attendance_result['time']}")
                    marked_any = True
                else:
                    st.info(f"ℹ️ {result['name']}: {attendance_result['message']}")
                    marked_any = True
        if not marked_any:
            if not face_results:
                st.warning("❌ No face detected. Try again.")
            else:
                st.warning("❌ Face not recognized. Register first.")

# -----------------------------
# View Attendance Page
# -----------------------------
def show_view_attendance_page():
    st.header("📊 View Attendance Records")

    selected_date = st.date_input("Select Date", value=datetime.now(), max_value=datetime.now())
    date_str = selected_date.strftime("%Y-%m-%d")
    attendance_df = st.session_state.attendance_manager.get_attendance_by_date(date_str)

    st.markdown("---")
    if not attendance_df.empty:
        st.success(f"**Total Present on {date_str}:** {len(attendance_df)}")
        st.dataframe(attendance_df, use_container_width=True)
        st.download_button("📥 Download as CSV", attendance_df.to_csv(index=False),
                           file_name=f"attendance_{date_str}.csv", mime="text/csv")
    else:
        st.info(f"No attendance records for {date_str}")

    st.markdown("---")
    st.subheader("📅 Available Attendance Records")
    all_dates = st.session_state.attendance_manager.get_all_attendance_dates()
    if all_dates:
        cols = st.columns(5)
        for idx, date in enumerate(all_dates[:20]):
            with cols[idx % 5]:
                st.markdown(f"📄 {date}")
    else:
        st.info("No attendance records yet.")

# -----------------------------
# Register Face Page
# -----------------------------
def show_register_face_page():
    st.header("➕ Register New Face")
    st.info("📝 Enter the person's name and capture their face.")

    person_name = st.text_input("Person's Name", placeholder="Enter full name")
    if person_name:
        img_file = st.camera_input(f"Take a photo for {person_name}")
        if img_file:
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            success = st.session_state.face_system.save_face_from_frame(person_name, cv2_img)
            if success:
                st.success(f"✅ Photo captured successfully for {person_name}!")
                st.balloons()
            else:
                st.error("❌ No face detected. Try again.")

# -----------------------------
# Settings Page
# -----------------------------
def show_settings_page():
    st.header("⚙️ Settings")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reload Known Faces"):
            st.session_state.face_system.load_known_faces()
            st.success("✅ Known faces reloaded successfully!")
    with col2:
        if st.button("📊 Show System Info"):
            st.info(f"""
**System Info**
- Registered Users: {len(st.session_state.face_system.get_known_names())}
- Total Face Encodings: {len(st.session_state.face_system.known_face_encodings)}
- Attendance Records: {len(st.session_state.attendance_manager.get_all_attendance_dates())} days
            """)

    st.markdown("---")
    st.subheader("📁 Directory Paths")
    st.code(f"Known Faces: {Path('known_faces').absolute()}")
    st.code(f"Attendance Files: {Path('attendance').absolute()}")

    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown(f"""
**Face Recognition Attendance System v1.0**

Built by: **{DEVELOPER_NAME}** — {DEVELOPER_ROLE}  
Email: {DEVELOPER_EMAIL}  
GitHub: [{GITHUB_URL}]({GITHUB_URL})

Features:
- ✅ Automatic attendance marking
- 📊 Daily Excel reports
- 👥 Easy face registration
- 🚫 Duplicate prevention
- 📈 Attendance history
    """)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    main()
