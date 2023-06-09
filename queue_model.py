import time
import numpy as np
import matplotlib.pyplot as plt

from random_var_exp import random_var_exp


class queue_model():
    def __init__(self, arrival_rate, service_rate, observation_time, buffer_size=np.inf):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.observation_time = observation_time
        self.buffer_size = buffer_size
        self.max_requests_in_system = 0
        self.arrival_times = []
        self.departure_times = []
        self.treatment_times = []
        self.service_times = []
        self.waiting_times = []

    def get_requests_in_system(self, t):
        count = 0
        for i in range(len(self.departure_times)):
            if self.arrival_times[i] <= t and (self.departure_times[i] > t):
                count += 1
        return count
    
    def get_requests_in_buffer(self, t):
        return self.get_requests_in_system(t) - 1 if self.get_requests_in_system(t) > 0 else 0
        
    def get_time_spent_with_n_requests_in_system(self):
        # initialize
        total_time = {i:0 for i in range(self.max_requests_in_system+2)}
        processed_arrivals = []
        processed_departures = []
        for i in range(len(self.arrival_times)):
            if self.departure_times[i] != -1:
                # request is processed
                processed_arrivals.append(self.arrival_times[i])
                processed_departures.append(self.departure_times[i])
        
        if len(processed_arrivals) == 0:
            return total_time
        
        # first interval
        total_time[0] = processed_arrivals[0]
        
        # intermediate intervals
        requests_in_system = 0
        for i in range(len(processed_arrivals)-1):
            requests_in_system += 1
            time_between_arrivals = processed_arrivals[i+1] - processed_arrivals[i]
            requests_processed_in_interval = [x for x in processed_departures if (x >= processed_arrivals[i] and x < processed_arrivals[i+1])]
            if len(requests_processed_in_interval) == 0:
                total_time[requests_in_system] += time_between_arrivals
            else:
                for j in range(len(requests_processed_in_interval)):
                    if j == 0:
                        total_time[requests_in_system] += requests_processed_in_interval[0] - processed_arrivals[i]
                    else:
                        total_time[requests_in_system] += requests_processed_in_interval[j] - requests_processed_in_interval[j-1]
                    requests_in_system -= 1
                total_time[requests_in_system] += processed_arrivals[i+1] - requests_processed_in_interval[-1]
        
        # last interval
        requests_in_system += 1
        total_time[requests_in_system] += self.departure_times[-1] - processed_arrivals[-1]
        
        return total_time

    def run_simulation(self):
        # Initialize
        last_arrival = 0
        last_departure = 0
        self.arrival_times = []
        self.departure_times = []
        arrival_times = self.arrival_times
        departure_times = self.departure_times
        treatment_times = self.treatment_times
        service_times = self.service_times
        waiting_times = self.waiting_times
        
        # Run simulation
        while last_arrival < self.observation_time:
            last_arrival += random_var_exp(self.arrival_rate)
            arrival_times.append(last_arrival)
            nb_requests_in_buffer = self.get_requests_in_buffer(last_arrival)
            nb_requests_in_system = self.get_requests_in_system(last_arrival)
            if nb_requests_in_system > self.max_requests_in_system:
                self.max_requests_in_system = nb_requests_in_system
            if nb_requests_in_buffer >= self.buffer_size:
                # request is lost
                departure_times.append(-1)
                treatment_times.append(-1)
                service_times.append(-1)
                waiting_times.append(-1)
            else:
                # request is processed
                treatment_time = random_var_exp(self.service_rate)
                if nb_requests_in_system == 0:
                    # no requests in system, the current request will be processed immediately
                    last_departure = last_arrival + treatment_time
                else:
                    # requests in system, the current request will be processed after the last one
                    last_departure = last_departure + treatment_time
                departure_times.append(last_departure)
                treatment_times.append(treatment_time)
                service_times.append(last_departure - last_arrival)
                waiting_times.append(last_departure - last_arrival - treatment_time if last_departure - last_arrival - treatment_time >= 0 else 0)


    def plot_simulation(self):
        processed_arrivals = []
        processed_departures = []
        time = np.linspace(0, self.observation_time, 10000)
        # number of requests arrived at every time t
        processed_arrivals = [len([x for x in self.arrival_times if x <= t]) for t in time]
        # number of requests processed at every time t
        processed_departures = [len([x for x in self.departure_times if (x <= t and x!=-1)]) for t in time]
        plt.plot(processed_arrivals)
        plt.plot(processed_departures)
        plt.show()

    def plot_raw_simulation(self):
        time = np.linspace(0, self.observation_time, len(self.departure_times))
        plt.plot(time, self.arrival_times)
        plt.plot(time, self.departure_times)
        plt.show()

    def get_number_of_requests_arrived(self):
        return len(self.arrival_times)
    
    def get_number_of_requests_processed(self):
        return len([x for x in self.departure_times if x!=-1 and x<=self.observation_time])
    
    def get_number_of_requests_lost(self):
        return self.get_number_of_requests_arrived() - self.get_number_of_requests_processed()
    
    def get_output_rate(self):
        return self.get_number_of_requests_processed()/self.observation_time
    
    def get_loss_rate(self):
        return self.get_number_of_requests_lost()/len(self.departure_times)
    
    def get_average_service_time(self):
        return np.mean([x for x in self.service_times if x!=-1])
    
    def get_average_treatment_time(self):
        return np.mean([x for x in self.treatment_times if x!=-1])
    
    def get_average_waiting_time(self):
        return np.mean([x for x in self.waiting_times if x!=-1])
    
    def get_average_number_of_requests_in_system(self):
        return sum([i*self.get_time_spent_with_n_requests_in_system()[i] for i in range(self.max_requests_in_system+1)])/(self.observation_time)
    
    def get_average_number_of_requests_in_system_approx(self, nb_points=1000):
        time_points = np.linspace(0, self.observation_time, nb_points)
        return sum([self.get_requests_in_system(t) for t in time_points])/nb_points
    
    def get_occupancy_rate(self):
        return sum([self.get_time_spent_with_n_requests_in_system()[i] for i in range(1, self.max_requests_in_system+1)])/(self.observation_time)

    def print_statistics(self):
        print("Number of requests arrived:", self.get_number_of_requests_arrived())
        print("Number of requests processed:", self.get_number_of_requests_processed())
        print("Number of requests lost:", self.get_number_of_requests_lost())
        print("Maximum number of requests in system:", self.max_requests_in_system)
        print("Output rate:", round(self.get_output_rate(), 2), "requests per time unit")
        print("Loss rate:", round(self.get_loss_rate()*100, 2), "%")
        print("Average service time:", round(self.get_average_service_time(), 2), "time units")
        print("Average treatment time:", round(self.get_average_treatment_time(), 2), "time units")
        print("Average waiting time:", round(self.get_average_waiting_time(), 2), "time units")
        t = time.time()
        print("Average number of requests in system:", round(self.get_average_number_of_requests_in_system(), 2), "requests")
        print("Time spent computing average number of requests in system:", time.time()-t, "seconds")
        t = time.time()
        print("Average number of requests in system (approximation):", round(self.get_average_number_of_requests_in_system_approx(100), 2), "requests")
        print("Time spent computing average number of requests in system (approximation):", time.time()-t, "seconds")
        print("Occupancy rate:", round(self.get_occupancy_rate()*100, 2), "%")	

if __name__ == "__main__":
    LAMBDA = 300-50*2 # 200
    MU = 1/(2*2/1000) # 250
    
    qm = queue_model(LAMBDA, MU, 10)
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
    