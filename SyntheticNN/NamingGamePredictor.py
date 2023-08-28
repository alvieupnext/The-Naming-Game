import torch
import torch.nn.functional as F  # Parameterless functions, like (some) activation functions
from torch import optim  # For optimizers like SGD, Adam, etc.
from torch import nn  # All neural network modules
from patients.patientData import *
import pandas as pd
from torch.utils.data import DataLoader, Dataset  # Gives easier dataset managment by creating mini batches etc.
from torch.utils.data.sampler import SubsetRandomSampler


#Create Network
class NN(nn.Module):
  def __init__(self, input_size, num_classes):
    super(NN, self).__init__()
    self.fc1 = nn.Linear(input_size, 50)
    self.fc2 = nn.Linear(50, num_classes)

  def forward(self, x):
    x = F.relu(self.fc1(x))
    x = self.fc2(x)
    return x

#Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Hyperparameters

noOfAgents = 40
input_size = ((noOfAgents - 1) * noOfAgents) // 2
#predicts 4 convergences
num_classes = 1
learning_rate = 0.01
batch_size = 95
num_epochs = 500

#load Data

class ConvergenceDataset(Dataset):

  def __init__(self):
    patientInfo = networkInfo
    # remove all zero columns (add no meaningful information)
    patientInfo = patientInfo.loc[(patientInfo.sum(axis=1) != 0), (patientInfo.sum(axis=0) != 0)]
    # turn MS data into int
    patientInfo["MS"] = patientInfo["MS"].astype(int)
    #only get the last column from convergenceInfo
    convergence = convergenceInfo
    #get last column
    convergence = convergence.iloc[:, [1, -1]]
    #merge datasets
    xy = pd.merge(patientInfo, convergence, on="subject")
    #get the x data
    x = xy.iloc[:, 1:-1]
    print(x.columns)
    #get the y data
    y = xy.iloc[:, [-1]]
    self.xcolumns = x.shape[1]
    print(self.xcolumns)
    #turn pandas dataframe to tensor
    self.x = torch.tensor(x.values, dtype=torch.float32)
    self.y = torch.tensor(y.values, dtype=torch.float32)
    self.n_samples = len(xy.index)

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.n_samples

dataset = ConvergenceDataset()
validation_split = .2
shuffle_dataset = True
random_seed = 42

#merged
# xy = pd.merge(networkInfo, convergenceInfo)
# xy = xy.loc[(xy.sum(axis=1) != 0), (xy.sum(axis=0) != 0)]
# print(xy.shape)

# C_mat = xy.corr()
# print(xy["C9-4"].sum())
# # print(C_mat)
# fig = plt.figure(figsize = (15,15))
# sb.heatmap(C_mat, vmax = 1, square = True)
# plt.show()

# Creating data indices for training and validation splits:
dataset_size = len(dataset)
indices = list(range(dataset_size))
split = int(np.floor(validation_split * dataset_size))
if shuffle_dataset :
  np.random.seed(random_seed)
  np.random.shuffle(indices)
train_indices, val_indices = indices[split:], indices[:split]

# Creating PT data samplers and loaders:
train_sampler = SubsetRandomSampler(train_indices)
valid_sampler = SubsetRandomSampler(val_indices)

train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                           sampler=train_sampler)
validation_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                                sampler=valid_sampler)

dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                                shuffle=True)

#Initialize Network
model = NN(input_size=dataset.xcolumns, num_classes=num_classes).to(device)

#criterion and optimizer
criterion = nn.HuberLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

#Train Network

for epoch in range(num_epochs):
  print(f"On training epoch {epoch}")
  running_loss = 0
  for batch_idx, (data, targets) in enumerate(dataloader):
    data = data.to(device=device)
    targets = targets.to(device=device)

    # backward
    optimizer.zero_grad()

    #forward
    scores = model(data)
    loss = criterion(scores, targets)
    loss.backward()

    #optimizer step
    optimizer.step()
    running_loss += loss.item()
  print(f"Training loss: {running_loss / len(train_loader)}")


