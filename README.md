# FaceDetection

A comprehensive Python-based face detection and recognition system with a PyQt5 GUI for access control and user management.

## 📋 Overview

FaceDetection is a complete face recognition system designed for access control applications. It combines face detection, face recognition, and user database management with an intuitive desktop interface. The system uses OpenCV and machine learning algorithms to detect and recognize faces in images and video streams.

## ✨ Features

- **Face Detection**: Real-time face detection using Haar Cascade classifiers
- **Face Recognition**: LBPH (Local Binary Patterns Histograms) face recognizer with trained models
- **Access Control**: User authentication and access management system
- **Image Management**: Upload, process, and manage user face image databases
- **GUI Application**: User-friendly PyQt5 interface for all operations
- **Image Preprocessing**: Advanced image normalization and enhancement
- **Database Management**: Store and manage user profiles with associated face data

## 🛠️ Technology Stack

- **Python 3**: Core programming language
- **OpenCV**: Computer vision library for face detection and recognition
- **PyQt5**: Desktop GUI framework
- **NumPy**: Numerical computing
- **PIL (Pillow)**: Image processing
- **imutils**: Image utilities for processing
- **Arduino Support**: Optional hardware integration for access control

## 📁 Project Structure

```
FaceDetection/
├── src/
│   ├── UI/                      # GUI components and user interface
│   │   ├── main.py              # Main application window
│   │   ├── controle.py          # Control access interface
│   │   ├── controle_acces.py    # Access control logic
│   │   └── *.ui                 # PyQt5 UI forms
│   ├── RetinaFace/              # RetinaFace detection model
│   │   └── dataBaseManager.py   # Database management
│   ├── data_prep.py             # Data preparation and preprocessing
│   ├── addFolder.py             # Add user folders and training data
│   ├── recongnizer.py           # Face recognition engine
│   └── recongnizer_.py          # Alternative recognizer implementation
├── classifiers/                 # Pre-trained Haar Cascade classifiers
│   ├── haarcascade_frontalface_alt.xml
│   └── haarcascade_frontalface_default.xml
├── splash/                      # Splash screen and branding
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Chamssidine/FaceDetection.git
   cd FaceDetection
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Required packages** (if requirements.txt is incomplete):
   ```bash
   pip install opencv-python opencv-contrib-python PyQt5 numpy pillow imutils
   ```

### Usage

#### Running the GUI Application

```bash
cd src
python -m UI.main
```

#### Face Detection on Images

```python
import cv2
from src.data_prep import detect_face, normalizer, rescale

# Load image
image = cv2.imread('path/to/image.jpg')

# Detect faces
face_roi = detect_face(image)

# Normalize for recognition
normalized_face = normalizer(face_roi)
```

#### Adding New Users

1. Launch the GUI application
2. Click "Ouvrir Dossier" (Open Folder) to select a folder with user images
3. Click "Ajouter Dossier" (Add Folder) to register the new user
4. Provide the user's name when prompted
5. The system will extract faces from the images and create a user profile

#### Face Recognition

1. Load a model from the database
2. Click "Démarrer" (Start) to begin recognition
3. The system will identify faces and display results with confidence scores

## 🔧 Core Components

### Face Detection (`data_prep.py`)
- Uses Haar Cascade classifiers for face detection
- Detects faces in images with configurable parameters
- Extracts face regions of interest (ROI)

### Face Recognizer (`recongnizer.py`)
- LBPH-based face recognition
- Supports real-time video recognition
- Returns recognized user ID, name, and confidence score
- Advanced image normalization with gamma correction and Difference of Gaussians (DOG)

### Database Manager (`RetinaFace/dataBaseManager.py`)
- Manages user profiles and face data storage
- Stores trained models (.yml files) for each user
- Organizes user data hierarchically

### GUI (`src/UI/`)
- Main interface with PyQt5
- File dialogs for image/folder selection
- Real-time video capture and display
- User authentication and access control

## 📊 How It Works

### Workflow

1. **User Registration**:
   - User uploads a folder with their face images
   - System detects faces in each image
   - Extracted faces are normalized and stored

2. **Model Training**:
   - LBPH recognizer trains on stored face data
   - Trained model saved as `.yml` file in user directory

3. **Recognition**:
   - Input image/video is converted to grayscale
   - Faces detected using Haar Cascade
   - Each face is normalized and passed to recognizer
   - System returns closest match (user ID, name, confidence)

### Image Processing Pipeline

```
Input Image → Grayscale Conversion → Face Detection (Haar Cascade)
    → Face Extraction (ROI) → Normalization (Gamma + DOG) 
    → LBPH Recognition → Results (ID, Name, Confidence)
```

## 🎯 Features in Detail

### Image Normalization
- Gamma correction for brightness adjustment
- Difference of Gaussians (DOG) for edge enhancement
- Contrast normalization for improved recognition accuracy

### Real-time Recognition
- Live video capture from webcam
- Frame-by-frame face detection and recognition
- Configurable confidence thresholds

### Access Control
- User authentication via face recognition
- Admin password protection for sensitive operations
- Optional Arduino integration for door locks/LED indicators

## 📝 Configuration

Key parameters can be adjusted in the code:

- **Face Detection Confidence**: `detectMultiScale` parameters (scaleFactor, minNeighbors)
- **Minimum Face Size**: `minSize=(30,30)` in detection
- **Image Resize Scale**: Default `scale=0.4`
- **Gamma Correction**: `gamma = 0.2` in normalization

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the project.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Chamssidine Abdallah Ambinintsoa**
- Email: chamssidinezx347@gmail.com
- GitHub: [@Chamssidine](https://github.com/Chamssidine)

## 🙏 Acknowledgments

- OpenCV community for face detection algorithms
- PyQt5 framework for the GUI
- Haar Cascade classifiers for robust face detection

## 📞 Support

For questions or issues, please open a GitHub issue in this repository.

---

**Last Updated**: June 2025
