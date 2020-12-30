# dumbpm

[![PyPI version](https://badge.fury.io/py/dumbpm.svg)](https://badge.fury.io/py/dumbpm)
[![Continuous Integration](https://github.com/poros/dumbpm/workflows/Continuous%20Integration/badge.svg)](https://github.com/poros/dumbpm/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A pretty dumb PM.

At the moment it only does projects prioritization: it is pretty dumb, indeed.

The whole philosophy behind `dumbpm` is that PMs (project managers, program managers,product managers, people managers, pokemon masters, etc.) all do some tasks that could use some automation, but at the same time this automation should be as dumb as possible. There are so many changing factors that influence such tasks that you better hire a PM (or a team of researchers to do the automation) to do the clever stuff, not a random software on the internet. In addition, if we keep it dumb, people can just read the code and understand what is going on, if they really want to.

If you have any suggestions for something (but nothing clever!) that you would like `dumbpm` to do for you, open an issue and let me know.

## Prioritization

Giving a table of projetcs defined as below, it outputs a list of projects in order of priority within the optionally specified budget (prioritization as "data problem").

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
