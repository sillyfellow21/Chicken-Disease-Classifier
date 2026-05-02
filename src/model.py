import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

def get_model(num_classes: int = 2) -> nn.Module:
    # Use standard modern non-vgg backbone
    weights = ResNet18_Weights.DEFAULT
    model = resnet18(weights=weights)
    
    # Freeze layers if needed (we'll leave them trainable for fine-tuning)
    # for param in model.parameters():
    #     param.requires_grad = False
        
    num_ftrs = model.fc.in_features
    # Replace classification head
    model.fc = nn.Linear(num_ftrs, num_classes)
    return model
