# 🐔 Chicken Disease Classifier

Welcome to the **Chicken Disease Classifier**! This application serves as a "virtual veterinarian" for poultry farmers and enthusiasts. By simply uploading a photo of a chicken, the app uses Artificial Intelligence to instantly predict whether the bird is **Healthy** or showing signs of a common disease like **Coccidiosis**.

Whether you are a farmer looking for quick diagnostics, or an AI developer exploring modern machine learning architectures, this project is built to be accessible, fast, and easy to use.

---

## 🌟 What Does It Do? (For Everyone)

This application provides a simple web dashboard that you can open in your browser. It has two main features:

1. **Disease Prediction (Diagnosis)**
   * **Drag & Drop:** Simply drag a picture of a chicken onto the webpage, or click to browse files on your computer.
   * **Instant Results:** The AI looks at the photo and gives you a verdict (e.g., "Healthy") along with a confidence score (e.g., "95.4% sure").
   
2. **One-Click AI Training**
   * **Self-Improving:** If you have new data, you don't need to be a programmer to teach the AI. Just click the **Start Training Run** button.
   * **Live Updates:** The dashboard will show you what the AI is doing, how much it is learning (accuracy), and notify you when the new, smarter 'brain' is ready to use.

---

## 🛠️ Technical Details & Architecture (For Developers)

Under the hood, this project is a modern, lightweight, and robust Deep Learning web application. It transitions away from older stacks (like Flask + TensorFlow) to a fast and modern stack.

**Core Tech Stack:**
* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) – Lightning-fast asynchronous Python web framework.
* **Machine Learning:** [PyTorch](https://pytorch.org/) & `torchvision` – Used for defining the CNN architecture and training loops.
* **Computer Vision Model:** **ResNet18** (Transfer Learning). The pre-trained backbone is used with a custom diagnostic head specifically tuned for 2 classes (Healthy vs. Coccidiosis).
* **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/) – Ensures that configurations and expected data types are strictly validated.
* **Frontend:** Vanilla HTML/JS with [Bootstrap 5](https://getbootstrap.com/), served directly by FastAPI. Zero build-step or bundler required.

**Key Architecture Highlights:**
* **Non-Blocking Training:** The training pipeline runs on a separate background thread. The FastAPI server remains responsive while the heavy lifting happens, allowing the frontend to poll for live training metrics via a `/api/status` endpoint.
* **Stateful Fallback Engine:** To ensure the app never crashes on a fresh install, if a trained `.pt` model is missing from the localized artifacts folder, the server dynamically provisions a lightweight initialized model in-memory.
* **Modular Configuration:** All AI hyperparameters (epochs, learning rate, batch size, augmentations, image dimensions) live cleanly outside the codebase in a pure `params.yaml` file. File paths and integrations live in `config/config.yaml`.

---

## 🚀 How to Run the App on Your Computer

If you want to run this application on your own machine, follow these steps:

### 1. Prerequisites
Make sure you have [Python 3.10+](https://www.python.org/downloads/) installed.

### 2. Setup the Environment
Open your terminal (Command Prompt, PowerShell, or bash) and clone/navigate to this project directory:

```bash
# 1. Create a virtual environment to isolate the project
python -m venv venv

# 2. Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install the required libraries
pip install -r requirements.txt
```

### 3. Start the Server
Run the web application using the Uvicorn ASGI server:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Open the App!
Open your favorite web browser (Chrome, Edge, Firefox, etc.) and go to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## ⚙️ Configuration & Tweaking

Want to change how the AI learns? You don't have to touch a single line of Python code!

* **`params.yaml`**: Edit this file to change machine learning hyperparameters like the number of training `epochs`, `learning_rate`, `batch_size`, or switch the `backbone` architecture.
* **`config/config.yaml`**: Edit this file to change where the app saves models, reads data, or logs metrics.
* **`.env`**: Store sensitive credentials here, like S3 buckets or AWS Keys for pulling large cloud datasets.

---
*Built with ❤️ to keep our feathered friends healthy.*