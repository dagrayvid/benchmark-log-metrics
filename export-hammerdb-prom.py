#!/usr/bin/python3

from prometheus_client import start_http_server, Gauge
import time
import os
import re
import random

print("Starting app")

def extract_tpm(hammerdb_log):
    tpm_list = []
    for line in hammerdb_log:
        index = line.find("TPM:")
        if(index != -1):
            val = re.search(r"(?:\d*\.\d+|\d+)", line)
            tpm_list.append(val.group())
            #print(val.group())

    print(tpm_list[len(tpm_list) - 1])
    return float(tpm_list[len(tpm_list) - 1])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8449)

    # Create a metric to track time spent and requests made.
    tpm = Gauge('hammerdb_tpm', 'TPM result from hammerdb-benchmark-workload-* pod')
    test_gauge = Gauge('hammerdb_test_gauge', 'Random number used as test for metrics reporting')

    # Generate some requests.
    while True:
        print("Checking logs")
        # Run oc command to get pod logs
        stream = os.popen('oc get pods -n benchmark-operator | grep "hammerdb-benchmark-.*-workload" | awk \'{print $1}\'')
        pod_name = stream.read()

        stream = os.popen("oc logs -n benchmark-operator pod/{}".format(pod_name))
        pod_logs = stream.read()

        # extract TPM from pod logs
        latest_tpm = extract_tpm(pod_logs.split("\n"))

        # set metric
        print("Setting tpm to: {}".format(latest_tpm))
        tpm.set(latest_tpm)
        test_gauge.set(random.randrange(0,5))
        time.sleep(30)

