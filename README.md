# dumbpm

[![GitHub version](https://badge.fury.io/gh/poros%2Fdumbpm.svg)](https://badge.fury.io/gh/poros%2Fdumbpm)
[![Build Status](https://travis-ci.org/poros/dumbpm.svg?branch=master)](https://travis-ci.org/poros/dumbpm)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A pretty dumb PM.

At the moment it only does projects prioritization: it is pretty dumb, indeed.

The whole philosophy behind `dumbpm` is that PMs (project managers, product managers, people managers, pokemon masters, etc.) all do some tasks that could use some automation, but at the same time this automation should be as dumb as possible. There are so many changing factors that influence such tasks that you better hire a PM (or a team of researchers to do the automation) to do the clever stuff, not a random software on the internet. In addition, if we keep it dumb, people can just read the code and understand what is going on, if they really want.

If you have any suggestions for something (but nothing clever!) that you would like dumbpm to do for you, open an issue and let me know.

## Prioritization

Giving a table of projetcs defined as below, it outputs a list of projects in order of priority within the optionally specified budget (prioritization as "data problem").

The prioritized list is modelled as the exact solution of a [Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem) with the following value function: `norm(value) / ((norm(cost) * norm(duration)) + norm(rigging)`. Pretty dumb, indeed.

```bash
$ dumbpm prioritize --help
usage: dumbpm prioritize [-h] [--budget [BUDGET]] filename

positional arguments:
  filename           CSV file with projects definition

optional arguments:
  -h, --help         show this help message and exit
  --budget [BUDGET]  Max budget allowed
```

### Projects format

Project definition happens in a CSV file with the following structure:

- `Project`: name of the project
- `Value`: value of the project
- `Cost`: cost of the project
- `Duration`: duration of the project expressed in unit of times
- `Rigging`: arbitrary value used to rig the result (yay, cheating!); the highest the more likely the project to be prioritized
- `Alternative`: comma separated list of projects that are incompatible with this one (e.g.; make lunch vs buy lunch)

Any field which is not specified, will be filled with 0.

There is a bit of slack on the headers of the columns (e.g.; Project, Projects, project, etc. are all alright). Notable mentions: rig and rigging both work; same for alts and alternatives; PQ can be used instead of cost if that's your thing.


| Project                                             | Value | Cost | Duration | Rigging | Alternatives                                |
|-----------------------------------------------------|-------|------|----------|---------|---------------------------------------------|
| Buy a better espresso machine                       | 5     | 4    | 2        | 9       |                                             |
| Buy ambient parfume for the back                    | 1     | 1    | 1        |         |                                             |
| Find and remove source of bad smell                 | 5     | 2    | 4        | 10      |                                             |
| Find better coffee vendors                          | 4     | 2    | 6        | 5       |                                             |
| Buy smart component for roaster                     | 3     | 5    | 2        |         | Build in-house roasting notification system |
| Introduce a periodical suggestion survey for treats | 3     | 2    | 6        |         |                                             |
| Buy a more modern sign                              | 3     | 3    | 1        |         |                                             |
| Contact a designer to re-think the front            | 5     | 5    | 6        |         |                                             |
| Buy beds for powernaps                              | 1     | 3    | 1        |         |                                             |
| Import treats from France                           | 2     | 4    | 2        |         |                                             |
| Build in-house roasting notification system         | 3     | 5    | 6        |         | Buy smart component for roaster             |



### Example

```bash
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
