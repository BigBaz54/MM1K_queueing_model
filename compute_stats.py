import time

import numpy as np
import queue_model
import mpi4py.MPI as MPI


# parallel version
t = MPI.Wtime()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

LAMBDA = 300-50*2 # 200
MU = 1/(2*2/1000) # 250

qm = queue_model.queue_model(LAMBDA, MU, 2, 5)
qm.run_simulation()

if rank == 0:
    requests_arrived = [qm.get_number_of_requests_arrived()]
    requests_processed = [qm.get_number_of_requests_processed()]
    requests_lost = [qm.get_number_of_requests_lost()]
    output_rate = [qm.get_output_rate()]
    loss_rate = [qm.get_loss_rate()]
    average_service_time = [qm.get_average_service_time()]
    average_treatment_time = [qm.get_average_treatment_time()]
    average_waiting_time = [qm.get_average_waiting_time()]
    average_number_of_requests_in_system = [qm.get_average_number_of_requests_in_system()]
    occupancy_rate = [qm.get_occupancy_rate()]
    for i in range(1, size):
        requests_arrived.append(comm.recv(source=i, tag=11))
        requests_processed.append(comm.recv(source=i, tag=12))
        requests_lost.append(comm.recv(source=i, tag=13))
        output_rate.append(comm.recv(source=i, tag=14))
        loss_rate.append(comm.recv(source=i, tag=15))
        average_service_time.append(comm.recv(source=i, tag=16))
        average_treatment_time.append(comm.recv(source=i, tag=17))
        average_waiting_time.append(comm.recv(source=i, tag=18))
        average_number_of_requests_in_system.append(comm.recv(source=i, tag=19))
        occupancy_rate.append(comm.recv(source=i, tag=20))
    print("Parallel version\n")
    print("Requests arrived:", np.mean(requests_arrived))
    print("Requests processed:", np.mean(requests_processed))
    print("Requests lost:", np.mean(requests_lost))
    print("Output rate:", np.mean(output_rate))
    print("Loss rate:", np.mean(loss_rate))
    print("Average service time:", np.mean(average_service_time))
    print("Average treatment time:", np.mean(average_treatment_time))
    print("Average waiting time:", np.mean(average_waiting_time))
    print("Average number of requests in system:", np.mean(average_number_of_requests_in_system))
    print("Occupancy rate:", np.mean(occupancy_rate))
    print("\nTime elapsed:", MPI.Wtime()-t)
else:
    comm.send(qm.get_number_of_requests_arrived(), dest=0, tag=11)
    comm.send(qm.get_number_of_requests_processed(), dest=0, tag=12)
    comm.send(qm.get_number_of_requests_lost(), dest=0, tag=13)
    comm.send(qm.get_output_rate(), dest=0, tag=14)
    comm.send(qm.get_loss_rate(), dest=0, tag=15)
    comm.send(qm.get_average_service_time(), dest=0, tag=16)
    comm.send(qm.get_average_treatment_time(), dest=0, tag=17)
    comm.send(qm.get_average_waiting_time(), dest=0, tag=18)
    comm.send(qm.get_average_number_of_requests_in_system(), dest=0, tag=19)
    comm.send(qm.get_occupancy_rate(), dest=0, tag=20)

# # sequential version
# t = MPI.Wtime()
# LAMBDA = 300-50*2 # 200
# MU = 1/(2*2/1000) # 250

# if rank == 0:
#     print("\n\n\n")
#     requests_arrived = []
#     requests_processed = []
#     requests_lost = []
#     output_rate = []
#     loss_rate = []
#     average_service_time = []
#     average_treatment_time = []
#     average_waiting_time = []
#     average_number_of_requests_in_system = []
#     occupancy_rate = []

#     for i in range(size):
#         qm = queue_model.queue_model(LAMBDA, MU, 2, 5)
#         qm.run_simulation()
#         requests_arrived.append(qm.get_number_of_requests_arrived())
#         requests_processed.append(qm.get_number_of_requests_processed())
#         requests_lost.append(qm.get_number_of_requests_lost())
#         output_rate.append(qm.get_output_rate())
#         loss_rate.append(qm.get_loss_rate())
#         average_service_time.append(qm.get_average_service_time())
#         average_treatment_time.append(qm.get_average_treatment_time())
#         average_waiting_time.append(qm.get_average_waiting_time())
#         average_number_of_requests_in_system.append(qm.get_average_number_of_requests_in_system())
#         occupancy_rate.append(qm.get_occupancy_rate())
#     print("Sequential version\n")
#     print("Requests arrived:", np.mean(requests_arrived))
#     print("Requests processed:", np.mean(requests_processed))
#     print("Requests lost:", np.mean(requests_lost))
#     print("Output rate:", np.mean(output_rate))
#     print("Loss rate:", np.mean(loss_rate))
#     print("Average service time:", np.mean(average_service_time))
#     print("Average treatment time:", np.mean(average_treatment_time))
#     print("Average waiting time:", np.mean(average_waiting_time))
#     print("Average number of requests in system:", np.mean(average_number_of_requests_in_system))
#     print("Occupancy rate:", np.mean(occupancy_rate))
#     print("\nTime elapsed:", MPI.Wtime()-t)


