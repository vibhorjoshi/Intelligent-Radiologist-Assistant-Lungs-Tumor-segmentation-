import torch
import torch.nn as nn
import torchvision.models as models

# Custom ResNet-15 model with both segmentation and classification heads
class ResNet15(nn.Module):
    def __init__(self, num_classes=2):  # Binary classification for tumor
        super(ResNet15, self).__init__()
        
        # Load pretrained ResNet18 model
        self.resnet = models.resnet18(pretrained=True)

        # Classification head (replacing the fully connected layer)
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)

        # Segmentation head (fully convolutional layers)
        self.segmentation_head = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 1, kernel_size=1),  # Output a single channel for the mask
            nn.Sigmoid()  # Sigmoid for binary mask output
        )
        
        # Modify layers to extract features for segmentation
        # Remove the original ResNet fully connected layer
        self.resnet = nn.Sequential(*list(self.resnet.children())[:-2])

    def forward(self, x):
        # Forward pass through the ResNet backbone to extract features
        features = self.resnet(x)

        # Segmentation output (binary mask)
        segmentation_output = self.segmentation_head(features)

        # Flatten and average pooling to feed into classification head
        pooled_features = nn.AdaptiveAvgPool2d((1, 1))(features)
        pooled_features = pooled_features.view(pooled_features.size(0), -1)

        # Classification output
        classification_output = self.resnet.fc(pooled_features)

        return classification_output, segmentation_output  # Return both outputs

def load_model(model_path='model.pth'):
    """
    Load the trained model with both classification and segmentation tasks.
    
    Args:
        model_path (str): Path to the saved model file (e.g., 'model.pth')
    
    Returns:
        ResNet15: Loaded ResNet15 model.
    """
    model = ResNet15()
    model.load_state_dict(torch.load(model_path))  # Load trained model weights
    return model
