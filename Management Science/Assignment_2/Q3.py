import numpy as np

def simulate_queue(num_customers=500,
                   arrival_rate_per_hour=10.0,
                   service_time_mean=5.0,
                   service_time_type='exponential',
                   server_cost_per_hour=20.0,
                   waiting_cost_per_hour=2.0,
                   random_seed=0):
    """
    Simulates a single-server queue with Poisson arrivals and either
    exponential or deterministic service times.
    
    Parameters:
      num_customers        : Number of customers to process.
      arrival_rate_per_hour: Poisson arrival rate (customers/hour).
      service_time_mean    : Mean (or exact) service time in minutes.
      service_time_type    : 'exponential' or 'deterministic'.
      server_cost_per_hour : Hourly server/registrar cost.
      waiting_cost_per_hour: Cost per hour per customer waiting.
      random_seed          : Seed for reproducibility.

    Returns:
      total_hourly_cost : Server cost + waiting cost (per hour).
      avg_waiting_time  : Mean waiting time in minutes.
      avg_queue_length  : Mean number of customers in queue.
    """
    np.random.seed(random_seed)
    
    # Convert arrival rate (per hour) to mean interarrival time in minutes
    mean_interarrival = 60.0 / arrival_rate_per_hour
    
    # Generate interarrival times and cumulative arrival times
    inter_arrivals = np.random.exponential(mean_interarrival, size=num_customers)
    arrival_times  = np.cumsum(inter_arrivals)
    
    # Generate service times (exponential or deterministic)
    if service_time_type == 'exponential':
        service_times = np.random.exponential(service_time_mean, size=num_customers)
    else:
        service_times = np.full(num_customers, service_time_mean)
    
    # Track start and completion times for each customer
    start_service_times = np.zeros(num_customers)
    completion_times    = np.zeros(num_customers)
    waiting_times       = np.zeros(num_customers)
    
    for i in range(num_customers):
        if i == 0:
            start_service_times[i] = arrival_times[i]
        else:
            start_service_times[i] = max(arrival_times[i], completion_times[i - 1])
        completion_times[i] = start_service_times[i] + service_times[i]
        waiting_times[i]    = start_service_times[i] - arrival_times[i]
    
    # Compute average queue length by summing all waiting times and dividing by total simulation time
    total_sim_time   = completion_times[-1] - arrival_times[0]
    sum_of_waiting   = np.sum(waiting_times)
    avg_queue_length = sum_of_waiting / total_sim_time if total_sim_time > 0 else 0.0
    
    # Calculate costs
    waiting_cost_hourly = waiting_cost_per_hour * avg_queue_length
    total_hourly_cost   = server_cost_per_hour + waiting_cost_hourly
    avg_waiting_time    = np.mean(waiting_times)
    
    return total_hourly_cost, avg_waiting_time, avg_queue_length

if __name__ == "__main__":
    # Use for three scenarios:

    # 1) Current system
    c1, w1, q1 = simulate_queue(
        num_customers=500,
        arrival_rate_per_hour=10.0,
        service_time_mean=5.0,
        service_time_type='exponential',
        server_cost_per_hour=20.0,
        waiting_cost_per_hour=2.0,
        random_seed=42
    )
    
    # 2) Computerized system
    c2, w2, q2 = simulate_queue(
        num_customers=500,
        arrival_rate_per_hour=10.0,
        service_time_mean=4.0,
        service_time_type='deterministic',
        server_cost_per_hour=7.0,
        waiting_cost_per_hour=2.0,
        random_seed=42
    )
    
    # 3) New faster registrar
    c3, w3, q3 = simulate_queue(
        num_customers=500,
        arrival_rate_per_hour=10.0,
        service_time_mean=3.0,
        service_time_type='exponential',
        server_cost_per_hour=32.0,
        waiting_cost_per_hour=2.0,
        random_seed=42
    )
    
    print("=== Current System ===")
    print(f"Hourly Cost: {c1:.2f} €, Avg Wait: {w1:.2f} min, Avg Queue: {q1:.2f}\n")
    
    print("=== Computerized System ===")
    print(f"Hourly Cost: {c2:.2f} €, Avg Wait: {w2:.2f} min, Avg Queue: {q2:.2f}\n")
    
    print("=== New Registrar ===")
    print(f"Hourly Cost: {c3:.2f} €, Avg Wait: {w3:.2f} min, Avg Queue: {q3:.2f}\n")