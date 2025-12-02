# Face Recognition Attendance System

A fully functional face recognition-based attendance system built with Streamlit that automatically records daily attendance in Excel sheets.

**Live demo:** [**Try it here**](https://face-attendance-model.streamlit.app/)


## Features

- 👤 **Face Recognition**: Automatic face detection and recognition using state-of-the-art algorithms
- 📊 **Excel Integration**: Daily attendance records saved in Excel format (`Attendance_YYYY-MM-DD.xlsx`)
- 🎥 **Live Camera Feed**: Real-time face detection through webcam
- 🚫 **Duplicate Prevention**: Prevents multiple check-ins for the same person on the same day
- 📱 **User-Friendly Interface**: Clean Streamlit web interface
- ➕ **Easy Registration**: Add new faces directly through the web interface
- 📈 **Attendance Reports**: View daily and historical attendance records

## System Requirements

- Python 3.8 or higher
- Webcam
- Windows/Linux/MacOS

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "e:\chat application\Face Reco"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note**: Installing `dlib` might require Visual Studio Build Tools on Windows. If you encounter issues, install it from [here](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022).

3. **Generate sample data (optional)**
   ```bash
   python setup_sample_data.py
   ```

## Quick Start

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - The browser will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal

3. **Mark Attendance**
   - Click on "Mark Attendance" in the sidebar
   - Allow camera access when prompted
   - Face the camera - your attendance will be marked automatically when recognized

## Adding New Faces

### Method 1: Through Web Interface
1. Go to "Register New Face" in the sidebar
2. Enter the person's name
3. Capture multiple photos (recommended: 3-5 photos from different angles)
4. Click "Save Face"

### Method 2: Manual Addition
1. Create a folder with the person's name in the `known_faces` directory
2. Add 3-5 clear photos of the person's face in that folder
3. Restart the application

## Project Structure

```
Face Reco/
├── app.py                      # Main Streamlit application
├── face_recognition_system.py  # Face recognition logic
├── attendance_manager.py       # Attendance tracking and Excel handling
├── setup_sample_data.py        # Generate sample face images
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── known_faces/               # Directory for registered faces
│   ├── Person1/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── Person2/
│       ├── image1.jpg
│       └── image2.jpg
└── attendance/                # Excel attendance sheets (auto-created)
    ├── Attendance_2025-11-30.xlsx
    └── Attendance_2025-12-01.xlsx
```

## Usage Guide

### Marking Attendance
1. Launch the app
2. Select "Mark Attendance" from the sidebar
3. Look at the camera
4. Once recognized, your attendance is automatically recorded
5. You'll see a success message with the timestamp

### Viewing Attendance
1. Select "View Attendance" from the sidebar
2. Choose a date from the date picker
3. View all attendance records for that day

### Attendance Records
- Each day creates a new Excel file: `Attendance_YYYY-MM-DD.xlsx`
- Records include: Name, Date, Time
- Files are stored in the `attendance` directory

## Troubleshooting

### Camera Not Working
- Ensure your webcam is connected and not being used by another application
- Check browser permissions for camera access
- Try refreshing the page

### Face Not Recognized
- Ensure good lighting conditions
- Face the camera directly
- Make sure you're registered in the system
- Try re-registering with more photos from different angles

### Installation Issues
- **dlib installation fails**: Install Visual Studio Build Tools
- **OpenCV issues**: Try `pip install opencv-python-headless`
- **Permission errors**: Run terminal as administrator

## Technical Details

- **Face Detection**: Uses HOG (Histogram of Oriented Gradients) algorithm
- **Face Recognition**: 128-dimensional face encoding comparison
- **Matching Threshold**: 0.6 (adjustable in code)
- **Image Format**: Supports JPG, PNG, JPEG
- **Excel Format**: XLSX with openpyxl

## Tips for Best Results

1. **Good Lighting**: Ensure your face is well-lit
2. **Multiple Angles**: Register with 3-5 photos from different angles
3. **Clear Images**: Use high-quality, clear face photos
4. **Direct Gaze**: Look directly at the camera
5. **No Obstructions**: Avoid sunglasses, masks, or other face coverings


## ⭐ Features

* Real-time face detection & recognition
* Daily Excel attendance sheets
* Prevents duplicate attendance
* Add new faces easily
* View attendance history

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## ▶️ Run the App

```bash
streamlit run app.py
```

## 📝 How It Works

1. Open the app
2. Go to **Mark Attendance**
3. Show your face to the camera
4. Attendance is saved automatically in `attendance/`

## ➕ Add New Faces

* Use the **Register New Face** option
* Or add images manually to `known_faces/PersonName/`

## 📂 Attendance Files

Generated daily as:

```
Attendance_YYYY-MM-DD.xlsx
```

## 💡 Tips

* Use clear, well-lit face photos
* Register 3–5 images for best accuracy

