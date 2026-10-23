import argparse
import csv

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


from .simulator import STRATEGIES


def make_plots(
    summary_file: str = "results/summary.csv",
    servers: int = 2,
) -> None:

    with Path(summary_file).open(
        newline="",
        encoding="utf-8",
    ) as file:

        rows = [
            row
            for row in csv.DictReader(file)
            if int(row["servers"]) == servers
        ]

    if not rows:
        raise ValueError(
            f"No results for {servers} servers"
        )

    output_dir = (
        Path(summary_file).parent / "figures"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics = (
        ("mean_wait", "Mean wait (minutes)"),
        ("max_wait", "Maximum wait (minutes)"),
        ("p95_wait", "95th-percentile wait (minutes)"),
        (
            "completed_before_close",
            "Customers completed before closing",
        ),
    )

    for field, label in metrics:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        for strategy in STRATEGIES:

            data = sorted(
                (
                    row
                    for row in rows
                    if row["strategy"] == strategy
                ),
                key=lambda row: int(
                    row["customers"]
                ),
            )

            x = [
                int(row["customers"])
                for row in data
            ]

            y = [
                float(row[field])
                for row in data
            ]

            ax.plot(
                x,
                y,
                marker="o",
                label=strategy.upper(),
            )

        ax.set(
            title=f"{label} | {servers} servers",
            xlabel="Customers per day",
            ylabel=label,
        )

        ax.grid(alpha=0.3)
        ax.legend()

        fig.tight_layout()

        path = (
            output_dir
            / f"{field}_{servers}_servers.png"
        )

        fig.savefig(
            path,
            dpi=160,
        )

        plt.close(fig)

        print(f"Saved {path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--summary-file",
        default="results/summary.csv",
    )

    parser.add_argument(
        "--servers",
        type=int,
        default=2,
    )

    args = parser.parse_args()

    make_plots(
        summary_file=args.summary_file,
        servers=args.servers,
    )