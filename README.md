# Project SetuP

## Prerequiseets
Ensure you have the following installed before proceeding:
- [FFmpeg](https://ffmpeg.org/download.html)
- Python (latest stable version recommended)
- Pip (Python package manager)
- Pipenv (Python environment manager)

## Installation Steps

### Step 1: Install FFmpeg
Download and install FFmpeg from the official website:
[FFmpeg Downloads](https://ffmpeg.org/download.html)

### Step 2: Install Pipenv
```sh
pip install pipenv
```

### Step 3: Set Up the Virtual Environment
```sh
pipenv install
pipenv shell
```

### Step 4: Create a Virtual Environment (if needed)
```sh
python -m venv venv
venv\Scripts\activate  # Activate the virtual environment (Windows)
```

### Step 5: Install Required Dependencies
```sh
pip install -r requirements.txt
```

## Running the Project

### Run Main Scripts
```sh
python brain_of_the_doctor.py
```
```sh
python voice_of_the_patient.py
```
```sh
python voice_of_the_doctor.py
```
```sh
python gradio_app.py
```

This setup ensures that all dependencies are correctly installed and the project runs smoothly.

