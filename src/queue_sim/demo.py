from .models import Customer
from .simulator import simulate


def main():

    customers = [
        Customer(0, 0, 8),
        Customer(1, 2, 2),
        Customer(2, 4, 4),
    ]

    results = simulate(customers)

    for record in results:
        print(
            f"Customer {record.customer_id}: "
            f"start={record.start}, "
            f"end={record.end}, "
            f"wait={record.wait}"
        )


if __name__ == "__main__":
    main()