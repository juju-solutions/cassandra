#!/usr/bin/env python
"""
Simple script to parse cassandra-stress' transaction results
and reformat them as JSON for sending back to juju
"""
import sys
import subprocess
import json


def action_set(key, val):
    action_cmd = ['action-set']
    if isinstance(val, dict):
        for k, v in val.iteritems():
            action_set('%s.%s' % (key, k), v)
        return

    action_cmd.append('%s=%s' % (key, val))
    subprocess.check_call(action_cmd)


def parse_stress_output():
    """
    Parse the output from cassandra-stress and set the action results:

    total,interval_op_rate,interval_key_rate,latency/95th/99.9th,elapsed_time
    8197,819,819,0.2,93.5,1283.3,10
    10000,180,180,0.3,91.3,707.0,13
    END
    """

    # Throw away the header
    sys.stdin.readline()
    header = [
        'total',
        'interval_op_rate',
        'interval_key_rate',
        'latency',
        '95th',
        '99th',
        'elapsed'
    ]

    results = []
    for line in sys.stdin.readlines():
        fields = line.rstrip().split(',')
        if len(header) == len(fields):
            result = {}
            for idx, field in enumerate(header):
                result[field] = fields[idx]
            results.append(result)
    action_set("results.raw", json.dumps(results))


if __name__ == "__main__":
    parse_stress_output()
