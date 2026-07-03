import numpy as np
import random
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import sklearn as sk
from pathlib import Path

def t(mu1, mu2, n): # Calculate the threshold value based on the means and sizes of the sets
    return (mu2 + mu1) / np.sqrt(n)

#Refactor code from iterate_exponential_test into a function that takes parameters as inputs
def exponential(
n, #Size of Alice and Bob's set
k, #Size of Bob's selection
mu1, #Mean of Alice's distribution
mu2, #Mean of Bob's distribution
t, #Threshold value as function of mu1, mu2, and n
S_start, #Min value of Bob's random number
S_end, #Max value of Bob's random number
num_trials): #Number of iterations to run the experiment
    
    num_successes = 0 # Initialize the number of successes

    outcomecount1 = 0
    outcomecount2 = 0
    outcomecount3 = 0
    outcomecount4 = 0

    t_value = t(mu1, mu2, n) # Calculate the threshold value

    for i in range(num_trials): 
        
        S = random.randint(S_start, S_end) # Bob's random number

#Bob randomly selects set
    
        bobChoice = random.choice(["U","V"])
    
#Establish sets
    
        U = np.random.exponential(scale=mu1, size=k) #Random sampling of distribution1 - this is public
        V = np.random.exponential(scale=mu2, size=k) #random sampling of distribution2 - this is public

#Generate random selection of half these values

        choiceU = random.sample(tuple(U), int(k//2))
        choiceV = random.sample(tuple(V), int(k//2))
    
#Sum sets with S
    
        sum_sampleU = sum(choiceU)+S
        sum_sampleV = sum(choiceV)+S

#Establish what to send to Alice

        if bobChoice == "U":
            aliceSample = sum_sampleU
        elif bobChoice == "V":
            aliceSample = sum_sampleV
        else:
            print("error")

#Alice now flips a coin to pick a distribution

        aliceChoice = random.choice(["Distribution 1","Distribution 2"])

#Alice now generates and adds n-(k/2) samples of chosen distribution to Bob's transmission
    
        if aliceChoice == "Distribution 1":
            x = np.random.exponential(scale=mu1, size=int(n-(k/2)))
            aliceSum = sum(x) + aliceSample
        elif aliceChoice == "Distribution 2":
            y = np.random.exponential(scale=mu2, size=int(n-(k/2)))
            aliceSum = sum(y) + aliceSample
        else:
            print("problem")
        
#Now alice divides this value by n: call this A

        A = aliceSum/n

#Alice will send E = A - u to Bob where u is either mu1 or mu2 depending on Alice's choice

        if aliceChoice == "Distribution 1":
            E = A - mu1
        elif aliceChoice == "Distribution 2":
            E = A - mu2
        else:
            print("problem")

        if abs(E-S/n) <= t_value:#then they agree on the distribution and bob knows shared bit is 1 if he chose d1 and 0 otherwise
            if bobChoice == "U":
                sharedBit = 1
                outcomecount1 += 1
            elif bobChoice == "V":
                sharedBit = 0
                outcomecount2 += 1
                #print(bobChoice)
            else:
                print("problem")
        elif abs(E- S/n) > t_value: #bob selected a diff distro than alice - bob still knows alice's distribution
            if bobChoice == "U":
                sharedBit=0
                outcomecount3 += 1
                #print(bobChoice)
            elif bobChoice == "V":
                sharedBit = 1
                outcomecount4 += 1
            else:
                print("problem")

#Establish if they selected the same distribution and count number of successes.
    
        if (sharedBit == 1) and (aliceChoice == "Distribution 1"):
            num_successes += 1
            #print("Success")
        elif (sharedBit == 0) and (aliceChoice == "Distribution 2"):
            num_successes += 1
            #print("Success")
        #else:
            #print("failure")

    print(f"Threshold value: {t_value}")
    print(f"Number of successes: {num_successes}")
    print(f"Success rate: {num_successes/num_trials}")

    print(f"Under threshold, distribution 1: {outcomecount1}")
    print(f"Under threshold, distribution 2: {outcomecount2}")
    print(f"Over threshold, distribution 1: {outcomecount3}")
    print(f"Over threshold, distribution 2: {outcomecount4}")
    return (num_successes/num_trials)
#print(exponential(100000, 256, 100, 2000, t, 10000, 1000000, 2000))

#Try an array of values and graph success rate based on x.

n_test = 100000
k_test = 32
mu1_test = 1
mu2_test = 30000
t_val_test = t(mu1_test, mu2_test, n_test)
start_test = 10000
end_test = 1000000
num_trials_test = 1000

output_dir = Path(r"/Users/matt/Desktop/rich internship images") 
#Change directory to whereever you'd like to save images.

x_axis = [] #create empty array to store x values (Bob's selection size)

y_axis = [] #create empty array to store y values (success rate of protocol based on Bob's selection size)

range_x = np.linspace(2, 7000, 40).round().astype(int) #creates the values tested for each parameter

for x in range_x: #Edit possible x values here!
    x_axis = np.append(x_axis, x)
    y_axis = np.append(y_axis, exponential(n_test, x, mu1_test, mu2_test, t, start_test, end_test, num_trials_test))
    print(f"Bob's selection size: {x}")
    #print(exponential(100000, x, 20000, 20500, t, 10000, 1000000, 2000))
"""coeff = np.polyfit(x_axis, y_axis, 1)
poly1d_fn = np.poly1d(coeff)

# poly1d_fn is now a function which takes in x and returns an estimate for y

plt.plot(x_axis,y_axis, 'yo', x_axis, poly1d_fn(x_axis), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.plot(x_axis, y_axis)
plt.xlim(0, 6000)
plt.ylim(0, 1)

plt.figtext(.6, .4, f"Threshold value: {round(t_val_test, 2)}")
plt.figtext(.7, .35, f"n: {n_test}")
plt.figtext(.7, .3, f"mu1: {mu1_test}")
plt.figtext(.7, .25, f"mu2: {mu2_test}")
plt.figtext(.5, .2, f"Trials per candidate value: {num_trials_test}")


plt.xlabel("Bob's selection size")
plt.ylabel("Success rate")
plt.title(f"Success rate of protocol based on Bob's selection size with threshold value {t(20000, 30000, 100000)}")
plt.savefig(output_dir / f"t={t_val_test}_n={n_test}_mu1={mu1_test}_mu2={mu2_test}_trials={num_trials_test}.png")
plt.show()"""