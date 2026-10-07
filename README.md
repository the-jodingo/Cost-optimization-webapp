[![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-web%20app-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Algorithm](https://img.shields.io/badge/algorithm-fractional%20knapsack-blueviolet)](https://en.wikipedia.org/wiki/Continuous_knapsack_problem)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Cost Optimization Web App

A Flask web app that solves the **fractional knapsack problem**: given a fixed
budget and a list of resources (each with a cost and a value), it calculates how
much of each to take to maximise total value without exceeding the budget.

## The problem

| | |
|---|---|
| **Goal** | Maximise total value within a fixed budget |
| **Input** | A list of resources, each with a cost and a value |
| **Output** | The optimal allocation, total spend, and total value |
| **Algorithm** | Greedy by value-per-dollar (optimal for the *fractional* variant) |

## Setup

```bash
pip install flask
mkdir -p cost_optimizer/templates
```

Expected layout:

```
cost_optimizer/
├── app.py          # Flask backend
└── templates/
    └── index.html  # Frontend
```

```bash
python app.py
# open http://127.0.0.1:5000
```

## Running

Enter a budget and one or more resources (name, cost, value). The app returns a
table of allocations with the percentage taken from each resource, plus the
total cost and total value.

## Notes

- The greedy approach is **optimal** for the fractional knapsack. If you need
  the 0/1 variant (whole items only), it becomes a dynamic-programming problem
  and the greedy result is only an approximation.
- See `Cost.python` for the frontend template source.

## License

MIT
