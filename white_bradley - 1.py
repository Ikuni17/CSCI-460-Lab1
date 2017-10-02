'''
Bradley White
Programming 1: Multi-Processor Management
CSCI-460: Operating Systems
October 2, 2017
'''

# Interpreter: Python 3.5.1
# Using k = 1876 % 3 + 2 = 3 processors

import statistics
import random

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


def main():
    global jobs
    k = 3

    # Open a txt file to record outputs
    output_file = open("output.txt", "w")

    # Test each method with the 12 job sequence
    output_file.write("Overall turnaround time for 12 job sequence:\n")
    output_file.write("\t Circular Queue: {0}ms".format(str(circular_queue(k, jobs))))

    # Test each method with 1000 randomly generated jobs, 100 times and record statistics

    # Clean up
    output_file.close()

main()
