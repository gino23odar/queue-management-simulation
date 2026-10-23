import heapq
from math import inf

from .models import Customer, ServiceRecord


STRATEGIES = ("fcfs", "spt", "priority")


def _selection_key(
    customer: Customer,
    strategy: str,
) -> tuple:

    if strategy == "fcfs":
        return (
            customer.arrival,
            customer.id,
        )

    if strategy == "spt":
        return (
            customer.duration,
            customer.arrival,
            customer.id,
        )

    return (
        customer.priority,
        customer.arrival,
        customer.id,
    )


def simulate(
    customers: list[Customer],
    strategy: str = "fcfs",
    servers: int = 1,
) -> list[ServiceRecord]:

    if strategy not in STRATEGIES:
        raise ValueError(
            f"Unknown strategy: {strategy}"
        )

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

    # Available employees.
    free_servers = list(range(servers))
    heapq.heapify(free_servers)

    # Active jobs:
    # (completion_time, server_id)
    ongoing = []

    # Waiting queue:
    # (selection_key, customer_id, customer)
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

        # Release servers finishing at this event time.
        while ongoing and ongoing[0][0] <= now:

            _, server_id = heapq.heappop(
                ongoing
            )

            heapq.heappush(
                free_servers,
                server_id,
            )

        # Add customers arriving at this event time.
        while (
            next_customer < len(arrivals)
            and arrivals[next_customer].arrival <= now
        ):

            customer = arrivals[next_customer]

            heapq.heappush(
                waiting,
                (
                    _selection_key(
                        customer,
                        strategy,
                    ),
                    customer.id,
                    customer,
                ),
            )

            next_customer += 1

        # Dispatch jobs using heap-based selection.
        while free_servers and waiting:

            server_id = heapq.heappop(
                free_servers
            )

            _, _, customer = heapq.heappop(
                waiting
            )

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