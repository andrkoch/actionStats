from .actionStats import actionStats

import json


def test_providedExampleTest():
    samples = [
        '{"action":"jump", "time":100}',
        '{"action":"run", "time":75}',
        '{"action":"jump", "time":200}',
    ]

    testActionStats = actionStats()
    for s in samples:
        ret = testActionStats.addAction(s)
        assert ret == True

    assert (
        testActionStats.getStats()
        == '[{"action": "jump", "avg": 150}, {"action": "run", "avg": 75}]'
    )


def test_BadInput():
    samples = [
        '{"action":"jump", "time":100}',
        '{"action":"run", "time":75}',
        '{"action":"jump", "time":200}',
    ]

    testActionStats = actionStats()

    # Add in the good samples
    for s in samples:
        ret = testActionStats.addAction(s)
        assert ret == True

    # Empty input
    assert testActionStats.addAction("") == False
    
    # Action wrong type
    assert testActionStats.addAction('{"action":1, "time":100}') == False
    # Time wrong type
    assert testActionStats.addAction('{"action":"jump", "time":"100"}') == False
    # Missing action
    assert testActionStats.addAction('{"sleep":"jump", "time":"100"}') == False
    # Missing time
    assert testActionStats.addAction('{"action":"jump", "var":"100"}') == False
    # key twice,
    assert testActionStats.addAction('{"action":"jump", "action":100}') == False
    # list instead of dict
    assert testActionStats.addAction("[]") == False
    # assert testActionStats.addAction( '{"action":"jump", "time":100}') == False
    # assert testActionStats.addAction( '{"action":"jump", "time":100}') == False

    # Ensure output includes only the good samples
    assert (
        testActionStats.getStats()
        == '[{"action": "jump", "avg": 150}, {"action": "run", "avg": 75}]'
    )
