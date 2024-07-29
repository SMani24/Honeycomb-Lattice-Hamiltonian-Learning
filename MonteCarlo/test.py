# Step 1: Import the necessary libraries
import matplotlib.pyplot as plt

# Step 2: Create your data lists
x = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
y2 = [1, 3, 5, 7, 9]

# Step 3: Plot the data on the same figure
plt.plot(x, y1, label='Line 1')  # Plot the first list
plt.plot(x, y2, label='Line 2')  # Plot the second list

# Step 4: Add labels, title, and legend
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')
plt.title('Title of the Plot')
plt.legend()

# Step 5: Display the plot
plt.show()
