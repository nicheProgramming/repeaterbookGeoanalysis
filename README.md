# :satellite: Repeaterbook Geoanalysis

LICENSE: GNU aGPL v3

[//]: # (reference for GitHub Emojis: https://gist.github.com/rxaviers/7360908)

## :round_pushpin: About

This script is being designed to be given a source city and a radius around the city in miles (25 mile increments ATM). ALl cities in this radius will be queried in Repeaterbook. The results will be used to display statistics of mode and band use and potentially other statistics of interest. Please feel free to share any ideas, bugs, or other issues you may encounter.

## :warning: Limitations

Current limitations include:

- Repeaterbook will not return ATV mode repeaters via their api
- The HERE api will only return up to 100 results. This means larger radiuses are likely to start missing information. No current workaround known.

## :bulb: Dev Environment Prerequisites

Environment tested and working on Ubuntu Linux (22.04 LTS)

1. pyenv (using 3.11 shell)

## :computer: Dev Environment Setup

Run the following to set up your dev environment from the project directory to work on this script:

```bash
    pyenv install 3.11
    pyenv shell 3.11
    pyenv exec pip install -r requirements.txt
```
