# Design note

This file has the rules for a design note written in chat. Open it when a user asks which design to pick, or when a report explains a design choice.

- Put the recommendation and its main reason in the first sentence, such as "Use an `audit_log` table, because the monthly report reads events by date."
- Describe each approach once, then compare them on the facts the user and the code give, one fact per sentence.
- Don't add a column, an index, a volume, or a cost that the request and the code don't show.
- State the fact behind each likely next change, such as "Finance asked for refund events in the same history."
