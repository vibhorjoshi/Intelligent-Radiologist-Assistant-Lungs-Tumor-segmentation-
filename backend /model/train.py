import torch
import torch.nn as nn
import torch.optim as optim
from model import ResNet15  # Import model architecture
from preprocess import load_data  # Data loading and preprocessing

# Load data
train_loader, val_loader = load_data()

# Define model, loss function, and optimizer
model = ResNet15()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):  # Change based on performance
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            val_loss += criterion(outputs, labels).item()
    print(f'Epoch {epoch+1}, Validation Loss: {val_loss}')
