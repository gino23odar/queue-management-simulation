from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    id: int
    arrival: float
    duration: float
    priority: int = 1

    def __post_init__(self):
        if self.id < 0:
            raise ValueError(
                "Customer ID must be non-negative"
            )

        if self.arrival < 0:
            raise ValueError(
                "Arrival must be non-negative"
            )

        if self.duration <= 0:
            raise ValueError(
                "Duration must be non-negative"
            )

        if self.priority not in (0, 1):
            raise ValueError(
                "Priority must be 0 or 1"
            )


@dataclass(frozen=True)
class ServiceRecord:
    customer_id: int
    server_id: int
    arrival: float
    start: float
    end: float
    priority: int

    @property
    def wait(self) -> float:
        return self.start - self.arrival