# Overwatch Queue Simulator
There are constantly complaints about how bad match-making is in Overwatch. I wanted to try my hand at a simple queue simulator to
see what a baseline match maker would look like, then make continuous improvements.

###Assumptions:
- Every tick of the clock is equivalent to 1 second

- The worst player on a team has more impact than the best player on the team. This is modeled by using a weighted average
when calculating average MMR for a team. The weights are applied from lowest MMR on the team to the highest and are:
`.3, .2, .15, .15, .2`. 

- There are 100000 players available in our simulations player base

- The simulation runs for the equivalent of 6 hours, but only time in queue for the final 5 hours is record. This gives the simulation 1 hour to stabilize and filter out the initial players in queue

- The average match takes 15 minutes, with a standard deviation of 3 minutes

- MMR has a minimum value of 0, maximum value of 5000 and a standard deviation of 500

- A player is randomly given a base MMR, that MMR is then expanded randomly into each individual role MMR.

- A player is randomly assigned to queue for any combination possible of Tank, DPS and/or Support.


## To Run
python run_queue.py -q BASIC
python run_queue.py -q BUCKET
python run_queue.py -q CUSTOM  

### Dumb Queue Results
```
Score: 121570 - Wait Score: 332 - MMR Score: 121238

       Team 1 Estimated Probability To Win  ABS Value Probability To Win Difference  Team 1 Average MMR (weighted)  Team 2 Average MMR (weighted)  ABS MMR Difference
count                         11336.000000                             11336.000000                   11336.000000                   11336.000000        11336.000000
mean                              0.500949                                 0.350202                    2501.191478                    2498.778727          347.812875
std                               0.208862                                 0.227695                     308.929438                     306.754327          264.525578
min                               0.019780                                 0.000000                    1252.050000                    1356.500000            0.050000
25%                               0.337538                                 0.157723                    2294.325000                    2293.775000          137.812500
50%                               0.500604                                 0.324756                    2502.350000                    2498.300000          291.900000
75%                               0.662236                                 0.520963                    2709.912500                    2704.437500          506.037500
max                               0.980311                                 0.960623                    3617.300000                    3771.300000         1809.800000
               Wait          Tank           DPS       Support
count  90000.000000  90000.000000  90000.000000  90000.000000
mean      17.996678   2501.097156   2500.507511   2500.203922
std        8.824013    578.015239    580.009935    581.433718
min        0.000000     44.000000    262.000000    189.000000
25%       10.000000   2104.000000   2106.000000   2105.000000
50%       18.000000   2501.000000   2504.000000   2498.000000
75%       25.000000   2896.000000   2895.000000   2893.000000
max       42.000000   4981.000000   4930.000000   4916.000000
```

### Bucket Queue Results
```
Score: 6547 - Wait Score: 3165 - MMR Score: 3382

       Team 1 Estimated Probability To Win  ABS Value Probability To Win Difference  Team 1 Average MMR (weighted)  Team 2 Average MMR (weighted)  ABS MMR Difference
count                         11317.000000                             11317.000000                   11317.000000                   11317.000000        11317.000000
mean                              0.497315                                 0.065717                    2530.814178                    2533.661209           57.773765
std                               0.041506                                 0.050997                     555.824993                     555.300979           44.760919
min                               0.277235                                 0.000000                     548.350000                     578.500000            0.000000
25%                               0.470504                                 0.026128                    2154.750000                    2160.400000           23.400000
50%                               0.497467                                 0.054575                    2536.900000                    2541.000000           48.300000
75%                               0.524761                                 0.094925                    2918.500000                    2915.700000           82.350000
max                               0.743569                                 0.487137                    4325.050000                    4296.750000          473.700000
               Wait          Tank           DPS       Support
count  89950.000000  89950.000000  89950.000000  89950.000000
mean      55.436876   2502.848627   2501.704158   2502.335208
std       92.254672    575.692311    575.003954    576.134597
min        0.000000    313.000000    220.000000    281.000000
25%       23.000000   2112.000000   2109.000000   2109.000000
50%       38.000000   2504.000000   2503.000000   2502.000000
75%       64.000000   2894.000000   2897.000000   2895.000000
max    11078.000000   4849.000000   4829.000000   4881.000000
```