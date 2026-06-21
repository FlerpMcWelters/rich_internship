"""
This will run the protocol for a given number of iterations and return
the highest value of E-S/n over those iterations.
Bob will assume that Alice selected the same distribution as him in that
scenario. We will test the success rate of this strategy calculated as the
number of times Bob is correct in assuming Alice's distribution is the same
as his distribution over the total number of iterations.

This differs from the previous protocol in that Bob will not have a threshold
value that tells Bob whether to pick 1 or 0, he will rather always select the
bit associated with his distribution and assume that Alice selected different.
"""

import numpy as np
import random   

#mu1 and mu2 are means/parameters of distributions
#n is the total number of samples when Bob and Alice sum their samples together
#k is the number of samples Bob takes
#protocol_iterations is the number of times we run the protocol

def generate_maximum(mu1, mu2, n, k, protocol_iterations=8):

    bobLen = protocol_iterations
    listS = [0]*bobLen
    listE = [0]*bobLen
    bobList = [0]*bobLen
    aliceList = [0]*bobLen

    for i in range(protocol_iterations):

        S = random.randint(10000,1000000)
        listS[i] = S

        bobChoice = random.choice(["U","V"])

        bobList[i] = bobChoice
    
        U = np.random.exponential(scale=mu1, size=k) #Random sampling of distribution1 - this is public


        V = np.random.exponential(scale=mu2, size=k) #random sampling of distribution2 - this is public

        choiceU = random.sample(tuple(U), int(k/2))
        choiceV = random.sample(tuple(V), int(k/2))

        sum_sampleU = sum(choiceU)+S
        sum_sampleV = sum(choiceV)+S

        if bobChoice == "U":
            aliceSample = sum_sampleU
        elif bobChoice == "V":
            aliceSample = sum_sampleV
        else:
            print("error")

        aliceChoice = random.choice(["Distribution 1","Distribution 2"])

        aliceList[i] = aliceChoice

        if aliceChoice == "Distribution 1":
            x = np.random.exponential(scale=mu1, size=int(n-(k/2)))
            aliceSum = sum(x) + aliceSample
        elif aliceChoice == "Distribution 2":
            y = np.random.exponential(scale=mu2, size=int(n-(k/2)))
            aliceSum = sum(y) + aliceSample
        else:
            print("problem")

        A = aliceSum/n

        if aliceChoice == "Distribution 1":
            E = A - mu1
        elif aliceChoice == "Distribution 2":
            E = A - mu2
        else:
            print("problem")

        listE[i] = E

        listS_over_n  = [x * 1/n for x in listS]
        listDiff = [abs(x - y) for x, y in zip(listE, listS_over_n)]
    
        minIndex = listDiff.index(min(listDiff))
    
    if (bobList[minIndex] == "U") and (aliceList[minIndex] == "Distribution 2"):
        return 1
    elif (bobList[minIndex] == "V") and (aliceList[minIndex] == "Distribution 1"):
        return 1
    else:
        return 0


#Iterate maximum will execute the protocol a given number of times and return the success rate       
#recall that n-k is alice's amount.
def iterateMaximum(mu1, mu2, n, k, protocol_iterations=8,total_iterations=8):
    successCount = 0
    for i in range(total_iterations):
        successCount += generate_maximum(mu1, mu2, n, k, protocol_iterations)
    return successCount/total_iterations

print(iterateMaximum(20000, 20500, 100000, 16, 8, 1000))