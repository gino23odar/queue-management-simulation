from .models import Customer, ServiceRecord


def simulate(
    customers: list[Customer],
    strategy: str = "fcfs", # first-come first-served
    servers: int = 1,
) -> list[ServiceRecord]:

    if strategy != "fcfs":
        raise ValueError("Only FCFS is supported")

    if servers != 1:
        raise ValueError("Only one server is supported")

    if len({c.id for c in customers}) != len(customers):
        raise ValueError("Customer IDs must be unique")

    current_time = 0.0
    records = []

    arrivals = sorted(
        customers,
        key=lambda c: (c.arrival, c.id),
    )

    for customer in arrivals:

        start = max(
            current_time,
            customer.arrival,
        )

        end = start + customer.duration

        records.append(
            ServiceRecord(
                customer_id=customer.id,
                server_id=0,
                arrival=customer.arrival,
                start=start,
                end=end,
                priority=customer.priority,
            )
        )

        current_time = end

    return records