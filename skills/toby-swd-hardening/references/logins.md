# Logins

This file covers limits on failed attempts at an endpoint that checks a password, a one-time code, or a reset token.

When the repo has no rate limiter, count failures per account and per IP. For each, store the time of the next allowed attempt, and reject earlier attempts with status 429 and a `Retry-After` header. Double the wait after each failure up to a cap, such as 15 minutes, so each lockout ends within that cap. Never sleep in the handler, because a sleeping request holds a worker, and guesses sent in parallel all finish after one sleep.

Read the client IP through the framework's trusted-proxy setting, such as Express `trust proxy` or Rails `request.remote_ip`. Never count attempts by the proxy's address or the first `X-Forwarded-For` value.
