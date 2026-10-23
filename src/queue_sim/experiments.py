import argparse
import csv

from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from statistics import mean, stdev

from .generator import generate_customers
from .metrics import calculate_metrics
from .simulator import STRATEGIES, simulate


LOADS = (100, 300, 500)
SERVER_COUNTS = (1, 2, 4)

def optional_mean(values):

    valid = [
        value
        for value in values
        if value is not None
    ]

    return mean(valid) if valid else None


def run_experiments(
    repetitions: int = 30,
    output_dir: str = "results",
) -> None:

    if repetitions < 1:
        raise ValueError(
            "Repetitions must be positive"
        )

    output = Path(output_dir)

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    for count in LOADS:

        for repetition in range(repetitions):

            seed = 1000 * count + repetition

            customers = generate_customers(
                count=count,
                seed=seed,
            )

            for servers in SERVER_COUNTS:

                for strategy in STRATEGIES:

                    records = simulate(
                        customers,
                        strategy=strategy,
                        servers=servers,
                    )

                    metrics = calculate_metrics(
                        records,
                        servers=servers,
                    )

                    rows.append({
                        "customers": count,
                        "servers": servers,
                        "repetition": repetition,
                        "seed": seed,
                        "strategy": strategy,
                        **asdict(metrics),
                    })

    # Export individual simulation results.
    raw_path = output / "experiments.csv"

    with raw_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0]),
        )

        writer.writeheader()
        writer.writerows(rows)

    # Group results by experimental configuration.
    grouped = defaultdict(list)

    for row in rows:

        key = (
            row["customers"],
            row["servers"],
            row["strategy"],
        )

        grouped[key].append(row)

    summary_rows = []

    for (count, servers, strategy), data in sorted(
        grouped.items()
    ):

        waiting_times = [
            row["mean_wait"]
            for row in data
        ]

        summary_rows.append({
            "customers": count,
            "servers": servers,
            "strategy": strategy,
            "repetitions": len(data),

            "mean_wait": mean(waiting_times),

            "sd_mean_wait": (
                stdev(waiting_times)
                if len(waiting_times) > 1
                else 0.0
            ),

            "max_wait": mean(
                row["max_wait"]
                for row in data
            ),

            "p95_wait": mean(
                row["p95_wait"]
                for row in data
            ),

            "completed_before_close": mean(
                row["completed_before_close"]
                for row in data
            ),

            "utilization_during_hours": mean(
                row["utilization_during_hours"]
                for row in data
            ),

            "high_priority_mean_wait": optional_mean(
                row["high_priority_mean_wait"]
                for row in data
            ),

            "regular_priority_mean_wait": optional_mean(
                row["regular_priority_mean_wait"]
                for row in data
            ),

            "priority_wait_gap": optional_mean(
                row["priority_wait_gap"]
                for row in data
            ),
        })

    # Export aggregated results.
    summary_path = output / "summary.csv"

    with summary_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(summary_rows[0]),
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print(
        f"Saved {len(rows)} simulation runs "
        f"to {output}"
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repetitions",
        type=int,
        default=30,
    )

    parser.add_argument(
        "--output-dir",
        default="results",
    )

    args = parser.parse_args()

    run_experiments(
        repetitions=args.repetitions,
        output_dir=args.output_dir,
    )