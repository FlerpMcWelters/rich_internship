import numpy as np
import random
import scipy.stats as stats

def t(mu1, mu2, n): # Calculate the threshold value based on the means and sizes of the sets
    return 0.5*(mu2 + mu1) / np.sqrt(n)
#Refactor code from iterate_exponential_test into a function that takes parameters as inputs
def beta(
n, #Size of Alice and Bob's set
k, #Size of Bob's selection
mu1, #Mean of Alice's distribution
mu2, #Mean of Bob's distribution
param=None, #Ordered pair of parameters for the beta distribution
t, #Threshold value
S_start, #Min value of Bob's random number
S_end, #Max value of Bob's random number
num_trials): #Number of iterations to run the experiment
    a,b = param

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
    
        U = np.random.beta(scale=mu1, size=k) #Random sampling of distribution1 - this is public
        V = np.random.beta(scale=mu2, size=k) #random sampling of distribution2 - this is public

#Generate random selection of half these values

        choiceU = random.sample(tuple(U), int(k/2))
        choiceV = random.sample(tuple(V), int(k/2))
    
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

print(beta(100000, 256, 100, 2000, t, 10000, 1000000, 2000))