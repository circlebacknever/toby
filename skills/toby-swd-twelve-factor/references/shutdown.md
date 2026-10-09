# Shutdown

This file gives the shutdown steps and health checks for a service behind a load balancer or an orchestrator.

On `SIGTERM`, take these steps inside the platform's grace period, which is 30 seconds by default in Kubernetes:

1. Make the readiness check fail.
2. Keep serving until the load balancer stops sending requests, which takes its health-check interval times its failure threshold.
3. Stop taking new work, finish the work in flight, and close connections.
4. In a consumer, stop pulling and return each unfinished message to the queue.

Liveness reports that the process runs. Readiness reports that this instance has finished starting and is not shutting down. Readiness must not fail on a dependency every instance shares, such as the database. To check, send `SIGTERM` to a local run during a slow request, and confirm the request finishes.
