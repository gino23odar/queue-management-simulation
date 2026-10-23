import pytest

from src.queue_sim.comparison import bootstrap_interval


def test_bootstrap_is_reproducible():

    differences = [
        2, 3, 4, 5, 6
    ]

    first = bootstrap_interval(
        differences,
        seed=42,
    )

    second = bootstrap_interval(
        differences,
        seed=42,
    )

    assert first == second


def test_constant_difference():

    differences = [5.0] * 30

    estimate, lower, upper = bootstrap_interval(
        differences
    )

    assert estimate == pytest.approx(5.0)
    assert lower == pytest.approx(5.0)
    assert upper == pytest.approx(5.0)


def test_empty_differences_rejected():

    with pytest.raises(ValueError):
        bootstrap_interval([])