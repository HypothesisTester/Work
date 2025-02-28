import random

def draw_loading_time():
    """
    Random loading time (minutes):
      5 with prob 0.7,
      10 with prob 0.3
    """
    return 5 if random.random() < 0.7 else 10

def draw_weighing_time():
    """
    Random weighing time (minutes):
      2 with prob 0.6,
      4 with prob 0.4
    """
    return 2 if random.random() < 0.6 else 4

def draw_travel_time():
    """
    Random travel time (minutes):
      30 with prob 0.5,
      45 with prob 0.5
    """
    return 30 if random.random() < 0.5 else 45

class Truck:
    """
    A truck with an ID, a state, and a finish time.
    """
    def __init__(self, truck_id):
        self.id = truck_id
        self.state = "waiting_for_load"
        self.finish_time = float('inf')

def simulate_next_10_events():
    """
    Simulates 10 events in a system with:
      - 4 trucks
      - 2 loading bays
      - 1 scale
      - Probabilistic loading, weighing, travel times

    Returns a list of (event_time, event_description, system_state).
    """
    random.seed(0)

    trucks = [Truck(i) for i in range(1, 5)]
    # Two trucks start loading immediately
    trucks[0].state = "loading"
    trucks[0].finish_time = draw_loading_time()
    trucks[1].state = "loading"
    trucks[1].finish_time = draw_loading_time()

    loading_bays_in_use = 2
    scale_in_use = False

    events = []
    count = 0

    while count < 10:
        # Find the earliest finishing truck
        next_time = float('inf')
        next_truck = None
        for t in trucks:
            if t.state in ("loading", "weighing", "travelling"):
                if t.finish_time < next_time:
                    next_time = t.finish_time
                    next_truck = t

        if not next_truck:
            break

        count += 1
        old_state = next_truck.state
        description = f"Truck {next_truck.id} finished {old_state}."

        if old_state == "loading":
            loading_bays_in_use -= 1
            if not scale_in_use:
                scale_in_use = True
                next_truck.state = "weighing"
                next_truck.finish_time = next_time + draw_weighing_time()
            else:
                next_truck.state = "waiting_for_scale"
                next_truck.finish_time = float('inf')

            # Start loading any waiting truck if a bay is free
            for t in trucks:
                if t.state == "waiting_for_load" and loading_bays_in_use < 2:
                    t.state = "loading"
                    t.finish_time = next_time + draw_loading_time()
                    loading_bays_in_use += 1
                    break

        elif old_state == "weighing":
            scale_in_use = False
            next_truck.state = "travelling"
            next_truck.finish_time = next_time + draw_travel_time()

            # Let a waiting truck weigh if present
            for t in trucks:
                if t.state == "waiting_for_scale":
                    t.state = "weighing"
                    t.finish_time = next_time + draw_weighing_time()
                    scale_in_use = True
                    break

        elif old_state == "travelling":
            if loading_bays_in_use < 2:
                loading_bays_in_use += 1
                next_truck.state = "loading"
                next_truck.finish_time = next_time + draw_loading_time()
            else:
                next_truck.state = "waiting_for_load"
                next_truck.finish_time = float('inf')

        state_summary = ", ".join(f"T{t.id}:{t.state}" for t in trucks)
        resource_summary = f"LoadingBaysUsed={loading_bays_in_use}, ScaleUsed={scale_in_use}"
        events.append((next_time, description, f"{state_summary}; {resource_summary}"))

    return events

if __name__ == "__main__":
    outcome = simulate_next_10_events()
    for i, (time_, desc, summary) in enumerate(outcome, 1):
        print(f"Event {i} at t={time_:.2f} min: {desc}")
        print(f"  State => {summary}\n")