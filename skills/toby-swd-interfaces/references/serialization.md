# Serialized contracts

Open this file when a message or parameter object crosses a queue, network call, worker process, native bridge, or disk file.

## Messages

Document the message format as the interface signature:

- the request and response types
- which field types survive serialization
- the delivery guarantees (at-least-once, at-most-once, ordering)

## Parameter objects

State in the comment for a serialized query or command object that it must not contain functions, live object references, or circular references.
