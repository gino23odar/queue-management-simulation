# Phase 2

## Question

How do the FCFS algorithm, shortest processing time and priority algorithms perform in terms of customer waiting times and service efficiency when varying the number of customers and number of employees?

## Starting Point

Started off with a single server FCFS queue.

Kept track of when each customer started being served, calculating service start times sequentially.

Did not allow for multiple employees to serve customers at the same time.

## Switching to Events

Changed to use an event-driven queueing algorithm.

Now able to handle customer arrivals, service completions and multiple employees serving customers at the same time.

## Algorithms

First come first serve

Shortest processing time

Priority-based scheduling

All algorithms are non-preemptive.

## Optimizing Waiting Customers

Had a list of customers that were waiting to be served.

Would have to iterate through the list to find who would be served next.

Changed this to use a heap-based priority queue which allowed me to get the next person to be served faster.

## Workload

Workloads of 100, 300 and 500 customers were tested.

Number of employees tested were 1, 2 and 4.

Ran each configuration 30 times.

Same generated workloads were used for all algorithms and numbers of employees.

## Measurements

Currently measuring the average time a customer will have to wait, max time a customer has to wait, the 95th percentile time a customer has to wait, throughput during opening hours and the utilization of the employees.

Other measurements are made on how long customers from different priority groups have to wait compared to each other.

## Statistics

Using paired workloads we can measure the differences between each algorithm.

Bootstrapping is used to calculate confidence intervals, giving us an indication of how much the results vary across synthetic workloads.

## Tests

Tests have been written to check that customers are served in the right order, that the time they have to wait is correct, multiple employees can serve customers at the same time, customers are generated correctly, the same workload can be reproduced and many other edge cases.

## Limitations

Our workloads are synthetic.

We assume that we know the estimated duration of each service beforehand.

Customers will never give up waiting.

Employees do not take breaks and the model does not account for service interruptions. Customers do not change their priority during their stay in the queue.

## Next Steps

Could experiment with more realistic arrival patterns and other types of queueing algorithms. Or we could apply our algorithm to a different situation that requires resource management.