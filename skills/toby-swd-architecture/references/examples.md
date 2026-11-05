# Default structure examples

This file shows the default structure from SKILL.md in two frameworks, one with an ORM model and one with a webhook.

## A renewal limit in Rails

```ruby
class Loan < ApplicationRecord
  class LimitReached < StandardError; end
  MAX_RENEWALS = 2

  def renew!
    with_lock do
      raise LimitReached if renewals >= MAX_RENEWALS
      update!(due_on: due_on + 14.days, renewals: renewals + 1)
    end
  end
end

# LoansController
def renew
  started = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  outcome = "failed"
  loan = current_member.loans.find(params[:id])
  loan.renew!
  outcome = "renewed"
  render json: loan
rescue Loan::LimitReached
  outcome = "limit_reached"
  head :unprocessable_entity
ensure
  elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - started) * 1000
  Rails.logger.info("loan.renewal loan_id=#{loan&.id} outcome=#{outcome} duration_ms=#{elapsed.round}")
end
```

The controller checks permission by finding the loan through the member. The admin screen and the overdue job call `renew!` too, so they get the same limit. The summary reports renewal, rejection, or failure with its duration. The framework's error handler records an unexpected exception and its cause once.

`with_lock` reloads the row with `SELECT ... FOR UPDATE` inside a transaction. A second renewal sent at the same moment waits for the first, then checks the limit against the new count.

## A carrier webhook in Express

Check a webhook's signature on the raw request bytes before you parse them.

```js
router.post("/webhooks/carrier", express.raw({ type: "application/json" }), async (req, res, next) => {
  const started = performance.now();
  let outcome = "failed";
  let trackingId;
  try {
    if (!carrier.verify(req.body, req.get("X-Carrier-Signature"))) {
      outcome = "invalid_signature";
      return res.sendStatus(401);
    }
    const delivery = carrier.parseDelivery(req.body);
    trackingId = delivery.trackingId;
    await shipments.markDelivered(delivery);
    outcome = "delivered";
    res.sendStatus(204);
  } catch (error) {
    next(error);
  } finally {
    log.info({
      tracking_id: trackingId,
      request_id: req.id,
      outcome,
      duration_ms: performance.now() - started,
    }, "shipment.delivery_processed");
  }
});
```

An `express.json()` parser mounted before this route parses the body first, so `req.body` no longer contains the bytes the signature covers. `parseDelivery` converts the carrier's payload into the repo's own fields. The `shipments` module is the only code that writes the shipments table. The established error handler receives `next(error)` and logs the cause once. The summary event omits the raw webhook payload and signature.
