# Serialized contracts

This file has the interface rules for a message or a parameter object that crosses a serialization boundary. Open it when the value passes through one of these:

- a queue or a network call
- a worker or another process
- a native bridge
- a file on disk

## Messages

When two modules exchange messages, such as over a queue or between processes, the message format is the signature. That format includes these parts:

- the request and response types
- which values survive serialization
- the delivery guarantees

## Parameter objects

The comment for a query or command object that crosses a serialization boundary states that the object contains none of these:

- functions
- references to live objects
- circular references
