# In the name of God
# SMani24
# Ali Kookani

import multiprocessing as mp
import ExpectationValueCalculator
import SignCalculator
import time
import os

startTime = time.time()

def generateExpectationValueJobs():
    jobs = []
    inputDir = f"../MoneCarlo/MCOutput/"
    outputDir = f"./ExpectationValues/"
    for latticeSize in [8]:
        for beta in [0.5]:
            for singleQubitErrorProbability in [0]:
                for configNumber in range(0, 1000):
                    filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                    inputFilePath = inputDir + filePath + f"configNumber={configNumber}.csv"
                    vertex_A_ExpectationValueFilePath = outputDir + filePath + f"vertex_A_ExpectationValue_configNumber={configNumber}.csv"
                    link_A_ExpectationValueFilePath = outputDir + filePath + f"link_A_ExpectationValue_configNumber={configNumber}.csv"
                    job = (inputFilePath, vertex_A_ExpectationValueFilePath, link_A_ExpectationValueFilePath, latticeSize)
                    print(job)
                    jobs.append(job)
    return jobs

def generateSingJobs():
    jobs = []
    inputDir = f"../MoneCarlo/MCOutput/"
    outputDir = f"./Signs/"
    for latticeSize in [8]:
        for beta in [0.5]:
            for singleQubitErrorProbability in [0]:
                for configNumber in range(0, 1000):
                    filePath = f"latticeSize={latticeSize}/Beta={beta}/singleQubitErrorProbability={singleQubitErrorProbability}/"
                    stateFilePath = inputDir + filePath + f"configNumber={configNumber}.csv"
                    singFilePath = outputDir + filePath + f"sign_configNumber={configNumber}.csv"
                    job = (stateFilePath, singFilePath, latticeSize)
                    print(job)
                    jobs.append(job)
    return jobs

if __name__ == "__main__":
    threadNumber = int(input("Enter the number of threades to be used: "))

    mp.freeze_support()
    pool = mp.Pool(threadNumber)
    
    poolJobs = []

    choice = input("Enter A to calculate <A> or S to calculate sign: ")
    if choice.upper() == 'A':
        jobs = generateExpectationValueJobs()

        pool.map(ExpectationValueCalculator.multithreadRun, jobs)

    elif choice.upper() == 'S':
        jobs = generateSingJobs()

        pool.map(SignCalculator.multithreadRun, jobs) 

    else:
        print("Invalid input!")
        exit()
    
    finishTime = time.time()
    print("Total time: ", finishTime - startTime)