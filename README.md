# Face Recognition Attendance System

A professional and fully functional **face recognition-based attendance system** built with Streamlit that automatically records daily attendance in Excel sheets.

**Live Demo:** [Try it here](https://face-recognition-attendance-project-vvdtejas-gholap.streamlit.app/)

---

## 🚀 Features

- 👤 **Face Recognition**: Automatic face detection and recognition using advanced algorithms
- 📊 **Excel Integration**: Daily attendance records saved in Excel format (`Attendance_YYYY-MM-DD.xlsx`)
- 🎥 **Live Camera Feed**: Real-time face detection through webcam
- 🚫 **Duplicate Prevention**: Prevents multiple check-ins for the same person on the same day
- 📱 **User-Friendly Interface**: Clean Streamlit web interface
- ➕ **Easy Registration**: Add new faces directly through the web interface
- 📈 **Attendance Reports**: View daily and historical attendance records

---

## 🛠️ System Requirements

- Python 3.8 or higher  
- Webcam  
- Windows / Linux / MacOS  

---
```
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Installing `dlib` may require Visual Studio Build Tools on Windows. Download from [here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022).

3. **(Optional) Generate sample data**

   ```bash
   python setup_sample_data.py
   ```

---

## ▶️ Quick Start

1. **Run the application**

   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**

   * Browser opens automatically at `http://localhost:8501`
   * Or manually navigate to the URL shown in terminal

3. **Mark Attendance**

   * Click on **"Mark Attendance"** in the sidebar
   * Allow camera access
   * Face the camera → attendance will be marked automatically

---

## ➕ Adding New Faces

### Method 1: Through Web Interface

1. Go to **Register New Face** in sidebar
2. Enter the person's name
3. Capture multiple photos (recommended: 3–5 photos)
4. Click **Save Face**

### Method 2: Manual Addition

1. Create a folder with the person's name inside `known_faces/`
2. Add 3–5 clear photos of the person
3. Restart the application

---

## 🗂️ Project Structure

```
Face Reco/
├── app.py                      # Main Streamlit application
├── face_recognition_system.py  # Face recognition logic
├── attendance_manager.py       # Attendance & Excel handling
├── setup_sample_data.py        # Generate sample face images
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── known_faces/                # Registered faces
│   ├── Person1/
│   └── Person2/
└── attendance/                 # Excel attendance sheets (auto-created)
```

---

## 📊 Usage Guide

### Marking Attendance

1. Launch the app
2. Select **Mark Attendance**
3. Look at the camera → attendance is recorded automatically
4. Success message shows timestamp

### Viewing Attendance

1. Select **View Attendance**
2. Pick a date
3. View attendance records

### Attendance Records

* Daily Excel file: `Attendance_YYYY-MM-DD.xlsx`
* Columns: Name, Date, Time
* Stored in `attendance/` directory

---

## ⚠️ Troubleshooting

### Camera Issues

* Ensure webcam is connected and free
* Check browser permissions
* Refresh the page

### Face Not Recognized

* Ensure good lighting
* Face the camera directly
* Re-register if needed

### Installation Issues

* **dlib installation fails:** Install Visual Studio Build Tools
* **OpenCV issues:** Use `pip install opencv-python-headless`
* **Permission errors:** Run terminal as administrator

---

## ⚙️ Technical Details

* **Face Detection:** HOG (Histogram of Oriented Gradients)
* **Face Recognition:** 128-dimensional face encodings
* **Matching Threshold:** 0.6 (adjustable)
* **Image Format:** JPG, PNG, JPEG
* **Excel Format:** XLSX (openpyxl)

---

## 💡 Tips for Best Results

1. Ensure good lighting
2. Register 3–5 photos from different angles
3. Use clear, high-quality images
4. Look directly at the camera
5. Avoid sunglasses, masks, or obstructions

---

## 👨‍💻 Developer Info

* **Name:** Tejas Gholap
* **Role:** Data Analyst & Face Recognition Developer
* **LinkedIn:** [https://www.linkedin.com/in/tejas-gholap-bb3417300/](https://www.linkedin.com/in/tejas-gholap-bb3417300/)
* **GitHub:** [https://github.com/tejasgholap45](https://github.com/tejasgholap45)
* **Live Demo:** [https://face-recognition-attendance-project-vvdtejas-gholap.streamlit.app/](https://face-recognition-attendance-project-vvdtejas-gholap.streamlit.app/)

```

---
```
