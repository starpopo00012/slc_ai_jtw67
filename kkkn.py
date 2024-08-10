import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Load the dataset
csv = pd.read_csv("Churn Modeling.csv")
df = pd.DataFrame(csv)

# Drop unnecessary columns
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Initialize LabelEncoder
le = LabelEncoder()

# Encode categorical variables
df['Geography'] = le.fit_transform(df['Geography'])
df['Gender'] = le.fit_transform(df['Gender'])

# Check for NaN values
nan_count = df.isnull().sum().sum()
print(f"Number of NaN: {nan_count}")

# Fill NaN values with the mean of the column
df = df.fillna(df.mean())

# Plot correlation matrix
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True)
plt.show()

# Prepare data for modeling
X = df.drop('Exited', axis=1)
y = df['Exited']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the range of k values to test
k_range = range(1, 21)  # Test values from 1 to 20
mean_scores = []

# Evaluate KNN with different k values using cross-validation
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')  # 5-fold cross-validation
    mean_scores.append(scores.mean())

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(k_range, mean_scores, marker='o')
plt.xlabel('Number of Neighbors K')
plt.ylabel('Mean Accuracy')
plt.title('K vs. Mean Accuracy')
plt.xticks(k_range)
plt.grid()
plt.show()

# Print the best k value
best_k = k_range[np.argmax(mean_scores)]
print(f"The best k value is: {best_k}")

# Train a KNN model with the best k value
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = knn.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(f"Score with best k ({best_k}): {accuracy_score(y_test, y_pred)}")

# Plot confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
