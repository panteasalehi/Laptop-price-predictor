import pandas as pd
import re
from sklearn.linear_model import LinearRegression


dataset_address = 'drive/MyDrive/data.csv'


from google.colab import drive
drive.mount('drive')

from sklearn import preprocessing

df = pd.read_csv(dataset_address)


df.isnull()

check_null = df.isnull()  # it will be true if the value is null
print("\n ssd:")
print(df['ssd'].unique())
ssd_list = df['ssd'].unique()
# we have gb and tb

print("\n hdd:")
print(df['hdd'].unique())
# we have gb and tb

print("\n ram:")
print(df['ram'].unique())
# we have gb

print("\n graphic_ram:")
print(df['graphic_ram'].unique())
# we have gb and mg


print("\n screen_size:")
print(df['screen_size'].unique())

print("\n cpu:")
print(df['cpu'].unique())
# we have inch

ssd_avg = 0
ssd_num = 0
hdd_avg = 0
hdd_num = 0
ram_avg = 0
ram_num = 0
graphic_ram_avg = 0
graphic_ram_num = 0
screen_size_avg = 0.0
screen_size_num = 0.0

for i in range(len(df['ssd'])):
    if not check_null['ssd'][i]:
        if " tb" in df['ssd'][i]:
            df.loc[i, 'ssd'] = int(str(re.findall("\d+", df['ssd'][i])[0]) + "000000000000")
        elif " gb" in df['ssd'][i]:
            df.loc[i, 'ssd'] = int(str(re.findall("\d+", df['ssd'][i])[0]) + "000000000")
        ssd_avg += int(df['ssd'][i])
        ssd_num += 1

    if not check_null['hdd'][i]:
        if " tb" in df['hdd'][i]:
            df.loc[i, 'hdd'] = int(str(re.findall("\d+", df['hdd'][i])[0]) + "000000000000")
        elif " gb" in df['hdd'][i]:
            df.loc[i, 'hdd'] = int(str(re.findall("\d+", df['hdd'][i])[0]) + "000000000")
        hdd_avg += int(df['hdd'][i])
        hdd_num += 1

    if not check_null['graphic_ram'][i]:
        if not "unified" in df['graphic_ram'][i]:
            if " mb" in df['graphic_ram'][i]:
                df.loc[i, 'graphic_ram'] = int(str(re.findall("\d+", df['graphic_ram'][i])[0]) + "000000")
            elif " gb" in df['graphic_ram'][i]:
                df.loc[i, 'graphic_ram'] = int(str(re.findall("\d+", df['graphic_ram'][i])[0]) + "000000000")
            graphic_ram_avg += int(df['graphic_ram'][i])
            graphic_ram_num += 1
        else:
          check_null['graphic_ram'][i] = True



    if not check_null['ram'][i]:

        if " gb" in df['ram'][i]:
            df.loc[i, 'ram'] = int(str(re.findall("\d+", df['ram'][i])[0]) + "000000000")
        elif " mb" in df['ram'][i]:
            df.loc[i, 'ram'] = int(str(re.findall("\d+", df['ram'][i])[0]) + "000000")
        ram_avg += int(df['ram'][i])
        ram_num += 1

    if not check_null['screen_size'][i]:
        df.loc[i, 'screen_size'] = float(str(re.findall("(\d+([.,]\d*)?)", df['screen_size'][i])[0][0]))
        screen_size_avg += float(df['screen_size'][i])
        screen_size_num += 1






screen_size_avg /= screen_size_num
ram_avg /= ram_num
graphic_ram_avg /= graphic_ram_num
ssd_avg /= ssd_num
hdd_avg /= hdd_num

print(screen_size_avg)
print(ram_avg)
print(graphic_ram_avg)
print(ssd_avg)
print(hdd_avg)



df["hdd"].fillna(hdd_avg, inplace=True)
df["ssd"].fillna(hdd_avg, inplace=True)
df["graphic_ram"].fillna(graphic_ram_avg, inplace=True)
df["ram"].fillna(ram_avg, inplace=True)
df["screen_size"].fillna(screen_size_avg, inplace=True)
df.loc[df["graphic_ram"] == "unified", "graphic_ram"] = graphic_ram_avg

# in graphic ram we have 'unified' so we should use one hot encoding
df['stock_status'] = df['stock_status'].astype('category')
df['stock_status'] = df['stock_status'].cat.codes



df = df[df['cpu'].notna()]

df['cpu'] = df['cpu'].astype('category')
df['cpu'] = df['cpu'].cat.codes

#df2 = df
#print(df.to_string())
#df['ssd'] = (preprocessing.normalize([df2['ssd']]).flatten())
#df['hdd'] = (preprocessing.normalize([df2['ssd']]).flatten())
#df['ram'] = (preprocessing.normalize([df2['ssd']]).flatten())
#df['graphic_ram'] = (preprocessing.normalize([df2['ssd']]).flatten())
#df['price'] = (preprocessing.normalize([df2['ssd']]).flatten())

print("ssd")
print(df['ssd'].max())
print(df['ssd'].min())

print("hdd")
print(df['hdd'].max())
print(df['hdd'].min())

print("ram")
print(df['ram'].max())
print(df['ram'].min())

print("graphic_ram")
print(df['graphic_ram'].max())
print(df['graphic_ram'].min())



import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#df = pd.read_csv(dataset_address)

# Extract features and target variable
X = df[['cpu', 'hdd', 'ram', 'ssd', 'graphic_ram', 'screen_size', 'stock_status']]
y = df['price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the random forest regressor
rf = RandomForestRegressor()

# Perform k-fold cross validation with different values of k
k_values = [5, 10, 15]
for k in k_values:
  kf = KFold(n_splits=k)
  scores = cross_val_score(rf, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
  #cross-validation divide data into training/validation set.
  #trained on the training set, performance evaluated on validation set
  mse = -1 * scores.mean()
  print(f'Mean squared error for {k}-fold cross validation: {mse:.2f}')

# Train the model on the entire training set
rf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = rf.predict(X_test)


# Calculate the accuracy score
accuracy = rf.score(X_test, y_test)
print(f'Accuracy score: {accuracy:.2f}')

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean squared error: {mse:.2f}')

# Plot the learning and validation curve
train_scores, val_scores = [], []
n_estimators_range = range(1, 101, 10)
for n_estimators in n_estimators_range:
    rf = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    train_score = cross_val_score(rf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    val_score = cross_val_score(rf, X_test, y_test, cv=5, scoring='neg_mean_squared_error')
    train_scores.append(-1 * train_score.mean())
    val_scores.append(-1 * val_score.mean())

plt.plot(n_estimators_range, train_scores, label='Training error')
plt.plot(n_estimators_range, val_scores, label='Validation error')
plt.xlabel('Number of estimators')
plt.ylabel('Mean squared error')
plt.legend()
plt.show()

# Import libraries
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn import preprocessing

# Load data


# Split data into features and target variable
X = df[['cpu', 'hdd', 'ram', 'ssd', 'graphic_ram', 'screen_size']]
y = df['price']

# Define the number of folds for cross validation
k_folds = [3, 5, 7, 10]

for k in k_folds:
    # Define the model
    model = xgb.XGBRegressor()

    # Define the k-fold cross validation
    kf = KFold(n_splits=k, shuffle=True)

    # Initialize lists to hold the training and validation errors
    train_errors = []
    val_errors = []

    le = preprocessing.LabelEncoder()
    y = le.fit_transform(y)

    # Perform k-fold cross validation
    for train_index, val_index in kf.split(X):
        # Split the data into training and validation sets
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y[train_index], y[val_index]
        le = preprocessing.LabelEncoder()
        y_train = le.fit_transform(y_train)

        # Train the model on the training set
        model.fit(X_train.values, y_train)

        # Compute the training error
        y_train_pred = model.predict(X_train.values)
        train_error = mean_squared_error(y_train, y_train_pred)
        train_errors.append(train_error)

        # Compute the validation error
        y_val_pred = model.predict(X_val.values)
        val_error = mean_squared_error(y_val, y_val_pred)
        val_errors.append(val_error)

    # Compute the average training and validation errors
    avg_train_error = np.mean(train_errors)
    avg_val_error = np.mean(val_errors)





    # Plot the learning curve
    plt.figure()
    plt.plot(range(k), train_errors, label='Training Error')
    plt.plot(range(k), val_errors, label='Validation Error')
    plt.xlabel('Fold')
    plt.ylabel('Mean Squared Error')
    plt.title('Learning Curve ({}-fold cross validation)'.format(k))
    plt.legend()

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb

#df = pd.read_csv(dataset_address)

# Extract features and target variable
X = df[['cpu', 'hdd', 'ram', 'ssd', 'graphic_ram', 'screen_size', 'stock_status']]
y = df['price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the random forest regressor
rf = xgb.XGBRegressor()

# Perform k-fold cross validation with different values of k
k_values = [5, 10, 15]
for k in k_values:
  kf = KFold(n_splits=k)
  scores = cross_val_score(rf, X_train.values, y_train, cv=kf, scoring='neg_mean_squared_error')
  mse = -1 * scores.mean()
  print(f'Mean squared error for {k}-fold cross validation: {mse:.2f}')

# Train the model on the entire training set
rf.fit(X_train.values, y_train)

# Make predictions on the testing set
y_pred = rf.predict(X_test.values)

# Calculate the accuracy score
accuracy = rf.score(X_test.values, y_test)
print(f'Accuracy score: {accuracy:.2f}')

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean squared error: {mse:.2f}')

# Plot the learning and validation curve
train_scores, test_scores = [], []
n_estimators_range = range(1, 101, 10)
for n_estimators in n_estimators_range:
    rf = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    train_score = cross_val_score(rf, X_train.values, y_train, cv=5, scoring='neg_mean_squared_error')
    test_score = cross_val_score(rf, X_test.values, y_test, cv=5, scoring='neg_mean_squared_error')
    train_scores.append(-1 * train_score.mean())
    test_scores.append(-1 * test_score.mean())

plt.plot(n_estimators_range, train_scores, label='Training error')
plt.plot(n_estimators_range, test_scores, label='Validation error')
plt.xlabel('Number of estimators')
plt.ylabel('Mean squared error')
plt.legend()
plt.show()

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold



# Split features and target variable
X = df.drop(['price'], axis=1)
y = df['price']

# Define number of folds for cross-validation
n_splits = 10

# Create instance of k-fold object
kf = KFold(n_splits=n_splits)

# Initialize lists to store training and validation errors
train_errors = []
val_errors = []

# Iterate through each fold
for train_index, val_index in kf.split(X):

    # Split data into training and validation sets
    X_train, X_val = X.iloc[train_index], X.iloc[val_index]
    y_train, y_val = y.iloc[train_index], y.iloc[val_index]

    # Fit linear regression model on training set
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # Calculate training and validation errors
    train_pred = lr.predict(X_train)
    train_error = mean_squared_error(y_train, train_pred)
    train_errors.append(train_error)

    val_pred = lr.predict(X_val)
    val_error = mean_squared_error(y_val, val_pred)
    val_errors.append(val_error)

# Calculate mean training and validation errors
mean_train_error = np.mean(train_errors)
mean_val_error = np.mean(val_errors)

# Calculate accuracy (R^2 score)
accuracy = lr.score(X, y)

print('Mean Training Error:', mean_train_error)
print('Mean Validation Error:', mean_val_error)
print('Accuracy (R^2 Score):', accuracy)
