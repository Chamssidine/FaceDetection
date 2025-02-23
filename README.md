# FaceRec

FaceDetection is a software developed for face recognition and visage detection. It leverages machine learning techniques, specifically **Haar Cascade** for face detection and **LBPH (Local Binary Patterns Histogram)** for face recognition.

## Features
- Real-time face detection using OpenCV
- Face recognition with LBPH algorithm
- GUI built with PyQt5
- Integration with Arduino via easyarduino

## Installation
### Prerequisites
Ensure you have Python installed (preferably Python 3.x). You can download it from [python.org](https://www.python.org/).

### Required Libraries
Install all dependencies using the following command:
```sh
pip freeze | findstr /R "imutils opencv pyqt5 easyarduino pil-utils" > requirements.txt
pip install -r requirements.txt
```

Alternatively, you can install each library manually:
```sh
pip install imutils opencv-python pyqt5 easyarduino pillow
```

**Note:** CMake is required for OpenCV and dlib. Download it from [CMake Official Website](https://cmake.org/download/).

## How to Run
To launch the program, use the following command:
```sh
python .\controle.py
```

## Contributing
Feel free to submit issues or pull requests if you have any improvements!

## License
This project is licensed under the MIT License.

