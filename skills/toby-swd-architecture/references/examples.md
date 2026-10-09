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
  loan = current_member.loans.find(params[:id])
  loan.renew!
  render json: loan
rescue Loan::LimitReached
  head :unprocessable_entity
end
```

The controller checks permission by finding the loan through the member. The admin screen and the overdue job call `renew!` too, so they get the same limit.

`with_lock` reloads the row with `SELECT ... FOR UPDATE` inside a transaction. A second renewal sent at the same moment waits for the first, then checks the limit against the new count.

## A carrier webhook in Express

Check a webhook's signature on the raw request bytes before you parse them.

```js
router.post("/webhooks/carrier", express.raw({ type: "application/json" }), async (req, res) => {
  if (!carrier.verify(req.body, req.get("X-Carrier-Signature"))) return res.sendStatus(401);
  const delivery = carrier.parseDelivery(req.body); // { trackingId, deliveredAt }
  await shipments.markDelivered(delivery); // the status change and its guard
  log.info({ trackingId: delivery.trackingId }, "shipment.delivered");
  res.sendStatus(204);
});
```

An `express.json()` parser mounted before this route parses the body first, so `req.body` no longer holds the bytes the signature covers. `parseDelivery` converts the carrier's payload into the repo's own fields. The `shipments` module is the only code that writes the shipments table.
