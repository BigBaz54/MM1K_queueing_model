import numpy as np
import queue_model
import mpi4py.MPI as MPI

LAMBDA = 300-50*2 # 200
MU = 1/(2*2/1000) # 250

# parallel version
def parallel(lam, mu, observation_time):
    t = MPI.Wtime()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    qm = queue_model.queue_model(lam, mu, observation_time)
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
            occupancy_rate.append(comm.recv(source=i, tag=25))
        print('Number of simulations:', size, '\n')
        print('LAMBDA:', lam)
        print('MU:', mu, '\n')

        print('== Parallel version ==\n')
        print(f'{"Requests arrived:":>40}', f'mean: {np.mean(requests_arrived):<25}', '|', f'std: {np.std(requests_arrived):<25}', '|', f'CI95: [{np.mean(requests_arrived)-1.96*np.std(requests_arrived)/np.sqrt(size)}; {np.mean(requests_arrived)+1.96*np.std(requests_arrived)/np.sqrt(size)}]')
        print(f'{"Requests processed:":>40}', f'mean: {np.mean(requests_processed):<25}', '|', f'std: {np.std(requests_processed):<25}', '|', f'CI95: [{np.mean(requests_processed)-1.96*np.std(requests_processed)/np.sqrt(size)}; {np.mean(requests_processed)+1.96*np.std(requests_processed)/np.sqrt(size)}]')
        print(f'{"Requests lost:":>40}', f'mean: {np.mean(requests_lost):<25}', '|', f'std: {np.std(requests_lost):<25}', '|', f'CI95: [{np.mean(requests_lost)-1.96*np.std(requests_lost)/np.sqrt(size)}; {np.mean(requests_lost)+1.96*np.std(requests_lost)/np.sqrt(size)}]')
        print(f'{"Output rate:":>40}', f'mean: {np.mean(output_rate):<25}', '|', f'std: {np.std(output_rate):<25}', '|', f'CI95: [{np.mean(output_rate)-1.96*np.std(output_rate)/np.sqrt(size)}; {np.mean(output_rate)+1.96*np.std(output_rate)/np.sqrt(size)}]')
        print(f'{"Loss rate:":>40}', f'mean: {np.mean(loss_rate):<25}', '|', f'std: {np.std(loss_rate):<25}', '|', f'CI95: [{np.mean(loss_rate)-1.96*np.std(loss_rate)/np.sqrt(size)}; {np.mean(loss_rate)+1.96*np.std(loss_rate)/np.sqrt(size)}]')
        print(f'{"Average service time:":>40}', f'mean: {np.mean(average_service_time):<25}', '|', f'std: {np.std(average_service_time):<25}', '|', f'CI95: [{np.mean(average_service_time)-1.96*np.std(average_service_time)/np.sqrt(size)}; {np.mean(average_service_time)+1.96*np.std(average_service_time)/np.sqrt(size)}]')
        print(f'{"Average treatment time:":>40}', f'mean: {np.mean(average_treatment_time):<25}', '|', f'std: {np.std(average_treatment_time):<25}', '|', f'CI95: [{np.mean(average_treatment_time)-1.96*np.std(average_treatment_time)/np.sqrt(size)}; {np.mean(average_treatment_time)+1.96*np.std(average_treatment_time)/np.sqrt(size)}]')
        print(f'{"Average waiting time:":>40}', f'mean: {np.mean(average_waiting_time):<25}', '|', f'std: {np.std(average_waiting_time):<25}', '|', f'CI95: [{np.mean(average_waiting_time)-1.96*np.std(average_waiting_time)/np.sqrt(size)}; {np.mean(average_waiting_time)+1.96*np.std(average_waiting_time)/np.sqrt(size)}]')
        print(f'{"Average number of requests in system:":>40}', f'mean: {np.mean(average_number_of_requests_in_system):<25}', '|', f'std: {np.std(average_number_of_requests_in_system):<25}', '|', f'CI95: [{np.mean(average_number_of_requests_in_system)-1.96*np.std(average_number_of_requests_in_system)/np.sqrt(size)}; {np.mean(average_number_of_requests_in_system)+1.96*np.std(average_number_of_requests_in_system)/np.sqrt(size)}]')
        print(f'{"Occupancy rate:":>40}', f'mean: {np.mean(occupancy_rate):<25}', '|', f'std: {np.std(occupancy_rate):<25}', '|', f'CI95: [{np.mean(occupancy_rate)-1.96*np.std(occupancy_rate)/np.sqrt(size)}; {np.mean(occupancy_rate)+1.96*np.std(occupancy_rate)/np.sqrt(size)}]')
        print('\nTime elapsed:', MPI.Wtime()-t)
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
        comm.send(qm.get_occupancy_rate(), dest=0, tag=25)

parallel(LAMBDA, MU, 1)

# sequential version
def sequential(lam, mu, observation_time):
    t = MPI.Wtime()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        print('\n\n\n')
        requests_arrived = []
        requests_processed = []
        requests_lost = []
        output_rate = []
        loss_rate = []
        average_service_time = []
        average_treatment_time = []
        average_waiting_time = []
        average_number_of_requests_in_system = []
        occupancy_rate = []

        for _ in range(size):
            qm = queue_model.queue_model(LAMBDA, MU, observation_time)
            qm.run_simulation()
            requests_arrived.append(qm.get_number_of_requests_arrived())
            requests_processed.append(qm.get_number_of_requests_processed())
            requests_lost.append(qm.get_number_of_requests_lost())
            output_rate.append(qm.get_output_rate())
            loss_rate.append(qm.get_loss_rate())
            average_service_time.append(qm.get_average_service_time())
            average_treatment_time.append(qm.get_average_treatment_time())
            average_waiting_time.append(qm.get_average_waiting_time())
            average_number_of_requests_in_system.append(qm.get_average_number_of_requests_in_system())
            occupancy_rate.append(qm.get_occupancy_rate())
        
        print('Number of simulations:', size, '\n')
        print('LAMBDA:', lam)
        print('MU:', mu, '\n')

        print('== Sequential version ==\n')
        print(f'{"Requests arrived:":>40}', f'mean: {np.mean(requests_arrived):<25}', '|', f'std: {np.std(requests_arrived):<25}', '|', f'CI95: [{np.mean(requests_arrived)-1.96*np.std(requests_arrived)/np.sqrt(size)}; {np.mean(requests_arrived)+1.96*np.std(requests_arrived)/np.sqrt(size)}]')
        print(f'{"Requests processed:":>40}', f'mean: {np.mean(requests_processed):<25}', '|', f'std: {np.std(requests_processed):<25}', '|', f'CI95: [{np.mean(requests_processed)-1.96*np.std(requests_processed)/np.sqrt(size)}; {np.mean(requests_processed)+1.96*np.std(requests_processed)/np.sqrt(size)}]')
        print(f'{"Requests lost:":>40}', f'mean: {np.mean(requests_lost):<25}', '|', f'std: {np.std(requests_lost):<25}', '|', f'CI95: [{np.mean(requests_lost)-1.96*np.std(requests_lost)/np.sqrt(size)}; {np.mean(requests_lost)+1.96*np.std(requests_lost)/np.sqrt(size)}]')
        print(f'{"Output rate:":>40}', f'mean: {np.mean(output_rate):<25}', '|', f'std: {np.std(output_rate):<25}', '|', f'CI95: [{np.mean(output_rate)-1.96*np.std(output_rate)/np.sqrt(size)}; {np.mean(output_rate)+1.96*np.std(output_rate)/np.sqrt(size)}]')
        print(f'{"Loss rate:":>40}', f'mean: {np.mean(loss_rate):<25}', '|', f'std: {np.std(loss_rate):<25}', '|', f'CI95: [{np.mean(loss_rate)-1.96*np.std(loss_rate)/np.sqrt(size)}; {np.mean(loss_rate)+1.96*np.std(loss_rate)/np.sqrt(size)}]')
        print(f'{"Average service time:":>40}', f'mean: {np.mean(average_service_time):<25}', '|', f'std: {np.std(average_service_time):<25}', '|', f'CI95: [{np.mean(average_service_time)-1.96*np.std(average_service_time)/np.sqrt(size)}; {np.mean(average_service_time)+1.96*np.std(average_service_time)/np.sqrt(size)}]')
        print(f'{"Average treatment time:":>40}', f'mean: {np.mean(average_treatment_time):<25}', '|', f'std: {np.std(average_treatment_time):<25}', '|', f'CI95: [{np.mean(average_treatment_time)-1.96*np.std(average_treatment_time)/np.sqrt(size)}; {np.mean(average_treatment_time)+1.96*np.std(average_treatment_time)/np.sqrt(size)}]')
        print(f'{"Average waiting time:":>40}', f'mean: {np.mean(average_waiting_time):<25}', '|', f'std: {np.std(average_waiting_time):<25}', '|', f'CI95: [{np.mean(average_waiting_time)-1.96*np.std(average_waiting_time)/np.sqrt(size)}; {np.mean(average_waiting_time)+1.96*np.std(average_waiting_time)/np.sqrt(size)}]')
        print(f'{"Average number of requests in system:":>40}', f'mean: {np.mean(average_number_of_requests_in_system):<25}', '|', f'std: {np.std(average_number_of_requests_in_system):<25}', '|', f'CI95: [{np.mean(average_number_of_requests_in_system)-1.96*np.std(average_number_of_requests_in_system)/np.sqrt(size)}; {np.mean(average_number_of_requests_in_system)+1.96*np.std(average_number_of_requests_in_system)/np.sqrt(size)}]')
        print(f'{"Occupancy rate:":>40}', f'mean: {np.mean(occupancy_rate):<25}', '|', f'std: {np.std(occupancy_rate):<25}', '|', f'CI95: [{np.mean(occupancy_rate)-1.96*np.std(occupancy_rate)/np.sqrt(size)}; {np.mean(occupancy_rate)+1.96*np.std(occupancy_rate)/np.sqrt(size)}]')
        print('\nTime elapsed:', MPI.Wtime()-t)

sequential(LAMBDA, MU, 1)


