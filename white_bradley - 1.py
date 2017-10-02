'''
Bradley White
Programming 1: Multi-Processor Management
CSCI-460: Operating Systems
October 2, 2017
'''

# Interpreter: Python 3.5.1
# Using k = 1876 % 3 + 2 = 3 processors
# Inputs: None
# Outputs to output.txt in the same directory, there is no console output

import statistics
import random
import math

# A job is a tuple of the form (arrival time, processing time)
# @param jobs: Predefined list of 12 jobs from assignment
# @param loading_time: The time take to load a job onto a processor
jobs = [(4, 9), (15, 2), (18, 16), (20, 3), (26, 29), (29, 198), (35, 7), (45, 170), (57, 180), (83, 178), (88, 73),
        (95, 8)]
loading_time = 1


# Creates a list of 1000 jobs that arrive every millisecond and can have between 1 and 500ms processing time, inclusive
def create_random_jobs():
    random_jobs = []

    for i in range(1000):
        random_jobs.append((i, random.randint(1, 500)))

    return random_jobs


# Simulate a circular queue where each job is placed on the processors in order, regardless of the previous jobs
# completion time
def circular_queue(k, jobs):
    global loading_time

    # Record the starting time and keep track of the starting time of the simulation
    current_time = jobs[0][0]
    start_time = jobs[0][0]

    # Keep track of the status of each processor and the time which the current job completes
    processor_busy = [False] * k
    processor_job_end_time = [0] * k
    i = 0

    # Iterate through all jobs
    for job in jobs:
        # Map to the correct index
        index = i % k

        # If the processor is available, or the job has completed but values haven't been updated, load the next job
        if processor_busy[index] is False or (
                        processor_busy[index] is True and processor_job_end_time[index] <= current_time):
            current_time = job[0]
            processor_busy[index] = True
            processor_job_end_time[index] = job[1] + current_time + loading_time
        # Otherwise we "wait" for the current job to finish then load the newest job
        elif processor_busy[index] is True and processor_job_end_time[index] > current_time:
            current_time = processor_job_end_time[index]
            processor_job_end_time[index] = job[1] + current_time + loading_time

        # Move to next processor
        i += 1

    # The max will be the job which is finishing last,
    # thus the overall turnaround time is that time minus the start time
    return max(processor_job_end_time) - start_time


def next_available(k, jobs):
    global loading_time

    # Record the starting time and keep track of the starting time of the simulation
    current_time = jobs[0][0]
    start_time = jobs[0][0]

    # Keep track of the status of each processor and the time which the current job completes
    processor_busy = [False] * k
    processor_job_end_time = [0] * k

    # Iterate through all jobs
    for job in jobs:
        # Find the job which completes next or has already completed,
        # Using infinity guarantees we always find an index
        min_time = math.inf
        min_index = None
        for i in range(len(processor_job_end_time)):
            if processor_job_end_time[i] < min_time:
                min_time = processor_job_end_time[i]
                min_index = i

        # Update the values
        # If the current time is lower than the minimum job completion time, jump ahead to that point
        if current_time < processor_job_end_time[min_index]:
            current_time = processor_job_end_time[min_index]
        # Otherwise set the current time to the arrival time of the current job
        else:
            current_time = job[0]
        # Update the ending time for the new job
        processor_job_end_time[min_index] = job[1] + current_time + loading_time

    # The max will be the job which is finishing last,
    # thus the overall turnaround time is that time minus the start time
    return max(processor_job_end_time) - start_time


def main():
    global jobs
    k = 3

    # Open a txt file to record outputs
    output_file = open("output.txt", "w")

    # Test each method with the 12 job sequence
    output_file.write("Overall turnaround time for 12 job sequence:\n")
    output_file.write("\t Circular Queue: {0}ms\n".format(str(circular_queue(k, jobs))))
    output_file.write("\t Next Available Processor: {0}ms\n".format(str(next_available(k, jobs))))

    circular_vector = []
    available_vector = []

    # Test each method with 1000 randomly generated jobs, 100 times and record statistics
    for i in range(100):
        jobs = create_random_jobs()
        circular_vector.append(circular_queue(k, jobs))
        available_vector.append(next_available(k, jobs))

    # Generate statistics and write to an output file
    output_file.write("\n1000 random jobs, repeated 100 times:\n")
    output_file.write("Circular Queue:\n")
    output_file.write("\tMinimum: {0}ms\n".format(min(circular_vector)))
    output_file.write("\tMaximum: {0}ms\n".format(max(circular_vector)))
    mean = statistics.mean(circular_vector)
    output_file.write("\tAverage: {0:.2f}ms\n".format(mean))
    output_file.write("\tStandard Deviation: {0:.2f}ms\n".format(statistics.stdev(circular_vector, xbar=mean)))

    output_file.write("\nNext Available Processor:\n")
    output_file.write("\tMinimum: {0}ms\n".format(min(available_vector)))
    output_file.write("\tMaximum: {0}ms\n".format(max(available_vector)))
    mean = statistics.mean(available_vector)
    output_file.write("\tAverage: {0:.2f}ms\n".format(mean))
    output_file.write("\tStandard Deviation: {0:.2f}ms\n".format(statistics.stdev(available_vector, xbar=mean)))

    # Clean up
    output_file.close()


main()
