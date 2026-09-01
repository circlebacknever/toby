# Replace the Growing Conditional

A `switch` or `if` chain is a design smell in two forms. The first takes a new arm every time the domain gains a case. The second is the same branch decision copied across call sites. Both are a module that is not closed to modification: the next case edits shared code, or several files at once.

A conditional that has not changed in a year is not this smell. This file is for the ones that keep growing.

The ladder runs lightest first. Stop at the first rung that fits. The code is illustrative and the reasoning transfers.

---

## Rung 1 — Remove the branch

New requirement: deleted users render as "[deleted]".

```python
def display_name(user):
    if user.deleted:
        return "[deleted]"
    return f"{user.first} {user.last}"
```

Every caller that formats a name now depends on this branch. The next user state — banned, system, unverified — adds another arm here or a second copy elsewhere. The concept "deleted" has leaked into name formatting.

Move the answer onto the type:

```python
def display_name(user):
    return user.display_label()

class User:
    def display_label(self):
        if self.deleted:
            return "[deleted]"
        return f"{self.first} {self.last}"
```

The branch still exists. It lives once, next to the data it reads, and callers do not see it. New states change one method.

The same move removes null checks. A null object that responds to every call the real one does lets the common path run with no `if x is None`.

---

## Rung 2 — Data-driven dispatch

Branches that select a small behavior by a tag value become a lookup map.

```tsx
function renderPreview(file: FileMeta): ReactNode {
  if (file.kind === "pdf") return <PdfPreview file={file} />;
  if (file.kind === "csv") return <CsvPreview file={file} />;
  if (file.kind === "image") return <ImagePreview file={file} />;
  return <UnknownPreview file={file} />;
}
```

Every new file kind edits this function. Replace it with a map:

```tsx
const PREVIEWS: Record<FileKind, FC<{ file: FileMeta }>> = {
  pdf: PdfPreview,
  csv: CsvPreview,
  image: ImagePreview,
};

function renderPreview(file: FileMeta): ReactNode {
  const Preview = PREVIEWS[file.kind] ?? UnknownPreview;
  return <Preview file={file} />;
}
```

Adding a kind is one entry. `Record<FileKind, …>` makes a missing entry a compile error, so the set stays complete. No pattern, no class.

Keep it to one map. Two maps that switch on the same tag is the leak this rung removes.

---

## Rung 3 — Discriminated union with an exhaustive switch

When the branches read different fields, the map does not fit. Keep the switch and let the type close it.

```ts
type DomainEvent =
  | { kind: "click"; x: number; y: number }
  | { kind: "key"; code: string }
  | { kind: "paste"; text: string };

function assertNever(x: never): never {
  throw new Error(`unhandled: ${JSON.stringify(x)}`);
}

function reduce(state: State, e: DomainEvent): State {
  switch (e.kind) {
    case "click": return placeMarker(state, e.x, e.y);
    case "key":   return applyKey(state, e.code);
    case "paste": return insertText(state, e.text);
    default:      return assertNever(e);
  }
}
```

Add a variant to `DomainEvent` and the `default` arm stops compiling until the new `case` is written. The switch is a single dispatch point, and the compiler holds it complete. No one can forget to extend it.

Use this over rung 2 when each branch reads different fields. Use rung 2 when the branches differ only in which function runs.

---

## Rung 4 — Polymorphism

When each case owns behavior, private state, or its own dependencies, a map of functions is the wrong container. Give each case an object behind a shared interface.

```ts
interface Gateway {
  charge(payment: Payment): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

class StripeGateway implements Gateway {
  // owns: the Stripe SDK client, the API key, a retry policy, an idempotency cache
}

class LegacyBankGateway implements Gateway {
  // owns: a SOAP client, a client cert, a different retry policy, a nightly batch file
}

const gateway: Gateway = GATEWAYS[config.gatewayName];
```

Each implementation is a module. Its state and dependencies stay inside it. `strategy/references/examples.md` reaches this same design for the two-gateway task.

The cost is real: one interface to keep stable, one class per case, a selection site. It earns that cost when the case set is open and each case holds state the others do not share. Three one-line branches over a closed set do not qualify. That is rung 2.

---

## Rung 5 — Registry

When a new case must be addable without editing any central file, the selection site itself has to be open. Each implementation registers itself.

```ts
const HANDLERS = new Map<string, MessageHandler>();

export function registerHandler(type: string, handler: MessageHandler): void {
  HANDLERS.set(type, handler);
}

export function dispatch(message: InboundMessage): Promise<void> {
  const handler = HANDLERS.get(message.type);
  if (!handler) throw new UnknownMessageType(message.type);
  return handler.handle(message);
}
```

Each handler module calls `registerHandler` at load. The dispatcher never names them. This fits a plugin API, or a set of adapters loaded by config at boot.

It is the heaviest rung. The registration is indirection a reader has to trace, and load order becomes something you can get wrong. Reserve it for a surface that is open to code you do not control.

---

## React and React Native forms

- **Status to component.** `Record<Status, FC>` over a `switch (status)` in render. The map sits above the component or in a sibling module.
- **Variant prop that grew.** A `<Button variant="…">` whose `variant` gains values every quarter is rung 2 wearing a prop. Move to compound components with `children`, or a map from variant to a style object.
- **Field type to input.** A form that renders from a schema maps `field.type` to a component. A `switch (field.type)` inside JSX is the smell.
- **Behavior split from presentation.** A headless hook owns the state machine and each screen composes it. `references/web.md` Example 4 shows it in full.
- **Platform branch.** `Platform.OS === "ios"` checks scattered through components are the copied-decision case. Use `Platform.select({ ios, android })` at one module boundary, or `Foo.ios.tsx` and `Foo.android.tsx` files where the bundler picks the file and no branch runs.

## Backend forms

- **Adapter interface.** `Gateway`, `StorageDriver`, `Notifier`: one interface, one implementation per provider, selection from config at the composition root.
- **Handler map by message type.** Rung 2 for a closed set of message types. Rung 5 when handlers ship independently.
- **Wire discriminated union.** A payload with a `type` tag is validated once at the edge, then dispatched with rung 3 so the compiler tracks every case.

---

## Cheat sheet

| What you see | Rung |
|---|---|
| Branch exists because the caller lacks a value the type could hold | 1 — move it onto the type |
| Branch picks which function runs, bodies are one-liners, closed set | 2 — lookup map |
| Branches read different fields, set is closed | 3 — discriminated union with `assertNever` |
| Each case owns a client, a policy, or private state; set is open | 4 — interface with implementations |
| New cases ship in code you do not control | 5 — registry |
| Conditional has been stable for a year | none — leave it |
