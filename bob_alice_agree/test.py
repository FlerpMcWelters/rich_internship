import numpy as np
import random

np.random.seed(42)

mu = 100000
k=4
num_trials = 100
trial_list = []

for i in range(num_trials):
    sample = np.random.exponential(scale=mu, size = 2*k)

    selection = random.sample(tuple(sample), int(k))

    mean = np.mean(selection)
    trial_list.append(mean)

#print(trial_list)
print(f"minimum:{min(trial_list)}")
print(f"maximum:{max(trial_list)}")
print(f"80th percentile:{np.percentile(trial_list, 80)}")