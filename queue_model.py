import random
import numpy as np
import matplotlib.pyplot as plt

from random_var_exp import random_var_exp


class queue_model():
    def __init__(self, arrival_rate, service_rate, observation_time, buffer_size=np.inf):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.observation_time = observation_time
        self.buffer_size = buffer_size
        self.arrival_times = []
        self.departure_times = []

    def get_requests_in_buffer(self, t):
        return len([x for x in self.departure_times if (x > t)])
        

    def run_simulation(self):
        # Initialize
        last_arrival = 0
        last_departure = 0
        self.arrival_times = []
        self.departure_times = []
        arrival_times = self.arrival_times
        departure_times = self.departure_times
        
        # Run simulation
        while last_arrival < self.observation_time:
            last_arrival += random_var_exp(self.arrival_rate)
            arrival_times.append(last_arrival)
            nb_requests_in_buffer = self.get_requests_in_buffer(last_arrival)
            if nb_requests_in_buffer >= self.buffer_size:
                # request is lost
                departure_times.append(-1)
            else:
                # request is processed
                if nb_requests_in_buffer == 0:
                    # no requests in buffer, the current request will be processed immediately
                    last_departure = last_arrival + random_var_exp(self.service_rate)
                else:
                    # requests in buffer, the current request will be processed after the last one
                    last_departure = last_departure + random_var_exp(self.service_rate)
                departure_times.append(last_departure)

    def plot_simulation(self):
        processed_arrivals = []
        processed_departures = []
        time = np.linspace(0, self.departure_times[-1], 10000)
        # number of requests arrived at every time t
        processed_arrivals = [len([x for x in self.arrival_times if x <= t]) for t in time]
        # number of requests processed at every time t
        processed_departures = [len([x for x in self.departure_times if (x <= t and x!=-1)]) for t in time]
        plt.plot(processed_arrivals)
        plt.plot(processed_departures)
        plt.show()

    def plot_raw_simulation(self):
        time = np.linspace(0, self.departure_times[-1], len(self.departure_times))
        plt.plot(time, self.arrival_times)
        plt.plot(time, self.departure_times)
        plt.show()

    def print_statistics(self):
        print("Numer of requests arrived: ", len(self.arrival_times))
        print("Numer of requests processed: ", len([x for x in self.departure_times if x!=-1]))
        print("Numer of requests lost: ", len([x for x in self.departure_times if x==-1]))        

if __name__ == "__main__":
    LAMBDA = 300-50*2 # 200
    MU = 1/(2*2/1000) # 250
    
    qm = queue_model(LAMBDA, MU, 1, 10)
    qm.run_simulation()
    qm.plot_simulation()
    qm.print_statistics()

    # plot loss rate as a function of the buffer size
    loss_rates = []
    for buffer_size in range(1, 10+2*2):
        qm = queue_model(LAMBDA, MU, 10, buffer_size)
        qm.run_simulation()
        loss_rates.append(len([x for x in qm.departure_times if x==-1])/len(qm.departure_times))
    plt.plot(range(1, 10+2*2), loss_rates)
    plt.show()
        