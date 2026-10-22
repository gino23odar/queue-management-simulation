import heapq
from math import inf

from .models import Customer, ServiceRecord


def simulate(
    customers: list[Customer],
    strategy: str = "fcfs", # first-come first-served
    servers: int = 1,
) -> list[ServiceRecord]:

    if strategy != "fcfs":
        raise ValueError("Only FCFS is supported")

    if servers < 1:
        raise ValueError(
            "At least one server is required"
        )

    if len({c.id for c in customers}) != len(customers):
        raise ValueError(
            "Customer IDs must be unique"
        )

    arrivals = sorted(
        customers,
        key=lambda c: (c.arrival, c.id),
    )

    free_servers = list(range(servers))
    heapq.heapify(free_servers)

    # (completion_time, server_id)
    ongoing = []

    waiting = []
    records = []
    next_customer = 0

    while (
        next_customer < len(arrivals)
        or ongoing
        or waiting
    ):

        next_arrival = (
            arrivals[next_customer].arrival
            if next_customer < len(arrivals)
            else inf
        )

        next_completion = (
            ongoing[0][0]
            if ongoing
            else inf
        )

        now = min(
            next_arrival,
            next_completion,
        )

        # Release employees who finished service.
        while ongoing and ongoing[0][0] <= now:

            _, server_id = heapq.heappop(ongoing)

            heapq.heappush(
                free_servers,
                server_id,
            )

        # Register new arrivals.
        while (
            next_customer < len(arrivals)
            and arrivals[next_customer].arrival <= now
        ):

            customer = arrivals[next_customer]
            waiting.append(customer)
            next_customer += 1

        # Assign waiting customers to free servers.
        while free_servers and waiting:

            server_id = heapq.heappop(
                free_servers
            )

            customer = waiting.pop(0)

            end = now + customer.duration

            records.append(
                ServiceRecord(
                    customer_id=customer.id,
                    server_id=server_id,
                    arrival=customer.arrival,
                    start=now,
                    end=end,
                    priority=customer.priority,
                )
            )

            heapq.heappush(
                ongoing,
                (end, server_id),
            )

    return sorted(
        records,
        key=lambda r: (
            r.start,
            r.server_id,
            r.customer_id,
        ),
    )