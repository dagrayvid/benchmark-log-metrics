FROM registry.redhat.io/ubi8/ubi:latest

# debug purposes only: curl, vim
RUN dnf install -y wget tar bash curl vim

RUN wget https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/stable/openshift-client-linux.tar.gz \
&& tar -xzvf openshift-client-linux.tar.gz -C /usr/local/bin

RUN dnf install -y python3 python3-pip && pip3 install prometheus-client

COPY export-hammerdb-prom.py /usr/local/bin/export-hammerdb-prom.py
