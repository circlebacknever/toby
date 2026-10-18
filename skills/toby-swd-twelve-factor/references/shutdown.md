# Shutdown

This file gives the `SIGTERM` shutdown sequence and health-check rules for services behind a load balancer or orchestrator.

On `SIGTERM`, complete these steps within a drain timeout set shorter than the platform's `SIGKILL` grace period (such as 25 seconds inside Kubernetes' 30-second default):

1. Mark the readiness check failing so the load balancer stops routing new requests.
2. Keep accepting requests during the load balancer's health-check propagation window, then stop accepting new connections.
3. Finish in-flight requests, flush logs and telemetry, and close database and client pools.
4. In a queue consumer, stop polling and release any unfinished messages back to the broker before exiting.

Liveness checks verify only that the process loop is responsive, while readiness checks verify that startup finished and shutdown hasn't started. Never fail readiness or liveness on a shared downstream dependency such as the database, because failing health checks across all instances takes the whole service offline during a brief database blip.
