import json
import logging
import os
import zipfile
import urllib.request
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, datasets
from pathlib import Path

from src.config import get_settings, load_config, load_params
from src.model import get_model

logger = logging.getLogger(__name__)

def dummy_dataset_creation(data_dir: Path, image_size: tuple):
    pass

def run_training_pipeline():
    config = load_config()
    params = load_params()
    settings = get_settings()

    config.artifacts_root.mkdir(parents=True, exist_ok=True)
    config.data_ingestion.root_dir.mkdir(parents=True, exist_ok=True)
    config.prepare_model.root_dir.mkdir(parents=True, exist_ok=True)
    config.training.root_dir.mkdir(parents=True, exist_ok=True)

    # 1. Data Ingestion
    logger.info("Starting data ingestion")
    data_dir = config.data_ingestion.unzip_dir
    # In a real scenario we'd download from S3 here
    # Mocking data if not exists
    dummy_dataset_creation(data_dir, params.image_size)

    # 2. Prepare Data Loaders
    logger.info("Preparing data loaders")
    # Data augmentation for training
    train_transforms = transforms.Compose([
        transforms.Resize(params.image_size),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    dataset = datasets.ImageFolder(data_dir, transform=train_transforms)
    dataloader = DataLoader(dataset, batch_size=params.batch_size, shuffle=True)

    # 3. Model Preparation
    logger.info("Initializing model")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model(num_classes=params.classes).to(device)

    # 4. Training
    logger.info("Starting training loop")
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=params.learning_rate, momentum=0.9)

    model.train()
    for epoch in range(params.epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(dataset)
        epoch_acc = correct / total
        logger.info(f"Epoch {epoch+1}/{params.epochs} - Loss: {epoch_loss:.4f}, Accuracy: {epoch_acc:.4f}")

    # 5. Evaluation / Metrics Saving
    metrics = {
        "loss": epoch_loss,
        "accuracy": epoch_acc
    }
    with open(config.training.metrics_path, "w") as f:
        json.dump(metrics, f)

    # 6. Save Model
    torch.save(model.state_dict(), config.training.trained_model_path)
    logger.info(f"Model saved to {config.training.trained_model_path}")
    
    return metrics
