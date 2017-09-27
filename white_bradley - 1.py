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


class Processor:
    def __init__(self, id):
        self.id = id


# Simpy example follows
class Car(object):
    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.charge(charge_duration))
            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)


class Job_scheduler:
    def __init__(self, env, num_processors):
        self.env = env
        self.processor = simpy.Resource(env, num_processors)

    def run_job(self, time):
        yield self.env.timeout(time)

def job(env, job, job_scheduler, job_num):
    with job_scheduler.processor.request() as request:
        yield request
        print("Starting job #{0}".format(job_num))
        yield env.process(job_scheduler.run_job(job[1]))

def setup_sim(env, num_processors):
    global jobs

    job_scheduler = Job_scheduler(env, num_processors)

    for i in range(len(jobs)):
        env.process(job(env, jobs[i], job_scheduler, i))

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
    env.run
    '''car = Car(env)
    env.run(until=15)
    car2 = Car(env)
    env.run(until=30)'''
    #create_random_jobs()
    #print(random_jobs[1], random_jobs[2])

main()
