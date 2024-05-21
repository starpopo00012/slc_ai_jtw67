import pandas as pd
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Pandas example
data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
df = pd.DataFrame(data)
print("Pandas DataFrame:")
print(df)

# NumPy example
arr = np.array([1, 2, 3])
print("\nNumPy array:")
print(arr)

# SciPy example
def integrand(x):
    return x**2
ans, err = quad(integrand, 0, 1)
print("\nSciPy integration result:")
print(ans)

# Matplotlib example
x = [1, 2, 3]
y = [4, 5, 6]
plt.plot(x, y)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Matplotlib Example")
plt.show()
