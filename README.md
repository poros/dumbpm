# dumbpm

[![PyPI version](https://badge.fury.io/py/dumbpm.svg)](https://badge.fury.io/py/dumbpm)
[![Continuous Integration](https://github.com/poros/dumbpm/workflows/Continuous%20Integration/badge.svg)](https://github.com/poros/dumbpm/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

* [Installation](#installation)
* [Prioritize projects](#prioritize-projects)
  + [Projects format](#projects-format)
  + [Example](#example)
* [Estimate project duration without historical data](#estimate-project-duration-without-historical-data)
  + [Input format](#input-format)
  + [Example](#example-1)
* [Estimate project duration based on historical data](#estimate-project-duration-based-on-historical-data)
  + [Input format](#input-format-1)
  + [Example](#example-2)

A pretty dumb PM.

The whole philosophy behind `dumbpm` is that PMs (project managers, program managers, product managers, people managers, pokemon masters, etc.) all do some tasks that could use some automation, but at the same time this automation should be as dumb as possible. There are so many changing factors that influence such tasks that you better hire a PM (or a team of researchers to do the automation) to do the clever stuff, not a random software on the internet. In addition, if we keep it dumb, people can just read the code and understand what is going on, if they really want to.

If you have any suggestions for something (but nothing clever!) that you would like `dumbpm` to do for you, open an issue and let me know.

## Installation

```
pip install dumbpm
```

Tested on both Linux and Mac OS. Windows _might_ work.

**NOTE** Python 3.9+ required.

## Prioritize projects

Giving a table of projects defined as below, it outputs a list of projects in order of priority within the optionally specified budget (prioritization as "data problem").

The prioritized list is modelled as the exact solution of a [Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem) with the following value function: `norm(norm(value) / (norm(cost) + norm(duration) + norm(risk))) + norm(rigging)`. Pretty dumb, indeed.

If `--budget` isn't specified, the list will simply be sorted by the result of the above value function. Budget is relative to the `cost` parameter.

If you are expressing `cost` as cost per unit of duration (e.g. developers per week or sprint), you'll have to specify the `--cost-per-duration` option, so that `total cost = cost * duration` and `budget` is measured against `total cost` (`duration` will also disappear from the value function not to count it twice).

```bash
$ dumbpm prioritize --help
usage: dumbpm prioritize [-h] [--budget [BUDGET]] filename

positional arguments:
  filename           CSV file with projects definition

optional arguments:
  -h, --help         show this help message and exit
  --budget [BUDGET]  Max budget allowed
  --cost-per-duration  Cost is to be assumed per unit of duration. Budget =
                       (cost * duration)
```

### Projects format

Project definition happens in a CSV file with the following structure:

- `Project`: [required] name of the project
- `Value`: [required] value of the project
- `Cost`: [required] cost of the project
- `Duration`: [optional] duration of the project expressed in unit of times
- `Risk`: [optional] risk of failure of the project
- `Rigging`: [optional, empty field = 0] arbitrary value used to rig the result (yay, cheating!); the highest the more likely the project to be prioritized (keep in mind that this counts for half of the score of a project)
- `Alternatives`: [optional, empty field = empty list] comma separated list of projects that are incompatible with this one (e.g. make lunch vs buy lunch)

There is a bit of slack on the headers of the columns (e.g. `Project`, `Projects`, `project`, etc. are all alright). Notable mentions: `rig` and `rigging` both work; same for `alts` and `alternatives`; `PQ` can be used instead of `cost` if that's your thing.


| Project                                             | Value | Cost | Duration | Risk | Rigging | Alternatives                                |
|-----------------------------------------------------|-------|------|----------|------|---------|---------------------------------------------|
| Buy a better espresso machine                       | 5     | 4    | 2        |1     | 9       |                                             |
| Buy ambient parfume for the back                    | 1     | 1    | 1        |1     |         |                                             |
| Find and remove source of bad smell                 | 5     | 2    | 4        |4     | 10      |                                             |
| Find better coffee vendors                          | 4     | 2    | 6        |3     | 5       |                                             |
| Buy smart component for roaster                     | 3     | 5    | 2        |3     |         | Build in-house roasting notification system |
| Introduce a periodical suggestion survey for treats | 3     | 2    | 6        |1     |         |                                             |
| Buy a more modern sign                              | 3     | 3    | 1        |1     |         |                                             |
| Contact a designer to re-think the front            | 5     | 5    | 6        |3     |         |                                             |
| Buy beds for powernaps                              | 1     | 3    | 1        |1     |         |                                             |
| Import treats from France                           | 2     | 4    | 2        |2     |         |                                             |
| Build in-house roasting notification system         | 3     | 5    | 6        |5     |         | Buy smart component for roaster             |


### Example

```text
$ cat projects.csv
Project,Value,Cost,Duration,Rigging,Alternatives
Buy a better espresso machine,5,4,2,9,
Buy ambient parfume for the back,1,1,1,,
Find and remove source of bad smell,5,2,4,10,
Find better coffee vendors,4,2,6,5,
Buy smart component for roaster,3,5,2,,Build in-house roasting notification system
Introduce a periodical suggestion survey for treats,3,2,6,,
Buy a more modern sign,3,3,1,,
Contact a designer to re-think the front,5,5,6,,
Buy beds for powernaps,1,3,1,,
Import treats from France,2,4,2,,
Build in-house roasting notification system,3,5,6,,Buy smart component for roaster

$ dumbpm prioritize projects.csv
01 Buy ambient parfume for the back
02 Buy a more modern sign
03 Find and remove source of bad smell
04 Buy a better espresso machine
05 Find better coffee vendors
06 Buy beds for powernaps
07 Buy smart component for roaster
08 Import treats from France
09 Introduce a periodical suggestion survey for treats
10 Contact a designer to re-think the front

$ dumbpm prioritize projects.csv --budget 10
01 Buy ambient parfume for the back
02 Buy a more modern sign
03 Find and remove source of bad smell
04 Buy a better espresso machine
```

## Estimate project duration without historical data

Giving a list of tasks or milestones the project can be broken into and (best case, expected, worst case) estimates for the duration of such tasks, it outputs an estimate of the project duration in the form of a probability distribution (median, variance, percentiles). You can use these numbers to formulate guesstimates like "I am 75% confident that we will complete the project in 38 weeks". Instead of using a unit of time (e.g. days, weeks), you can instead specify story points for each tasks and so estimate the project size in story point instead of its duration.

The estimation is based on a [Monte Carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_method) of the following equation: `project_duration = sum(duration, over=tasks)`. Tasks duration for each iteration are derived from a [modified-PERT distribution](https://en.wikipedia.org/wiki/PERT_distribution) interpolating the (best case, expected, worst case) estimates for the task. Pretty dumb, indeed.

The command is called `guesstimate` to highlight that the result of this method should be considered with lower confidence than the one produced by the `estimate` command, which is based on historical data. You can switch to `estimate` after you conclude a few sprints, while relying on `guesstimate` for the initial estimates during the planning period.

If it is taking too long to perform the estimation on your computer, set `--simulations` to something lower than `10000`.

```bash
$ dumbpm guesstimate --help
usage: dumbpm guesstimate [-h] [--simulations [SIMULATIONS]] filename

positional arguments:
  filename              CSV file with tasks estimates

optional arguments:
  -h, --help            show this help message and exit
  --simulations [SIMULATIONS]
                        Number of simulations to run
```

### Input format

Estimates for tasks or milestones have to be defined in a CSV file with the following structure:

- `Task`: [required] name of the task (`Milestone` works as header, too)
- `Best`: [required] best case estimate for the task duration
- `Expected`: [required] most likely estimate for the task duration
- `Worst`: [required] worst case estimate for the task duration


| Task   | Best | Expected | Worst |
|--------|------|----------|-------|
| Task A | 5    | 10       | 20    |
| Task B | 6    | 12       | 40    |
| Task C | 1    | 13       | 24    |
| Task D | 10   | 13       | 15    |
| Task E | 5    | 7        | 12    |
| Task F | 12   | 25       | 34    |

### Example

```text
$ cat tasks.csv
Task,Best,Expected,Worst
Task A,5,10,20
Task B,6,12,40
Task C,1,13,24
Task D,10,13,15
Task E,5,7,12
Task F,12,25,34

$ dumbpm guesstimate tasks.csv
            Duration
count   10000.000000
mean        7.761430
std         0.993793
min         5.000000
50%         8.000000
5%         8.000000
90%         9.000000
99%        10.000000
max        12.000000
```

## Estimate project duration based on historical data

Giving a list of past sprint velocities and (optionally) a list of scope changes for the project in story points defined as below, it outputs an estimate of the project duration in the form of a probability distribution (median, variance, percentiles). You can use these numbers to formulate guesstimates like "I am 75% confident that we will complete the project in 38 weeks".

Please note that the estimate is measured in sprints, so you'll have to multiply that for the duration of your sprint and project that on your working calendar to account for holidays and anything else which could affect your schedule.

The estimation is based on a [Monte Carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_method) of the following inequation: `scope + sum(scope_change, over=sprints) <= sum(velocity, over=sprints)`. Pretty dumb, indeed.

By default, velocity and scope change for each iteration are picked at random following a [uniform probability distribution](https://en.wikipedia.org/wiki/Discrete_uniform_distribution) from the provided historical data. If `--normal` is specified, the input will be modelled as [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution) from which velocity and scope changes will be derived.

If it is taking too long to perform the estimation on your computer, set `--simulations` to something lower than `10000`.

```bash
$ dumbpm estimate --help
usage: dumbpm estimate [-h] [--normal] [--simulations [SIMULATIONS]] filename scope

positional arguments:
  filename              CSV file with velocity and scope change datapoints
  scope                 Remaining scope in story points for the project

optional arguments:
  -h, --help            show this help message and exit
  --normal              Use a normal distribution for the input data
  --simulations [SIMULATIONS]
                        Number of simulations to run
```

### Input format

Historical data has to be defined in a CSV file with the following structure:

- `Velocity`: [required] velocity for each past sprint
- `Change`: [optional] project scope change for each past sprint (zero and negative values are allowed)


| Velocity | Change |
|----------|--------|
| 17       | 5      |
| 19       | 1      |
| 10       | 0      |
| 12       | 0      |
| 21       | 1      |
|  7       | -3     |
| 15       | -2     |
| 12       | 5      |
| 12       | 0      |
| 14       | 2      |
| 18       | -4     |


### Example

```text
$ cat sprints.csv
Velocity,Change
17,5
19,1
10,0
12,0
21,1
7,-3
15,-2
12,5
12,0
14,2
18,-4

$ dumbpm estimate sprints.csv 100
            Duration
count   10000.000000
mean        7.761430
std         0.993793
min         5.000000
50%         8.000000
75%         8.000000
90%         9.000000
99%        10.000000
max        12.000000

$ dumbpm prioritize projects.csv 100 --normal
           Duration
count   10000.00000
mean        7.75637
std         0.99810
min         4.00000
50%         8.00000
75%         8.00000
90%         9.00000
99%        10.00000
max        13.00000
```
