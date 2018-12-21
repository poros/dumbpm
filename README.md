# dumbpm

[![GitHub version](https://badge.fury.io/gh/poros%2Fdumbpm.svg)](https://badge.fury.io/gh/poros%2Fdumbpm)
[![Build Status](https://travis-ci.org/poros/dumbpm.svg?branch=master)](https://travis-ci.org/poros/dumbpm)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A pretty dumb PM.

At the moment only offers project prioritization, but it is indeed pretty dumb.

Project definition happens in a CSV file with the following structure:

- `Project`: name of the project
- `Value`: value of the project
- `Cost`: cost of the project
- `Duration`: duration of the project expressed in unit of times
- `Rigging`: arbitrary value used to rig the result; the highest the more likely the project to be prioritized

Any field which is not specified, will be filled with 0.

There is a bit of slack on the headers of the columns (e.g.; Project, Projects, project, etc. are all alright).


## Usage
```bash
$ dumbpm --help
usage: dumbpm [-h] {prioritize} ...

A very dumb PM

optional arguments:
  -h, --help    show this help message and exit

subcommands:
  {prioritize}
    prioritize  Prioritize projects in a very dumb way
```

```bash
$ dumbpm prioritize --help
usage: dumbpm prioritize [-h] [--budget [BUDGET]] filename

positional arguments:
  filename           CSV file with projects definition

optional arguments:
  -h, --help         show this help message and exit
  --budget [BUDGET]  Max budget allowed
```

## Example

```bash
$ cat projects.csv
Project,Value,Cost,Duration,Rigging
Buy a better espresso machine,5,4,2,9
Buy ambient parfume for the back,1,1,1,
Find and remove source of bad smell,5,2,4,10
Find better coffee vendors,4,2,6,5
Buy smart component for roaster,3,5,2,
Introduce a periodical suggestion survey for treats,3,2,6,
Buy a more modern sign,3,3,1,
Contact a designer to re-think the front,5,5,6,
Buy beds for powernaps,1,3,1,
Import treats from France,2,4,2,

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
11 Build in-house roasting notification system

$ dumbpm prioritize projects.csv --budget 10
01 Buy ambient parfume for the back
02 Buy a more modern sign
03 Find and remove source of bad smell
04 Buy a better espresso machine
```
