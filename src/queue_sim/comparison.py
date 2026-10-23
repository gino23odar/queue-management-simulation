import csv
import random

from pathlib import Path
from statistics import mean


def bootstrap_interval(
    differences: list[float],
    draws: int = 2000,
    seed: int = 42,
) -> tuple[float, float, float]:

    if not differences or draws < 1:
        raise ValueError(
            "Need differences and at least one bootstrap draw"
        )

    rng = random.Random(seed)

    estimates = sorted(
        mean(
            rng.choices(
                differences,
                k=len(differences),
            )
        )
        for _ in range(draws)
    )

    lower_index = int(
        0.025 * (draws - 1)
    )

    upper_index = int(
        0.975 * (draws - 1)
    )

    return (
        mean(differences),
        estimates[lower_index],
        estimates[upper_index],
    )


def compare_algorithms(
    input_file: str = "results/experiments.csv",
    output_file: str = "results/comparison.csv",
) -> None:

    with Path(input_file).open(
        newline="",
        encoding="utf-8",
    ) as file:

        rows = list(
            csv.DictReader(file)
        )

    # group results belonging to the same workload
    grouped = {}

    for row in rows:

        key = (
            int(row["customers"]),
            int(row["servers"]),
            int(row["repetition"]),
        )

        grouped.setdefault(
            key,
            {},
        )[row["strategy"]] = float(
            row["mean_wait"]
        )

    comparisons = []

    configurations = sorted({
        key[:2]
        for key in grouped
    })

    for customers, servers in configurations:

        for alternative in ("spt", "priority"):

            differences = []

            for key, strategies in grouped.items():

                if key[:2] != (customers, servers):
                    continue

                if not (
                    {"fcfs", alternative}
                    <= strategies.keys()
                ):
                    continue

                difference = (
                    strategies["fcfs"]
                    - strategies[alternative]
                )

                differences.append(difference)

            if not differences:
                continue

            estimate, lower, upper = bootstrap_interval(
                differences
            )

            comparisons.append({
                "customers": customers,
                "servers": servers,
                "alternative": alternative,
                "repetitions": len(differences),
                "mean_improvement": estimate,
                "ci_lower": lower,
                "ci_upper": upper,
            })

    output = Path(output_file)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "customers",
                "servers",
                "alternative",
                "repetitions",
                "mean_improvement",
                "ci_lower",
                "ci_upper",
            ],
        )

        writer.writeheader()
        writer.writerows(comparisons)

    print(f"Saved {output}")


if __name__ == "__main__":
    compare_algorithms()