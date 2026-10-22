from dataclasses import dataclass
from math import ceil
from statistics import mean

from .models import ServiceRecord


@dataclass(frozen=True)
class Metrics:
    mean_wait: float
    max_wait: float
    p95_wait: float
    completed_before_close: int
    utilization_during_hours: float


def calculate_metrics(
    records: list[ServiceRecord],
    servers: int,
    day_minutes: float = 480,
) -> Metrics:

    if servers < 1 or day_minutes <= 0:
        raise ValueError(
            "Invalid server count or day length"
        )

    if not records:
        return Metrics(
            mean_wait=0,
            max_wait=0,
            p95_wait=0,
            completed_before_close=0,
            utilization_during_hours=0,
        )

    waits = sorted(
        record.wait
        for record in records
    )

    average_wait = mean(waits)
    maximum_wait = max(waits)

    percentile_index = (
        ceil(0.95 * len(waits)) - 1
    )

    p95_wait = waits[percentile_index]

    completed = sum(
        record.end <= day_minutes
        for record in records
    )

    busy_minutes = sum(
        max(
            0.0,
            min(record.end, day_minutes)
            - max(record.start, 0.0),
        )
        for record in records
    )

    utilization = (
        busy_minutes / (servers * day_minutes)
    )

    return Metrics(
        mean_wait=average_wait,
        max_wait=maximum_wait,
        p95_wait=p95_wait,
        completed_before_close=completed,
        utilization_during_hours=utilization,
    )