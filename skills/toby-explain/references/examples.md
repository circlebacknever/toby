# Worked examples

Each answer starts with the point, then walks one concrete case. Don't reuse the wording of these examples.

## New concept without code shown yet

The user asks what a function is in mathematics, and hasn't shown any code or equation yet.

A function is a rule that gives each input exactly one output. `f(x) = x²` sends both 3 and −3 to 9, which the rule allows because two inputs can share an output. The circle `x² + y² = 1` is not a function, because the single input `x = 0` gives two outputs, `y = 1` and `y = −1`. To test any rule, pick one input and count its outputs.

## Design choice mid-task

The user asks why `RateLimiter.allow(client_id)` replaced the four-method bucket interface.

The old interface forced callers to fetch a bucket and refill it with the current time. Callers also had to check the token count and consume tokens in that exact order. Running those steps out of order broke the rate limiter. `allow(client_id)` runs all four steps inside the module, so callers ask one question and can't run the steps out of order.

## Verification step mid-task

The user asks what the migration check just proved.

Before the migration ran, `orders` rows created before May had `currency = NULL`, which crashed `Invoice.total()` when it formatted the price. The test seeded three pre-May rows with `NULL` currency, ran migration `0044`, and confirmed all three rows now have `currency = 'USD'` and `Invoice.total()` returns `"$12.00"`. Production row counts haven't been timed yet.
