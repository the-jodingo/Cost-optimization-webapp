"""Resource cost optimizer - fractional knapsack.

Given a fixed budget and a list of resources (each with a cost and a value),
allocate budget across resources to maximise total value.

The greedy by value-per-dollar strategy is provably optimal for the
*continuous* (fractional) knapsack problem.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass
class Resource:
    """A purchasable resource with a unit cost and a unit value."""

    name: str
    cost: float
    value: float

    @property
    def ratio(self) -> float:
        """Value per unit cost. Zero cost is treated as infinitely good."""
        return float("inf") if self.cost <= 0 else self.value / self.cost


def optimize(budget: float, resources: list[Resource]) -> dict:
    """Allocate `budget` across `resources` to maximise total value.

    Returns a dict with per-resource allocations, total spend and total value.
    """
    if budget < 0:
        raise ValueError("budget must be non-negative")

    remaining = float(budget)
    allocations = []
    total_value = 0.0
    total_cost = 0.0

    for r in sorted(resources, key=lambda x: x.ratio, reverse=True):
        if remaining <= 0:
            break
        if r.cost <= 0:
            fraction = 1.0
        else:
            fraction = min(1.0, remaining / r.cost)
        spend = fraction * r.cost
        value = fraction * r.value
        remaining -= spend
        total_cost += spend
        total_value += value
        allocations.append(
            {
                "name": r.name,
                "cost": r.cost,
                "value": r.value,
                "fraction": fraction,
                "spend": spend,
                "value_gained": value,
            }
        )

    return {
        "allocations": allocations,
        "total_cost": total_cost,
        "total_value": total_value,
        "remaining": remaining,
    }


def parse_form(form) -> tuple[float, list[Resource]]:
    """Build (budget, resources) from submitted form data."""
    budget = float(form.get("budget", 0) or 0)
    names = form.getlist("item_name")
    costs = form.getlist("item_cost")
    values = form.getlist("item_value")

    resources = []
    for name, cost, value in zip(names, costs, values):
        if not name.strip():
            continue
        resources.append(Resource(name.strip(), float(cost or 0), float(value or 0)))
    return budget, resources


@app.get("/health")
def health():
    """Liveness probe."""
    return {"status": "healthy", "service": "cost-optimizer"}


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the form, and the optimisation result on POST."""
    result = None
    budget = None
    error = None

    if request.method == "POST":
        try:
            budget, resources = parse_form(request.form)
            if not resources:
                error = "Add at least one resource."
            else:
                result = optimize(budget, resources)
        except (TypeError, ValueError) as exc:
            error = f"Invalid input: {exc}"

    return render_template("index.html", result=result, budget=budget, error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
