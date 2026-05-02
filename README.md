# 🐔 Chicken Disease Classifier

🌍 **Live Demo:** 👉 **[https://chicken-disease-classifier-1q0r.onrender.com](https://chicken-disease-classifier-1q0r.onrender.com)** 👈

Welcome to the **Chicken Disease Classifier**! This application serves as a "virtual veterinarian" for poultry farmers and enthusiasts. By simply uploading a photo of chicken feces, the app uses Artificial Intelligence to instantly predict whether the bird is **Healthy** or showing signs of 3 common diseases: **Coccidiosis**, **Newcastle Disease**, or **Salmonella**.

Whether you are a farmer looking for quick diagnostics, or an AI developer exploring modern machine learning architectures, this project is built to be accessible, fast, and easy to use with automated free deployments.

---

## 🌟 What Does It Do?

This application provides a simple web dashboard that you can open in your browser. It has two main features:

1. **Disease Prediction (Diagnosis)**
   * **Drag & Drop:** Simply drag a picture onto the webpage, or click to browse files on your computer.
   * **Instant Results:** The AI evaluates the photo and gives you a classification across 4 states, alongside a confidence score (e.g., "95.4% sure it's Salmonella").
   
2. **One-Click AI Training**
   * **Self-Improving:** If you have new data in your `artifacts/data_ingestion/` folders, just click the **Start Training Run** button on the UI.
   * **Live Updates:** The dashboard will show you what the AI is doing, how much it is learning, and notify you when the new, smarter 'brain' is ready to use.

---

## � Dataset

The model is trained on the publicly available **Chicken Disease** dataset. You can view, explore, and download the original dataset on Kaggle:
👉 **[Chicken Disease Dataset on Kaggle](https://www.kaggle.com/datasets/allandclive/chicken-disease-1)**

---

## �🛠️ Technical Details & DevOps Architecture

Under the hood, this project is a modern, robust Deep Learning web application utilizing an entirely free hosting and CI/CD workflow.

**Core Tech Stack:**
* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) – Lightning-fast asynchronous Python web framework instead of Flask.
* **Machine Learning:** [PyTorch](https://pytorch.org/) & `torchvision` – Used for defining the CNN architecture and training loops.
* **Computer Vision Model:** **ResNet18** (Transfer Learning) with an overridden classification head tuned for 4 classes.
* **Frontend:** Vanilla HTML/JS with [Bootstrap 5](https://getbootstrap.com/), served dynamically via Starlette `TemplateResponse`.
* **Containerization:** **Docker** for standardized multi-OS runtime stability.
* **CI/CD pipeline:** **GitHub Actions** building and deploying containers automatically to the **GitHub Container Registry (GHCR)**.
* **Infrastructure as Code:** **Render** ready configuration via `render.yaml`.

---

## 🚀 How to Run locally

If you want to run this application on your own machine without Docker, follow these steps:

### 1. Prerequisites
Make sure you have [Python 3.11+](https://www.python.org/downloads/) installed.

### 2. Setup the Environment
```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment (Windows)
.\venv\Scripts\activate

# 3. Install the required libraries
pip install -r requirements.txt
```

### 3. Start the Server
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Open your web browser and go to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🐳 Docker Deployment & Free Cloud Hosting

This project is entirely Dockerized and optimized (using CPU-only PyTorch) to run efficiently on free cloud tiers. You can run it locally or deploy it alive online to show the world!

### Option A: Free Online Deployment (Render.com)
Because this repository contains a `render.yaml` Infrastructure-as-Code file, deploying it for free is a 2-minute process:
1. Create a free account at **[Render.com](https://render.com/)** and sign in with GitHub.
2. Click **New** -> **Blueprint**.
3. Select this GitHub repository (`Chicken-Disease-Classifier`).
4. Keep the Blueprint Path as `render.yaml` and click **Apply**.

Render will automatically provision a free server, install the optimized CPU PyTorch build to avoid Out-Of-Memory crashes, and host your application securely with an `https://` URL!

### Option B: Local Docker Build
If you want to run the isolated container on your own machine:
```bash
docker build -t chicken-classifier .
docker run -p 8000:8000 chicken-classifier
```
The app will be active at `http://localhost:8000`.

### CI/CD Pipeline (GitHub Actions)
Every time you push to the `main` branch, a GitHub Action automatically triggers to:
1. Check out the latest code.
2. Build the Docker container.
3. Push the validated image to the **GitHub Container Registry (GHCR)** completely for free.

---

## ⚙️ Configuration
* **`params.yaml`**: Edit this file to change hyperparameters (epochs, learning_rate, batch_size, classes: 4).
* **`config/config.yaml`**: Edit this file to change where the app saves models and reads data.

*Built with ❤️ to keep our feathered friends healthy.*