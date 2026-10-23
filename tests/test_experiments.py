import csv

from src.queue_sim.experiments import run_experiments


def test_experiments_are_reproducible(tmp_path):

    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    run_experiments(
        repetitions=2,
        output_dir=str(first_dir),
    )

    run_experiments(
        repetitions=2,
        output_dir=str(second_dir),
    )

    with (
        first_dir / "experiments.csv"
    ).open(newline="") as file:

        first = list(
            csv.DictReader(file)
        )

    with (
        second_dir / "experiments.csv"
    ).open(newline="") as file:

        second = list(
            csv.DictReader(file)
        )

    assert first == second

    # 3 loads x 3 server configurations
    # x 3 algorithms x 2 repetitions
    assert len(first) == 54