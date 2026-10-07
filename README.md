[![CI](https://github.com/the-jodingo/Cost-optimization-webapp/actions/workflows/ci.yml/badge.svg)](https://github.com/the-jodingo/Cost-optimization-webapp/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Algorithm](https://img.shields.io/badge/algorithm-fractional%20knapsack-blueviolet)](https://en.wikipedia.org/wiki/Continuous_knapsack_problem)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Cost Optimization Web App

A Flask web app that solves the **fractional knapsack problem**: given a fixed
budget and a list of resources (each with a unit cost and a unit value), it
allocates the budget to maximise total value.

## Table of contents

- [The problem](#the-problem)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Testing and CI](#testing-and-ci)
- [Project structure](#project-structure)
- [Accessibility](#accessibility)
- [License](#license)

## The problem

| | |
|---|---|
| **Goal** | Maximise total value within a fixed budget |
| **Input** | A budget, plus resources with a unit cost and unit value |
| **Output** | How much of each resource to take, total spend, total value |
| **Algorithm** | Greedy by value-per-unit-cost |

## Requirements

- Python 3.11 or newer

## Quick start

```bash
git clone https://github.com/the-jodingo/Cost-optimization-webapp.git
cd Cost-optimization-webapp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

Open <http://127.0.0.1:5000>.

## Usage

1. Enter your total budget.
2. Add one or more resources — a name, a unit cost, and a unit value.
3. Press **Optimize**.

The result table shows, per resource, the percentage taken, the spend, and the
value gained, followed by totals.

### Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | The form |
| `POST` | `/` | Runs the optimisation and renders the result |
| `GET` | `/health` | `{"status": "healthy", "service": "cost-optimizer"}` |

## How it works

`optimize()` sorts resources by value-per-unit-cost descending, then takes as
much as the remaining budget allows from each in turn, taking a fraction of the
last one if the budget runs out mid-resource.

**Why greedy is correct here:** for the *continuous* (fractional) knapsack, the
greedy-by-ratio strategy is provably optimal. For the 0/1 variant — where you
must take a resource whole or not at all — greedy is only an approximation and
the exact answer needs dynamic programming.

## Testing and CI

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the suite on Python 3.11 and 3.12 for every push and PR.

## Project structure

```
Cost-optimization-webapp/
├── app.py                  # Flask app + optimise()
├── templates/index.html    # Front end
├── tests/test_app.py       # pytest suite
├── requirements.txt
├── requirements-dev.txt
└── .github/workflows/ci.yml
```

## Accessibility

The interface is built to WCAG 2.1 AA basics:

- semantic landmarks (`main`), headings in order, and a real `<table>` with
  `<caption>` and `<th scope="col">`
- every input has an associated `<label>`
- visible focus outlines (`:focus-visible`), 3 px, high contrast
- errors announced via `role="alert"`
- body text meets AA contrast; layout is usable down to 320 px wide

## License

[MIT](LICENSE) © Joash Odingo
