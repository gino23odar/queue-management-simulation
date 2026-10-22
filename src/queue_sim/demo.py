from .models import Customer
from .simulator import STRATEGIES, simulate


def main():

    customers = [
        Customer(0, 0, 8, 1),
        Customer(1, 0, 2, 1),
        Customer(2, 0, 4, 0),
    ]

    for strategy in STRATEGIES:

        records = simulate(
            customers,
            strategy=strategy,
        )

        print(
            f"\nStrategy: {strategy.upper()}"
        )

        for record in records:

            print(
                f"Customer {record.customer_id}: "
                f"wait={record.wait:.2f}"
            )


if __name__ == "__main__":
    main()