import pytest

from src.queue_sim.models import Customer
from src.queue_sim.simulator import simulate


def test_fcfs_order_and_waits():

    customers = [
        Customer(0, 0, 8),
        Customer(1, 0, 2),
        Customer(2, 0, 4),
    ]

    records = simulate(customers)

    assert [
        r.customer_id for r in records
    ] == [0, 1, 2]

    assert [
        r.wait for r in records
    ] == [0, 8, 10]


def test_idle_server():

    customers = [
        Customer(0, 10, 2),
    ]

    records = simulate(customers)

    assert records[0].start == 10
    assert records[0].wait == 0


def test_multiple_servers():

    customers = [
        Customer(0, 0, 8),
        Customer(1, 0, 2),
        Customer(2, 0, 4),
    ]

    records = simulate(
        customers,
        servers=2,
    )

    assert [
        (r.customer_id, r.start)
        for r in records
    ] == [
        (0, 0),
        (1, 0),
        (2, 2),
    ]