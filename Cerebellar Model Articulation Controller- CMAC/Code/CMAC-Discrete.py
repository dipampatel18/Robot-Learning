# ENPM808F Robot Learning
# Assignment-2: CMAC
# Created By: DIPAM PATEL (115809833)

import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

# 100 Points for Division of Sine Curve:
div_points = np.arange(0, 100)

# Creating a Unit Step Value:
x = 0.0628  # (2 * pi)/100 = 0.0628
y = np.arange(0)

# Using the Sine Curve for Training
for i in range(0, 100):
    s_curve = math.sin((div_points[np.array(i)]) * x)
    y = np.append(y, s_curve)

M = np.dstack((div_points * x, y))

# Selecting 70 Random Points for Training:
train_num = np.arange(0)
while (train_num.size < 70):
    rand_num = random.randint(0, 99)
    if ((rand_num in train_num) is False):
        train_num = np.append(train_num, rand_num)

train_num = np.sort(train_num)

# Selecting Remaining 30 Random Points for Testing:
test_num = np.arange(0)
while (test_num.size < 30):
    rand_num = random.randint(0, 99)
    if (((rand_num in train_num) == False) and ((rand_num in test_num) == False)):
        test_num = np.append(test_num, rand_num)

test_num = np.sort(test_num)

# Initializing Variables
w_value = 0.0
w_zero = np.arange(0.0)
w_save = w_save2 = w_save3 = w_zero
e_array = mean_sq_array = time_array = time_gen_array = w_rand = w_weight_save = w_weight_save2 = w_weight_save3 = np.arange(0)
mean_sq = 1
start = time.time()  # To Measure Time for Training/Testing

for gen in range(1, 37, 2):
    print(gen)
    weight = np.random.rand(35)  # Weights for the Network
    padding = (gen - 1) / 2
    w_zero = np.array([0])

    for i in range(int(padding)):  # Creating a Layer of Padding on both the Ends
        weight = np.append(w_zero, weight)
        weight = np.append(weight, w_zero)

    while (mean_sq > 0.01):
        w_rand = np.arange(0)

        # Training Phase
        for j in range(0, 70):
            q_value = j / 2

            for k in range(gen):
                w_value = w_value + weight[np.array(int(k) + int(q_value))]

            w_new_value = w_value / gen
            y_value = (math.sin(train_num[np.array(j)] * x))

            e_value = y_value - w_new_value
            e_array = np.append(e_array, e_value)
            corrected_val = e_value / gen  # Error Correction

            for k in range(gen):
                weight[np.array(int(k) + int(q_value))] = (weight[np.array(int(k) + int(q_value))]) + corrected_val

            w_value = 0.0

        mean_sq = np.mean(e_array ** 2)

    # Trying Different Values of Generalization Factor

    if gen == 3:
        w_save = w_rand
        w_weight_save = weight

    if gen == 5:
        w_save2 = w_rand
        w_weight_save2 = weight

    if gen == 7:
        w_save3 = w_rand
        w_weight_save3 = weight

    time_gen_array = np.append(time_gen_array, gen)
    end = time.time()
    time_array = np.append(time_array, (end - start))
    mean_sq_array = np.append(mean_sq_array, mean_sq)
    mean_sq = 1

print(mean_sq_array, 'Error')

w_new = w_weight_save[1::2]
w_new2 = w_weight_save2[1::2]
w_new3 = w_weight_save3[1::2]

new_gen = 3
new_gen2 = 5
new_gen3 = 7

w_new_array = np.arange(0)
w_new_array2 = np.arange(0)
w_new_array3 = np.arange(0)

# Testing Phase
for j in range(0, 30):
    q_value = j / 2
    w_average = w_new[np.array(int(q_value))] + w_new[np.array(int(q_value) - 1)] + w_new[np.array(int(q_value) + 1)]
    w_average = w_average / new_gen
    w_new_array = np.append(w_new_array, w_average)

    w_average2 = w_new2[np.array(int(q_value))] + w_new2[np.array(int(q_value) - 1)] + w_new2[np.array(int(q_value) + 1)]
    w_average2 = w_average2 / new_gen2
    w_new_array2 = np.append(w_new_array2, w_average2)

    w_average3 = w_new3[np.array(int(q_value))] + w_new3[np.array(int(q_value) - 1)] + w_new3[np.array(int(q_value) + 1)]
    w_average3 = w_average3 / new_gen3
    w_new_array3 = np.append(w_new_array3, w_average3)


new_test_num = test_num * x
x_tested = div_points * x

# Plotting the Output Graphs

# Gen 1
plt.figure(1)
plt.plot(new_test_num, w_new_array, '-b', label="Testing Curve (gen = 3)")
plt.plot(new_test_num, w_new_array2, '-g', label="Testing Curve (gen = 5)")
plt.plot(new_test_num, w_new_array3, '-r', label="Testing Curve (gen = 7)")
plt.plot(x_tested, y, '-k', label="Input Curve", linewidth=2)
plt.title("Different Generalization Factors")
plt.xlabel('Radians')
plt.ylabel('sin(x)')
plt.legend(loc='upper right')

plt.figure(2)
plt.plot(time_gen_array, mean_sq_array, '-k')
plt.xlabel("Generalization")
plt.ylabel("Error")

plt.figure(3)
plt.plot(time_gen_array, time_array, '-g')
plt.xlabel("Generalization")
plt.ylabel("Time")
plt.show()
