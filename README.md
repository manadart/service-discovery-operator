# service-discovery-operator

## Description

A proof-of-concept for on operator that can spawn a process to watch its local
k8s cluster for events.

These events are dispatched back to the spawn charm via a custom event.

## Usage

- `charmcraft pack` this charm and deploy it.
- Deploy grafana-k8s and observe the status change indicating discovery.

