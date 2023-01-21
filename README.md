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
python run_queue.py -q CUSTOM

### Dumb Queue Results
```
Match "Fairness"
       Team 1 Estimated Probability To Win  ABS Value Probability To Win Difference  Team 1 Average MMR (weighted)  Team 2 Average MMR (weighted)  ABS MMR Difference
count                         11339.000000                             11339.000000                   11339.000000                   11339.000000        11339.000000
mean                              0.501471                                 0.345220                    2497.560107                    2495.892839          339.941847
std                               0.205952                                 0.224690                     302.860979                     302.647030          258.603255
min                               0.023529                                 0.000115                    1291.200000                    1190.450000            0.000000
25%                               0.341521                                 0.156713                    2293.550000                    2290.750000          136.150000
50%                               0.500345                                 0.318589                    2498.200000                    2496.700000          286.950000
75%                               0.660612                                 0.509782                    2700.950000                    2701.425000          483.800000
max                               0.971308                                 0.952941                    3736.450000                    3689.200000         1615.350000
               
Queue Wait Time (s)
               Wait
count  90010.000000
mean      18.001689
std        8.817228
min        0.000000
25%       10.000000
50%       18.000000
75%       26.000000
max       43.000000
```