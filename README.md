This code is a machine learning model that predicts the price of computer based on various features such as CPU, hard drive, RAM, SSD, graphics RAM, screen size, and stock status.data is collected from https://torob.com/. 
# Data Preprocessing

The first step is to select the relevant features from the dataset and assign them to the X variable. The target variable, which is the price, is assigned to the y variable.

# Dependencies
* numpy
* pandas
* scikit-learn
* xgboost


# usage
Ensure that you have the required libraries installed (pandas, numpy, xgboost, scikit-learn, ...).
Provide the dataset path in the # Load data section.
Run the script, and it will output that is consist of average training and validation errors.
The script also plots the learning curve, showing the training and validation errors for each fold.

