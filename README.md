# Overwatch Queue Simulator
There are constantly complaints about how bad match-making is in Overwatch. I wanted to try my hand at a simple queue simulator to
see what a baseline matchmaker would look like, then make continuous improvements. The goal is to get the lowest score possible.


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

- When a player is created, they will randomly be assigned some combination of roles (Tank, DPS, Support) that they will always queue for.


## To Run
```
python run_queue.py -q BASIC 
python run_queue.py -q BUCKET
python run_queue.py -q CUSTOM  
```

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
Score: 3486 - Wait Score: 3112 - MMR Score: 374
       Team 1 Estimated Probability To Win  ABS Value Probability To Win Difference  Team 1 Average MMR (weighted)  Team 2 Average MMR (weighted)  ABS MMR Difference
count                         11317.000000                             11317.000000                   11317.000000                   11317.000000        11317.000000
mean                              0.499127                                 0.064575                    2525.103115                    2527.535420           18.810383
std                               0.040817                                 0.049967                     553.146736                     552.458755           20.994311
min                               0.317105                                 0.000000                     532.550000                     520.250000            0.000000
25%                               0.472598                                 0.024978                    2149.750000                    2151.200000            6.550000
50%                               0.499309                                 0.053714                    2543.350000                    2543.750000           14.000000
75%                               0.526369                                 0.093099                    2926.100000                    2924.650000           24.500000
max                               0.679369                                 0.365789                    4273.150000                    4254.050000          352.300000
               Wait          Tank           DPS       Support
count  89960.000000  89960.000000  89960.000000  89960.000000
mean      55.069086   2498.589351   2495.866074   2495.538673
std       80.251588    577.244692    577.440827    573.807233
min        0.000000    216.000000    192.000000    263.000000
25%       23.000000   2108.000000   2100.000000   2102.000000
50%       38.000000   2495.000000   2495.000000   2499.000000
75%       65.000000   2894.000000   2895.000000   2883.000000
max     6150.000000   4852.000000   4808.000000   4754.000000

```
