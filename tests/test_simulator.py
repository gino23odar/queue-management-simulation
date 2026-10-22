import pytest

from src.queue_sim.models import Customer
from src.queue_sim.simulator import simulate
from src.queue_sim.generator import generate_customers


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

def test_shortest_processing_time():

    customers = [
        Customer(0, 0, 8),
        Customer(1, 0, 2),
        Customer(2, 0, 4),
    ]

    records = simulate(
        customers,
        strategy="spt",
    )

    assert [
        r.customer_id for r in records
    ] == [1, 2, 0]


def test_priority_scheduling():

    customers = [
        Customer(0, 0, 8, 1),
        Customer(1, 0, 2, 1),
        Customer(2, 0, 4, 0),
    ]

    records = simulate(
        customers,
        strategy="priority",
    )

    assert [
        r.customer_id for r in records
    ] == [2, 0, 1]


def test_priority_does_not_interrupt_service():

    customers = [
        Customer(0, 0, 8, 1),
        Customer(1, 1, 1, 0),
    ]

    records = simulate(
        customers,
        strategy="priority",
    )

    assert records[1].start == 8

def test_customer_generation_is_reproducible():

    first = generate_customers(
        count=100,
        seed=42,
    )

    second = generate_customers(
        count=100,
        seed=42,
    )

    assert first == second


def test_different_seeds_generate_different_data():

    first = generate_customers(
        count=100,
        seed=42,
    )

    second = generate_customers(
        count=100,
        seed=43,
    )

    assert first != second