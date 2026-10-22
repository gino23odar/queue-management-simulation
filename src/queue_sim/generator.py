import random

from .models import Customer


def generate_customers(
    count: int,
    seed: int,
    day_minutes: float = 480,
) -> list[Customer]:

    if count < 0:
        raise ValueError(
            "Customer count cannot be negative"
        )

    if day_minutes <= 0:
        raise ValueError(
            "Day length must be positive"
        )

    rng = random.Random(seed)

    customers = []

    for i in range(count):

        arrival = rng.uniform(
            0,
            day_minutes,
        )

        duration = rng.triangular(
            2,
            8,
            4,
        )

        priority = (
            0 if rng.random() < 0.20
            else 1
        )

        customers.append(
            Customer(
                id=i,
                arrival=arrival,
                duration=duration,
                priority=priority,
            )
        )

    return sorted(
        customers,
        key=lambda c: (c.arrival, c.id),
    )