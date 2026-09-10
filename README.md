# ImageBgRemoverAI

A local AI-powered desktop application that removes image backgrounds using `rembg`, `Pillow`, and `PySide6`.

ImageBgRemoverAI processes images directly on your computer using a locally running AI model. It does not require an external AI API or cloud service for image processing.

---

## ✨ Features

* 🖼️ Open and preview images
* 🤖 AI-powered background removal
* 💻 Local CPU-based processing
* 🔒 No external AI API required
* 🌐 Works offline after the AI model is downloaded
* 🔄 Reprocess images using different AI models
* 🧠 Multiple background-removal models
* 👀 Before-and-after image preview
* 💾 Export results as transparent PNG files
* 🧹 Clear and reset the workspace
* 🖥️ Simple desktop GUI built with PySide6

---

## 🛠️ Tech Stack

* **Python** — Core programming language
* **PySide6** — Desktop graphical user interface
* **rembg** — AI-powered background removal
* **Pillow** — Image loading and processing
* **ONNX Runtime** — Local AI model inference

---

## 📥 Download the Project

Clone the repository using Git:

```bash
git clone https://github.com/debojitdutta/ImageBgRemoverAI.git
```

Navigate to the project directory:

```bash
cd ImageBgRemoverAI
```

Alternatively, you can download the repository as a ZIP file from GitHub and extract it.

---

## 🐍 Create a Virtual Environment

It is recommended to use a Python virtual environment to keep project dependencies isolated.

Create a virtual environment:

```bash
python -m venv venv
```

### Windows PowerShell

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
venv\Scripts\activate.bat
```

If PowerShell prevents script execution, you may need to allow scripts for your current user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 📦 Install Dependencies

Install all required Python packages using:

```bash
python -m pip install -r requirements.txt
```

The main dependencies include:

* PySide6
* Pillow
* rembg[cpu]

---

## ▶️ Start the Application

From the root project directory, run:

```bash
python -m app.main
```

The ImageBgRemoverAI desktop application should now launch.

---

## 🚀 How to Use

1. Launch the application.
2. Click **Open Image**.
3. Select an image from your computer.
4. Choose an AI model if required.
5. Click **Remove Background**.
6. Wait for the AI model to process the image.
7. Preview the original and processed images.
8. If the result needs improvement, select another model and click **Reprocess**.
9. Click **Save Result** to export the image as a transparent PNG.

---

## 🧠 How It Works

ImageBgRemoverAI uses a locally running AI segmentation model to identify the foreground object and separate it from the background.

```text
Input Image
     │
     ▼
Pillow
     │
     ▼
rembg AI Model
     │
     ▼
Foreground Detection
     │
     ▼
Background Removal
     │
     ▼
Transparent PNG
```

The application uses `ONNX Runtime` to perform AI inference locally on the computer.

No image needs to be uploaded to an external AI service for processing.

---

## 🌐 Offline Usage

ImageBgRemoverAI is designed for local processing.

The first time you use a particular AI model, `rembg` may need to download the model files. Once the model is available locally, background removal can be performed without an internet connection.

```text
First Run
    │
    ├── Download AI Model
    │
    ▼
Model Stored Locally
    │
    ▼
Disconnect Internet
    │
    ▼
Process Images Locally
```

Processing speed depends on your computer's CPU, RAM, and image resolution.

---

## 📁 Project Structure

```text
ImageBgRemoverAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── remover.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔮 Future Improvements

Planned improvements may include:

* Drag-and-drop image support
* Batch background removal
* Improved image preview with zoom and pan
* Custom background colors and images
* Additional AI models
* Better result comparison
* Image editing tools
* GPU acceleration
* Standalone Windows executable
* Improved UI and application themes

---

⭐ If you find this project useful, consider giving the repository a star!
