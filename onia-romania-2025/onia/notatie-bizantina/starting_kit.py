# Solution scaffolding for 'Notatia bizantina'
# Feel free to use anything from this 

import math
import pandas as pd
import cv2
import csv 
import joblib
import torch.nn as nn
import torch
import numpy as np

from typing import Any, Tuple


def preprocess_image(imgdata):
    
    # ...

    return imgdata

def load_data(dataset_path: str, data_root_dir='.') -> Tuple[Any, Any, Any]:
    unique_labels = set() 

    # Load dataset from CSV file
    dataset = []
    with open(dataset_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            #row["Path"], row["Effect"] ...
    
    X = []
    labels = []
    
    for row in dataset:
        imgdata = preprocess_image(cv2.imread(data_root_dir + "/" + row["Path"]))
       
        # other processing
        # build X and labels

    # Return the output tuple
    return X, labels, unique_labels



def train_model(X: pd.DataFrame, y: pd.DataFrame) -> Any:
    
    # train model

    return model


# Preprocess and extract signs from sequence dataset

def process_sequence_image(model, path):
    imgdata = preprocess_image(cv2.imread(path))
    
    # process image

    return result


# Make predictions and output them to output.csv

def predict(model: Any)
    results = []
    with open("dataset_eval.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = {}
            result["subtaskID"] = 1
            result["datapointID"] = row["datapointID"]
            result["answer"] = process_sequence_image(model, row["datapointID"])
            results.append(result)
    
    with open("output.csv", "w") as file:
        # Write the header
        file.write("subtaskID,datapointID,answer\n")
        # Write the prediction sequence
        for result in results:
            file.write(str(result["subtaskID"]))
            file.write(",")
            file.write(result["datapointID"] + ",")
            file.write("|".join(map(str, result["answer"])) + "\n")


X, labels, unique_labels = load_data("dataset_train.csv", data_root_dir='.')

X = pd.DataFrame(X)
labels = pd.DataFrame(labels)

model = train_model(X, Y)

predict(model)
print('Done')

