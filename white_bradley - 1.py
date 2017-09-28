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
random_jobs = []


class Job_scheduler(object):
    def __init__(self, env, num_processors):
        self.env = env
        self.processor = simpy.Resource(env, num_processors)

    def run_job(self, name, time):
        print("Running job {0} with runtime {1}".format(name, time))
        yield self.env.timeout(time)


def job(env, job_name, job_time, job_scheduler):
    with job_scheduler.processor.request() as request:
        yield request
        # print("Starting job #{0}".format(job_num))
        yield env.process(job_scheduler.run_job(job_name, job_time))


def setup_sim(env, num_processors):
    global jobs

    job_scheduler = Job_scheduler(env, num_processors)

    for i in range(len(jobs)):
        yield env.timeout(1)
        env.process(job(env, 'job %d' % (i + 1), jobs[i][1], job_scheduler))

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
    global random_jobs

    for i in range(1000):
        random_jobs.append((i, random.randint(1, 500)))


def main():
    global jobs
    global random_jobs

    k = 3

    env = simpy.Environment()
    env.process(setup_sim(env, k))
    env.run()
    '''car = Car(env)
    env.run(until=15)
    car2 = Car(env)
    env.run(until=30)'''
    # create_random_jobs()
    # print(random_jobs[1], random_jobs[2])


main()
