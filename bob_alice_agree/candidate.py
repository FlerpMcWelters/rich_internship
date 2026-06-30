"""

Here is a procedure that could help determine the threshold experimentally.

1. Bob always uses the set U.
2. Alice always uses the distribution that corresponds to the set U.
3. By running the protocol multiple times, Bob gets a dataset of {E_i - S_i/n}. Bob then selects a value from this dataset that would give a success rate over 0.8, say.
That would be a value t such that 80% of the values in the dataset are less than t.

VS
"""

import numpy as np
import random
import matplotlib.pyplot as plt

#Everytime this script is run, 

n = 100000 #size of Bob and Alice's set
k = 64 #size of Bob's selection from U
mu = 20000 #mean of distro 
mu2 = 50000
num_trials = 1500

candidate_list_U = []

U = np.random.exponential(scale=mu, size = 2*k) #Bob's set.

#Run protocol several times to get a dataset of E-S/n values.

for i in range(num_trials):
    
    S = random.randint(10000,1000000) #Bob's random number

    bobChoice  = random.sample(tuple(U), int(k)) #samples k times from U

    aliceSum = sum(bobChoice) + S #combines Bob's samples with his private key to be sent to Alice

    aliceSample = np.random.exponential(scale=mu, size = int(n-k)) #alice fills out the transmission with n-k samples of her distribution

    A = (aliceSum+sum(aliceSample))/n #Alice takes the mean

    E = A - mu #Subtracts the mean of her distribution
    
    threshold_candidate = abs(E - S/n) #This is what Bob computes when he receives E.

    candidate_list_U.append(threshold_candidate) #Adds the result to a list

experimental_threshold_U = np.percentile(candidate_list_U, 80) #This is the threshold value that gives a success rate of 0.8
print(f"The 80th percentile for a threshold where they use U is: {experimental_threshold_U}")

#The protocol below looks at how much the threshold can vary.
"""
#Now let's see the variance of this process
experimental_threshold_list = []
for i in range(100):
    candidate_list = []
    for i in range(num_trials):
    
        S = random.randint(10000,1000000) #Bob's random number

        bobChoice  = random.sample(tuple(U), int(k))

        aliceSum = sum(bobChoice) + S

        aliceSample = np.random.exponential(scale=mu, size = int(n-k))

        A = (aliceSum+sum(aliceSample))/n

        E = A - mu
        
        threshold_candidate = abs(E - S/n)

        candidate_list.append(threshold_candidate)

    experimental_threshold = np.percentile(candidate_list, 80)
    experimental_threshold_list.append(experimental_threshold)

print(experimental_threshold_list[:15])
print(np.var(experimental_threshold_list))
"""

#We can perform the same computation for distribution 2 if we'd like, and compare.
candidate_list_V = []
V = np.random.exponential(scale=mu2, size = 2*k) #Bob's set.
for i in range(num_trials):
    
    S = random.randint(10000,1000000) #Bob's random number

    bobChoice  = random.sample(tuple(V), int(k)) #samples k times from V

    aliceSum = sum(bobChoice) + S #combines Bob's samples with his private key to be sent to Alice

    aliceSample = np.random.exponential(scale=mu2, size = int(n-k)) #alice fills out the transmission with n-k samples of her distribution

    A = (aliceSum+sum(aliceSample))/n #Alice takes the mean

    E = A - mu2 #Subtracts the mean of her distribution
    
    threshold_candidate = abs(E - S/n) #This is what Bob computes when he receives E.

    candidate_list_V.append(threshold_candidate) #Adds the result to a list

experimental_threshold_V = np.percentile(candidate_list_V, 80) #This is the threshold value that gives a success rate of 0.8
print(f"The 80th percentile for a threshold where they use V is: {experimental_threshold_V}")



#Now what if Bob and Alice's dstributions don't agree? Let Bob have distro 1 (i.e. U)
#and Alice has distro 2 (i.e. V)

candidate_list_disagree = []

for i in range(num_trials):
    
    S = random.randint(10000,1000000) #Bob's random number

    bobChoice  = random.sample(tuple(U), int(k)) #samples k times from U

    aliceSum = sum(bobChoice) + S #combines Bob's samples with his private key to be sent to Alice

    aliceSample = np.random.exponential(scale=mu2, size = int(n-k)) #alice fills out the transmission with n-k samples of her distribution

    A = (aliceSum+sum(aliceSample))/n #Alice takes the mean

    E = A - mu2 #Subtracts the mean of her distribution
    
    threshold_candidate = abs(E - S/n) #This is what Bob computes when he receives E.

    candidate_list_disagree.append(threshold_candidate) #Adds the result to a list

experimental_threshold_disagree = np.percentile(candidate_list_disagree, 80) #This is the threshold value that gives a success rate of 0.8
print(f"The 80th percentile for a threshold where they disagree is: {experimental_threshold_disagree}")

print(f"The minimum result for when they disagree was {min(candidate_list_disagree)}")
print(f"The minimum result for when they agree (U) was {min(candidate_list_U)}")
print(f"The maximum result for when they disagree was {max(candidate_list_disagree)}")
print(f"The maximum result for when they agree (U) was {max(candidate_list_U)}")
print(f"The minimum result for when they agree (V) is {min(candidate_list_V)}")
print(f"The maximum result for when they agree (V) is {max(candidate_list_V)}")
"""
I am interested now in the difference between the 80th percentile when they agree and when they disagree. 
Obviously the disagree threshold is higher, but how many of those entries are higher than the agree threshold?
"""
#With these diagnostics, let's now run the protocol using the experimentally derived thresholds.
success = 0
inconclusive = 0
failure = 0

for j in range(num_trials):
    bobGuess = None
    S = random.randint(10000,1000000) #Bob's random number

    bobChoice  = random.sample(tuple(U), int(k)) #samples k times from U

    aliceSum = sum(bobChoice) + S #combines Bob's samples with his private key to be sent to Alice

    alice_choice = random.choice(["Distribution 1", "Distribution 2"]) #Alice randomly chooses a distribution

    if alice_choice == "Distribution 1":
        aliceSample = np.random.exponential(scale=mu, size = int(n-k)) #alice fills out the transmission with n-k samples of her distribution
        A = (aliceSum+sum(aliceSample))/n #Alice takes the mean
        E = A - mu #Subtracts the mean of her distribution
    elif alice_choice == "Distribution 2":
        aliceSample = np.random.exponential(scale=mu2, size = int(n-k)) #alice fills out the transmission with n-k samples of her distribution
        A = (aliceSum+sum(aliceSample))/n #Alice takes the mean
        E = A - mu2 #Subtracts the mean of her distribution
    #This value E is sent back to Bob, who will use the experimentally determined threshold to determine if they agree or not.

    if abs(E-S/n) <= experimental_threshold_U: #Bob uses the threshold derived from when they agree on U
        bobGuess = "Distribution 1"
    elif abs(E-S/n) >= experimental_threshold_disagree: #Bob uses the threshold derived from when they disagree
        bobGuess = "Distribution 2"
    
    if bobGuess == alice_choice:
        success += 1
    elif (bobGuess != alice_choice) and (bobGuess != None):
        failure += 1
    elif bobGuess == None:
        inconclusive += 1
    
print(success/num_trials)
print(inconclusive/num_trials)
print(failure/num_trials)