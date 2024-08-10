import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Load the dataset
csv = pd.read_csv("Churn Modeling.csv")
df = pd.DataFrame(csv)

df = df.drop('RowNumber', axis=1)
df = df.drop('CustomerId', axis=1)
df = df.drop('Surname', axis=1)

print(df.info())

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

# Binning certain columns in training data
X_train['Age'] = pd.cut(X_train['Age'], 
                        bins=[0, 30, 40, 50, 60, 70, 80, 90, 100], 
                        labels=['0', '30', '40', '50', '60', '70', '80', '90'])

X_train['Balance'] = pd.cut(X_train['Balance'], 
                            bins=[0, 50000, 100000, 150000, 200000, 250000], 
                            labels=['0', '50000', '100000', '150000', '200000'])

X_train['EstimatedSalary'] = pd.cut(X_train['EstimatedSalary'], 
                                    bins=[0, 50000, 100000, 150000, 200000, 250000], 
                                    labels=['0', '50000', '100000', '150000', '200000'])

# Check for NaN values after binning
print(X_train.isnull().sum())

# Fill NaN values if any
X_train = X_train.fillna(X_train.mode().iloc[0])

# Train a decision tree model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Prepare test data similarly (binning should be applied if necessary)
X_test['Age'] = pd.cut(X_test['Age'], 
                       bins=[0, 30, 40, 50, 60, 70, 80, 90, 100], 
                       labels=['0', '30', '40', '50', '60', '70', '80', '90'])

X_test['Balance'] = pd.cut(X_test['Balance'], 
                           bins=[0, 50000, 100000, 150000, 200000, 250000], 
                           labels=['0', '50000', '100000', '150000', '200000'])

X_test['EstimatedSalary'] = pd.cut(X_test['EstimatedSalary'], 
                                   bins=[0, 50000, 100000, 150000, 200000, 250000], 
                                   labels=['0', '50000', '100000', '150000', '200000'])

# Fill NaN values in test data if any
X_test = X_test.fillna(X_test.mode().iloc[0])

# Predict and evaluate the model
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(f"Score: {accuracy_score(y_test, y_pred)}")

# Plot confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

# Optionally, plot the decision tree
plt.figure(figsize=(20,10))
plot_tree(model, filled=True, feature_names=X.columns)
plt.show()
