"""
Face Recognition System Module (OpenCV-based)
Handles face detection, encoding, and recognition using only OpenCV
No dlib or MediaPipe required - works on all platforms
"""

import cv2
import numpy as np
import os
from pathlib import Path
from typing import List, Tuple, Dict
import pickle


class FaceRecognitionSystem:
    def __init__(self, known_faces_dir: str = "known_faces"):
        """
        Initialize the face recognition system using OpenCV
        
        Args:
            known_faces_dir: Directory containing subdirectories of known faces
        """
        self.known_faces_dir = Path(known_faces_dir)
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Initialize OpenCV face detector and recognizer
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Use LBPH Face Recognizer (Local Binary Patterns Histograms)
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.is_trained = False
        
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known faces from the known_faces directory"""
        self.known_face_encodings = []
        self.known_face_names = []
        faces = []
        labels = []
        label_map = {}
        current_label = 0
        
        if not self.known_faces_dir.exists():
            self.known_faces_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {self.known_faces_dir}")
            return
        
        # Iterate through each person's directory
        for person_dir in self.known_faces_dir.iterdir():
            if person_dir.is_dir():
                person_name = person_dir.name
                label_map[current_label] = person_name
                
                # Load all images for this person
                for image_path in person_dir.glob("*"):
                    if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        try:
                            # Load image
                            image = cv2.imread(str(image_path))
                            if image is None:
                                print(f"Could not load {image_path}")
                                continue
                            
                            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            
                            # Detect face
                            face_rects = self.face_cascade.detectMultiScale(
                                gray, 
                                scaleFactor=1.1, 
                                minNeighbors=5, 
                                minSize=(30, 30)
                            )
                            
                            if len(face_rects) > 0:
                                # Use the first detected face
                                (x, y, w, h) = face_rects[0]
                                face_roi = gray[y:y+h, x:x+w]
                                
                                # Resize to standard size
                                face_roi = cv2.resize(face_roi, (200, 200))
                                
                                faces.append(face_roi)
                                labels.append(current_label)
                                self.known_face_names.append(person_name)
                                
                                print(f"Loaded face: {person_name} from {image_path.name}")
                            else:
                                print(f"No face found in {image_path}")
                        except Exception as e:
                            print(f"Error loading {image_path}: {e}")
                
                current_label += 1
        
        # Train the recognizer if we have faces
        if len(faces) > 0:
            self.face_recognizer.train(faces, np.array(labels))
            self.is_trained = True
            self.label_map = label_map
            print(f"Total faces loaded: {len(faces)}")
            print(f"Trained recognizer with {len(label_map)} people")
        else:
            print("No faces loaded for training")
            self.is_trained = False
    
    def recognize_faces(self, frame: np.ndarray, confidence_threshold: int = 100) -> List[Dict]:
        """
        Recognize faces in a frame
        
        Args:
            frame: Image frame (BGR format from OpenCV)
            confidence_threshold: Maximum distance for recognition (lower is more strict, typical: 50-100)
        
        Returns:
            List of dictionaries containing face information:
            - name: Person's name or "Unknown"
            - location: Tuple of (top, right, bottom, left)
            - confidence: Match confidence (lower is better for LBPH)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        face_rects = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        results = []
        
        for (x, y, w, h) in face_rects:
            # Extract face region
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))
            
            name = "Unknown"
            confidence = 0.0
            
            # Recognize face if trained
            if self.is_trained:
                label, distance = self.face_recognizer.predict(face_roi)
                
                # Lower distance means better match
                if distance < confidence_threshold:
                    name = self.label_map.get(label, "Unknown")
                    # Convert distance to confidence (0-1 scale, inverted)
                    confidence = max(0, 1 - (distance / confidence_threshold))
                else:
                    confidence = 0.0
            
            # Convert to (top, right, bottom, left) format
            results.append({
                'name': name,
                'location': (y, x + w, y + h, x),
                'confidence': confidence,
                'distance': distance if self.is_trained else 999
            })
        
        return results
    
    def draw_faces(self, frame: np.ndarray, face_results: List[Dict]) -> np.ndarray:
        """
        Draw bounding boxes and labels on detected faces
        
        Args:
            frame: Image frame
            face_results: List of face recognition results
        
        Returns:
            Frame with drawn annotations
        """
        for result in face_results:
            top, right, bottom, left = result['location']
            name = result['name']
            confidence = result['confidence']
            
            # Choose color based on recognition
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            
            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw label text
            label = f"{name}"
            if name != "Unknown":
                label += f" ({confidence:.2f})"
            
            cv2.putText(
                frame, 
                label, 
                (left + 6, bottom - 6), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.6, 
                (255, 255, 255), 
                1
            )
        
        return frame
    
    def add_new_face(self, name: str, image_path: str) -> bool:
        """
        Add a new face to the known faces database
        
        Args:
            name: Person's name
            image_path: Path to the image file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create person directory if it doesn't exist
            person_dir = self.known_faces_dir / name
            person_dir.mkdir(parents=True, exist_ok=True)
            
            # Load and verify the image contains a face
            image = cv2.imread(image_path)
            if image is None:
                print(f"Could not load image from {image_path}")
                return False
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_rects = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            if len(face_rects) == 0:
                print(f"No face found in the image")
                return False
            
            # Copy image to person's directory
            import shutil
            dest_path = person_dir / f"{len(list(person_dir.glob('*'))) + 1}.jpg"
            shutil.copy(image_path, dest_path)
            
            # Reload all known faces
            self.load_known_faces()
            
            print(f"Successfully added face for {name}")
            return True
            
        except Exception as e:
            print(f"Error adding face: {e}")
            return False
    
    def save_face_from_frame(self, name: str, frame: np.ndarray) -> bool:
        """
        Save a face from a camera frame
        
        Args:
            name: Person's name
            frame: Image frame containing the face
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create person directory if it doesn't exist
            person_dir = self.known_faces_dir / name
            person_dir.mkdir(parents=True, exist_ok=True)
            
            # Verify the frame contains a face
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_rects = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
            
            if len(face_rects) == 0:
                print(f"No face found in the frame")
                return False
            
            # Save the frame
            image_count = len(list(person_dir.glob('*.jpg'))) + 1
            image_path = person_dir / f"{image_count}.jpg"
            cv2.imwrite(str(image_path), frame)
            
            # Reload all known faces
            self.load_known_faces()
            
            print(f"Successfully saved face for {name}")
            return True
            
        except Exception as e:
            print(f"Error saving face: {e}")
            return False
    
    def get_known_names(self) -> List[str]:
        """Get list of all known person names"""
        return list(set(self.known_face_names))
