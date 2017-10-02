'''
Bradley White
Programming 1: Multi-Processor Management
CSCI-460: Operating Systems
October 2, 2017
'''

# Interpreter: Python 3.5.1
# k = 1876 % 3 + 2 = 3 processors

import statistics
import random

jobs = [(4, 9), (15, 2), (18, 16), (20, 3), (26, 29), (29, 198), (35, 7), (45, 170), (57, 180), (83, 178), (88, 73),
        (95, 8)]
loading_time = 1

def create_random_jobs():
    random_jobs = []

    for i in range(1000):
        random_jobs.append((i, random.randint(1, 500)))

    return random_jobs


def circular_queue(k, jobs):
    global loading_time

    current_time = jobs[0][0]
    start_time = jobs[0][0]

    processor_busy = [False] * k
    processor_job_end_time = [0] * k
    i = 0

    for job in jobs:
        index = i % k

        if processor_busy[index] is False or (
                processor_busy[index] is True and processor_job_end_time[index] <= current_time):
            current_time = job[0]
            processor_busy[index] = True
            processor_job_end_time[index] = job[1] + current_time + loading_time
        elif processor_busy[index] is True and processor_job_end_time[index] > current_time:
            current_time = processor_job_end_time[index]
            processor_job_end_time[index] = job[1] + current_time + loading_time

        i += 1

    return max(processor_job_end_time) - start_time


def main():
    global jobs

    k = 3
    output_file = open("output.txt", "w")
    output_file.write("Overall turnaround time for 12 job sequence:\n")
    output_file.write("\t Circular Queue: {0}ms".format(str(circular_queue(k, jobs))))

    '''env = simpy.Environment()
    env.process(setup_sim(env, k))
    env.run()
    car = Car(env)
    env.run(until=15)
    car2 = Car(env)
    env.run(until=30)'''
    # create_random_jobs()
    # print(random_jobs[1], random_jobs[2])

    output_file.close()

main()
