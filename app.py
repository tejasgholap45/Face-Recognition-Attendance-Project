"""
Streamlit Face Recognition Attendance System
Main application file
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import tempfile
import os
from pathlib import Path

from face_recognition_system import FaceRecognitionSystem
from attendance_manager import AttendanceManager


# Page configuration
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'face_system' not in st.session_state:
    st.session_state.face_system = FaceRecognitionSystem()
    st.session_state.attendance_manager = AttendanceManager()
    st.session_state.camera_active = False


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">👤 Face Recognition Attendance System</div>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["🏠 Home", "✅ Mark Attendance", "📊 View Attendance", "➕ Register New Face", "⚙️ Settings"]
    )
    
    # Display current date and time
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**📅 Date:** {datetime.now().strftime('%Y-%m-%d')}")
    st.sidebar.markdown(f"**🕐 Time:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Display registered users count
    known_names = st.session_state.face_system.get_known_names()
    st.sidebar.markdown(f"**👥 Registered Users:** {len(known_names)}")
    
    # Route to selected page
    if page == "🏠 Home":
        show_home_page()
    elif page == "✅ Mark Attendance":
        show_mark_attendance_page()
    elif page == "📊 View Attendance":
        show_view_attendance_page()
    elif page == "➕ Register New Face":
        show_register_face_page()
    elif page == "⚙️ Settings":
        show_settings_page()


def show_home_page():
    """Display home page"""
    st.header("Welcome to Face Recognition Attendance System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**✅ Mark Attendance**\n\nUse your webcam to automatically mark attendance")
    
    with col2:
        st.info("**📊 View Records**\n\nView daily and historical attendance records")
    
    with col3:
        st.info("**➕ Register Faces**\n\nAdd new people to the system")
    
    st.markdown("---")
    
    # Display today's attendance summary
    st.subheader("📋 Today's Attendance Summary")
    today_attendance = st.session_state.attendance_manager.get_today_attendance()
    
    if not today_attendance.empty:
        st.dataframe(today_attendance, use_container_width=True)
        st.success(f"**Total Present Today:** {len(today_attendance)}")
    else:
        st.info("No attendance marked yet today.")
    
    # Display registered users
    st.markdown("---")
    st.subheader("👥 Registered Users")
    known_names = st.session_state.face_system.get_known_names()
    
    if known_names:
        cols = st.columns(4)
        for idx, name in enumerate(sorted(known_names)):
            with cols[idx % 4]:
                st.markdown(f"✓ {name}")
    else:
        st.warning("No users registered yet. Please register faces to start using the system.")


def show_mark_attendance_page():
    """Display mark attendance page with camera"""
    st.header("✅ Mark Attendance")
    
    st.info("📸 Position your face in front of the camera and click 'Take Photo'.")
    
    # Camera input
    img_file_buffer = st.camera_input("Take a photo to mark attendance", key="attendance_camera")
    
    status_placeholder = st.empty()
    
    if img_file_buffer is not None:
        # Convert the file buffer to an opencv image
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Recognize faces
        face_results = st.session_state.face_system.recognize_faces(cv2_img)
        
        # Draw faces on frame (optional, for display)
        frame_with_faces = st.session_state.face_system.draw_faces(cv2_img.copy(), face_results)
        
        # Display the processed image
        st.image(frame_with_faces, channels="BGR", caption="Processed Image", use_container_width=True)
        
        # Check for recognized faces and mark attendance
        marked_any = False
        for result in face_results:
            if result['name'] != "Unknown" and result['confidence'] > 0.5:
                # Try to mark attendance
                attendance_result = st.session_state.attendance_manager.mark_attendance(
                    result['name']
                )
                
                if attendance_result['success']:
                    st.success(
                        f"✅ Attendance marked for **{result['name']}** at {attendance_result['time']}"
                    )
                    marked_any = True
                else:
                    st.info(
                        f"ℹ️ {result['name']}: {attendance_result['message']}"
                    )
                    marked_any = True
        
        if not marked_any:
            if not face_results:
                st.warning("❌ No face detected. Please try again.")
            else:
                st.warning("❌ Face not recognized. Please register first or try again.")


def show_view_attendance_page():
    """Display attendance records page"""
    st.header("📊 View Attendance Records")
    
    # Date selector
    col1, col2 = st.columns([2, 3])
    
    with col1:
        selected_date = st.date_input(
            "Select Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    date_str = selected_date.strftime("%Y-%m-%d")
    
    # Get attendance for selected date
    attendance_df = st.session_state.attendance_manager.get_attendance_by_date(date_str)
    
    st.markdown("---")
    
    if not attendance_df.empty:
        st.success(f"**Total Present on {date_str}:** {len(attendance_df)}")
        st.dataframe(attendance_df, use_container_width=True)
        
        # Download button
        csv = attendance_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"attendance_{date_str}.csv",
            mime="text/csv"
        )
    else:
        st.info(f"No attendance records found for {date_str}")
    
    # Show all available dates
    st.markdown("---")
    st.subheader("📅 Available Attendance Records")
    
    all_dates = st.session_state.attendance_manager.get_all_attendance_dates()
    
    if all_dates:
        st.write(f"Records available for {len(all_dates)} days:")
        cols = st.columns(5)
        for idx, date in enumerate(all_dates[:20]):  # Show last 20 dates
            with cols[idx % 5]:
                st.markdown(f"📄 {date}")
    else:
        st.info("No attendance records available yet.")


def show_register_face_page():
    """Display register new face page"""
    st.header("➕ Register New Face")
    
    st.info("📝 Enter the person's name and capture their face using the camera.")
    
    # Name input
    person_name = st.text_input("Person's Name", placeholder="Enter full name")
    
    if person_name:
        st.markdown("---")
        st.subheader(f"📸 Capture Photo for {person_name}")
        
        # Initialize session state for registration
        if 'reg_captured_count' not in st.session_state:
            st.session_state.reg_captured_count = 0
            
        # Camera input
        img_file_buffer = st.camera_input("Take a photo to register", key="register_camera")
        
        if img_file_buffer is not None:
            # Convert the file buffer to an opencv image
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Save face
            success = st.session_state.face_system.save_face_from_frame(
                person_name, 
                cv2_img
            )
            
            if success:
                st.success(f"✅ Photo captured successfully for {person_name}!")
                st.balloons()
                # Optional: Clear the name or reset state if needed, 
                # but for now we just show success.
                # To allow multiple photos, we'd need a more complex flow with st.camera_input 
                # (since it retains the last image), but for basic registration one good photo is often enough 
                # or the user can retake.
                
                # If we want to force a "reset" of the camera input, it's tricky in Streamlit without rerunning.
                # But the user can just take another photo.
            else:
                st.error("❌ No face detected in the frame. Please try again.")


def show_settings_page():
    """Display settings page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔄 System Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reload Known Faces", use_container_width=True):
            st.session_state.face_system.load_known_faces()
            st.success("✅ Known faces reloaded successfully!")
    
    with col2:
        if st.button("📊 Show System Info", use_container_width=True):
            st.info(f"""
            **System Information:**
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
    st.markdown("""
    **Face Recognition Attendance System v1.0**
    
    A fully functional face recognition-based attendance system built with:
    - Streamlit for web interface
    - OpenCV for camera handling
    - face_recognition library for face detection and recognition
    - pandas & openpyxl for Excel integration
    
    Features:
    - ✅ Automatic attendance marking
    - 📊 Daily Excel reports
    - 👥 Easy face registration
    - 🚫 Duplicate prevention
    - 📈 Attendance history
    """)


if __name__ == "__main__":
    main()
