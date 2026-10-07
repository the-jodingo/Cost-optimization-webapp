"""Tests for the cost optimizer."""

import pytest

from app import Resource, app, optimize


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_takes_best_ratio_first():
    # B costs half as much per unit of value as A
    res = [Resource("A", cost=10, value=10), Resource("B", cost=10, value=20)]
    out = optimize(10, res)
    assert [a["name"] for a in out["allocations"]] == ["B"]
    assert out["total_value"] == 20


def test_splits_when_budget_is_short():
    res = [Resource("A", cost=100, value=100)]
    out = optimize(25, res)
    assert out["allocations"][0]["fraction"] == pytest.approx(0.25)
    assert out["total_value"] == pytest.approx(25)
    assert out["remaining"] == pytest.approx(0)


def test_respects_budget():
    res = [Resource("A", cost=10, value=5), Resource("B", cost=10, value=9)]
    out = optimize(15, res)
    assert out["total_cost"] <= 15


def test_zero_budget_yields_nothing():
    out = optimize(0, [Resource("A", cost=10, value=5)])
    assert out["allocations"] == []
    assert out["total_value"] == 0


def test_negative_budget_rejected():
    with pytest.raises(ValueError):
        optimize(-1, [])


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "healthy"


def test_index_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Cost Optimizer" in r.data


def test_post_returns_allocation(client):
    r = client.post(
        "/",
        data={
            "budget": "100",
            "item_name": ["Server", "Storage"],
            "item_cost": ["60", "40"],
            "item_value": ["90", "50"],
        },
    )
    assert r.status_code == 200
    assert b"Total value" in r.data
