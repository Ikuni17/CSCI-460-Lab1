'''
Bradley White
Programming 1: Multi-Processor Management
CSCI-460: Operating Systems
September 26, 2017
'''

# Interpreter: Python 3.5.1
# k = 1876 % 3 + 2 = 3 processors

# $pip install simpy
import simpy
import statistics
import random

jobs = [(4, 9), (15, 2), (18, 16), (20, 3), (26, 29), (29, 198), (35, 7), (45, 170), (57, 180), (83, 178), (88, 73),
        (95, 8)]
loading_time = 1


class Job_scheduler(object):
    def __init__(self, env, num_processors):
        self.env = env
        self.processor = simpy.Resource(env, num_processors)

    def run_job(self, name, time):
        print("Running {0} with runtime {1} at {2}".format(name, time, self.env.now))
        print('%d of %d slots are allocated.' % (self.processor.count, self.processor.capacity))
        yield self.env.timeout(time)
        print("\tFinished {0} at {1}".format(name, self.env.now))


def create_job(env, job_name, job_time, job_scheduler):
    with job_scheduler.processor.request() as request:
        yield request
        yield env.timeout(1)
        # print("Starting job #{0}".format(job_num))
        yield env.process(job_scheduler.run_job(job_name, job_time))


def setup_sim(env, num_processors):
    global jobs

    job_scheduler = Job_scheduler(env, num_processors)

    for i in range(len(jobs)):
        yield env.timeout(jobs[i][0] - env.now)
        env.process(create_job(env, 'job %d' % (i + 1), jobs[i][1], job_scheduler))

    '''i = 1
    while True:
        yield env.timeout(1)
        i+=1
        env.process(job1(env, 'job %d' % i, 1, job_scheduler))'''


def job_gen():
    global jobs

    for job in jobs:
        yield job


def create_random_jobs():
    random_jobs = []

    for i in range(1000):
        random_jobs.append((i, random.randint(1, 500)))

    return random_jobs


def main():
    global jobs

    k = 3


    env = simpy.Environment()
    env.process(setup_sim(env, k))
    env.run()

main()
