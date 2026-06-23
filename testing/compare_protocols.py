""" 
Really slow at the moment
"""

import numpy as np
import random
import matplotlib.pyplot as plt

### AI Generated

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

### End AI Generated Code

from generate_maximum_setUV import iterateMaximum as iterateMaximumSetUV
from generate_minimum_setUV import iterateMinimum as iterateMinimumSetUV
from generate_maximum import iterateMaximum
from generate_minimum import iterateMinimum
from for_profShpilrain.function_exponential import exponential 

"""
The purpose of this script is to visually compare the results of several protocols.
On one plot, see the variation of success rate with respect to generate_maximum,
generate_minimum, generate_maximum_setUV, and generate_minimum_setUV.
"""

candidate_k_values = [8, 32, 128, 256, 512, 1024, 2048, 4096, 8912]

y_axis_minimum = []
y_axis_minimum_setUV = []
y_axis_maximum = []
y_axis_maximum_setUV = []


for x in candidate_k_values:
    y_axis_minimum.append(iterateMinimum(20000, 30000, 100000, x, total_iterations=1000, protocol_iterations=32))
    y_axis_minimum_setUV.append(iterateMinimumSetUV(20000, 30000, 100000, x, total_iterations=1000, protocol_iterations=32))
    y_axis_maximum.append(iterateMaximum(20000, 30000, 100000, x, total_iterations=1000, protocol_iterations=32))
    y_axis_maximum_setUV.append(iterateMaximumSetUV(20000, 30000, 100000, x, total_iterations=1000, protocol_iterations=32))
    

plt.plot(candidate_k_values, y_axis_minimum, label="generate_minimum")
plt.plot(candidate_k_values, y_axis_minimum_setUV, label="generate_minimum_setUV")
plt.plot(candidate_k_values, y_axis_maximum, label="generate_maximum")
plt.plot(candidate_k_values, y_axis_maximum_setUV, label="generate_maximum_setUV")

plt.xlabel("Bob's selection size (k)")
plt.ylabel("Success rate of protocol")
plt.title("Comparison of Protocols")
plt.legend()
plt.show()
