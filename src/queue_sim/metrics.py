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

    high_priority_mean_wait: float | None
    regular_priority_mean_wait: float | None
    priority_wait_gap: float | None


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
            high_priority_mean_wait=None,
            regular_priority_mean_wait=None,
            priority_wait_gap=None,
        )

    waits = sorted(
        r.wait for r in records
    )

    high_waits = [
        r.wait
        for r in records
        if r.priority == 0
    ]

    regular_waits = [
        r.wait
        for r in records
        if r.priority == 1
    ]

    high_mean = (
        mean(high_waits)
        if high_waits
        else None
    )

    regular_mean = (
        mean(regular_waits)
        if regular_waits
        else None
    )

    gap = (
        regular_mean - high_mean
        if high_mean is not None
        and regular_mean is not None
        else None
    )

    busy_minutes = sum(
        max(
            0.0,
            min(r.end, day_minutes)
            - max(r.start, 0.0),
        )
        for r in records
    )

    return Metrics(
        mean_wait=mean(waits),

        max_wait=max(waits),

        p95_wait=waits[
            ceil(0.95 * len(waits)) - 1
        ],

        completed_before_close=sum(
            r.end <= day_minutes
            for r in records
        ),

        utilization_during_hours=(
            busy_minutes / (servers * day_minutes)
        ),

        high_priority_mean_wait=high_mean,
        regular_priority_mean_wait=regular_mean,
        priority_wait_gap=gap,
    )