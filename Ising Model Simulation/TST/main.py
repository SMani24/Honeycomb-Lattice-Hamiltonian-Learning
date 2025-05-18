import matplotlib.pyplot as plt
import csv


file_names = ["1e4_1.csv", "1e4_2.csv", "1e4_3.csv", "1e5.csv"]


y_values = [0, 0.05, 0.1, 0.15, 0.2]


x_values_list = []
for file in file_names:
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x_values = list(map(float, row))  
            x_values_list.append(x_values)


plt.figure(figsize=(8, 6))
for i, x_values in enumerate(x_values_list):
    plt.plot(x_values, y_values, marker='o', linestyle='-', label=file_names[i])

plt.xlabel("Vertex Flip probability, p")
plt.ylabel("Single Qubit error probability, er")
plt.title("")
plt.legend()
plt.grid()
plt.show()
