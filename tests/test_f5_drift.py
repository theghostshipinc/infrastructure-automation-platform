from python.drift.f5 import compare_collection, compare_snapshots, has_drift


def test_detects_added_object():
    before = [
        {
            "full_path": "/Common/web01",
            "address": "10.10.11.10",
        }
    ]

    after = [
        {
            "full_path": "/Common/web01",
            "address": "10.10.11.10",
        },
        {
            "full_path": "/Common/web02",
            "address": "10.10.11.11",
        },
    ]

    result = compare_collection(before, after)

    assert result["added"] == ["/Common/web02"]
    assert result["removed"] == []
    assert result["modified"] == []


def test_detects_removed_object():
    before = [
        {
            "full_path": "/Common/web01",
            "address": "10.10.11.10",
        }
    ]

    after = []

    result = compare_collection(before, after)

    assert result["added"] == []
    assert result["removed"] == ["/Common/web01"]
    assert result["modified"] == []


def test_detects_modified_object():
    before = [
        {
            "full_path": "/Common/pool_web",
            "lb_method": "round-robin",
        }
    ]

    after = [
        {
            "full_path": "/Common/pool_web",
            "lb_method": "least-connections-member",
        }
    ]

    result = compare_collection(before, after)

    assert result["added"] == []
    assert result["removed"] == []
    assert len(result["modified"]) == 1
    assert result["modified"][0]["object"] == "/Common/pool_web"


def test_no_drift_when_snapshots_match():
    snapshot = {
        "metadata": {
            "inventory_hostname": "F5-01",
        },
        "nodes": [
            {
                "full_path": "/Common/web01",
                "address": "10.10.11.10",
            }
        ],
    }

    result = compare_snapshots(snapshot, snapshot)

    assert has_drift(result) is False


def test_drift_when_snapshot_changes():
    before = {
        "metadata": {
            "inventory_hostname": "F5-01",
        },
        "virtual_servers": [],
    }

    after = {
        "metadata": {
            "inventory_hostname": "F5-01",
        },
        "virtual_servers": [
            {
                "full_path": "/Common/vs_web",
                "destination": "10.10.12.100:80",
            }
        ],
    }

    result = compare_snapshots(before, after)

    assert has_drift(result) is True
    assert result["collections"]["virtual_servers"]["added"] == [
        "/Common/vs_web"
    ]