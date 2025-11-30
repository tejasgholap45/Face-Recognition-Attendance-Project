"""
Setup Sample Data
Generates sample face images for testing the attendance system
"""

import os
from pathlib import Path
import requests
from PIL import Image
import io


def create_sample_faces():
    """Create sample face images for testing"""
    
    # Create known_faces directory
    known_faces_dir = Path("known_faces")
    known_faces_dir.mkdir(exist_ok=True)
    
    # Sample person names
    sample_people = [
        "John_Smith",
        "Sarah_Johnson",
        "Michael_Brown",
        "Emily_Davis",
        "David_Wilson"
    ]
    
    print("Generating sample face images...")
    print("Note: This will use placeholder images from an online service.")
    print("For production use, replace with actual photos of people.\n")
    
    for person_name in sample_people:
        # Create person directory
        person_dir = known_faces_dir / person_name
        person_dir.mkdir(exist_ok=True)
        
        print(f"Creating images for {person_name}...")
        
        # Generate 3 sample images per person
        for i in range(1, 4):
            try:
                # Use a placeholder face image service
                # This generates random faces for testing
                # Note: In production, use real photos
                
                # Using a simple placeholder service
                # Each person gets a unique seed for consistent faces
                seed = hash(person_name) % 1000
                url = f"https://i.pravatar.cc/300?img={seed + i}"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    # Save image
                    image_path = person_dir / f"{i}.jpg"
                    
                    # Open and save the image
                    img = Image.open(io.BytesIO(response.content))
                    img.save(image_path)
                    
                    print(f"  ✓ Created {image_path.name}")
                else:
                    print(f"  ✗ Failed to download image {i} for {person_name}")
                    
            except Exception as e:
                print(f"  ✗ Error creating image {i} for {person_name}: {e}")
        
        print()
    
    print("Sample data generation complete!")
    print(f"\nCreated {len(sample_people)} sample people in the 'known_faces' directory.")
    print("You can now run the application with: streamlit run app.py")


if __name__ == "__main__":
    create_sample_faces()
