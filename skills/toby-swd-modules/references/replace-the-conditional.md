# Replace the Growing Conditional

---

## Option 1 — Remove the branch

A new requirement says that deleted users render as "[deleted]".

```python
def display_name(user):
    if user.deleted:
        return "[deleted]"
    return f"{user.first} {user.last}"
```

Every caller that formats a name now depends on this branch. Each new user state, such as banned, system, or unverified, needs another arm here or a second copy elsewhere. The concept "deleted" has leaked into name formatting.

Move the branch onto the `User` type:

```python
def display_name(user):
    return user.display_label()

class User:
    def display_label(self):
        if self.deleted:
            return "[deleted]"
        return f"{self.first} {self.last}"
```

The branch still exists, but only once, next to the data it reads, so callers do not see it. Adding a state changes one method.

The same move removes null checks. A null object that responds to every call the real one does lets the common path run with no `if x is None`.

---

## Option 2 — Data-driven dispatch

Replace branches that select a small behavior by a tag value with a lookup map.

```tsx
function renderPreview(file: FileMeta): ReactNode {
  if (file.kind === "pdf") return <PdfPreview file={file} />;
  if (file.kind === "csv") return <CsvPreview file={file} />;
  if (file.kind === "image") return <ImagePreview file={file} />;
  return <UnknownPreview file={file} />;
}
```

Every new file kind requires an edit to this function. Replace it with a map:

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

Adding a kind means adding one entry. `Record<FileKind, …>` makes a missing entry a compile error, so the set stays complete. The map needs no design pattern and no class.

Keep it to one map. Two maps keyed on the same tag repeat the leak that one map removes.

---

## Option 3 — Discriminated union with an exhaustive switch

When the branches read different fields, the map does not fit. Keep the switch and let the type make it exhaustive.

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

Add a variant to `DomainEvent` and the `default` arm stops compiling until the new `case` is written. The switch is a single dispatch point that the compiler keeps complete. The compiler reports any `case` a developer forgets to add.

Use this over option 2 when each branch reads different fields. Use option 2 when the branches differ only in which function runs.

---

## Option 4 — Polymorphism

When each case has its own behavior, private state, or dependencies, a map of functions is the wrong container. Give each case an object behind a shared interface.

```ts
interface Gateway {
  charge(payment: Payment): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

class StripeGateway implements Gateway {
  // stores the Stripe SDK client, the API key, a retry policy, and an idempotency cache
}

class LegacyBankGateway implements Gateway {
  // stores a SOAP client, a client cert, a different retry policy, and a nightly batch file
}

const gateway: Gateway = GATEWAYS[config.gatewayName];
```

Each implementation is its own module, with its state and dependencies inside it.

The cost is one interface to keep stable, one class per case, and a selection site. Polymorphism is worth that cost when the case set is open and each case holds state the others do not share. Three one-line branches over a closed set do not qualify, because they belong on option 2.

---

## Option 5 — Registry

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

Each handler module calls `registerHandler` at load, so the dispatcher never imports them. This fits a plugin API, or a set of adapters loaded by config at boot.

It is the most complex option. The registration adds indirection that a reader has to trace. Load order also becomes something you can get wrong. Reserve it for an interface that is open to code you do not control.

---

## React and React Native forms

- **Status to component.** Replace a `switch (status)` in render with a `Record<Status, FC>`. Put the map above the component or in a sibling module.
- **Variant prop that grew.** A `<Button variant="…">` whose `variant` gains values every quarter is option 2, with the tag passed as a prop. Move to compound components with `children`, or a map from variant to a style object.
- **Field type to input.** A form that renders from a schema maps `field.type` to a component. A `switch (field.type)` inside JSX is the smell.
- **Behavior split from presentation.** Each screen composes a headless hook that contains the state machine.
- **Platform branch.** `Platform.OS === "ios"` checks scattered through components are the copied-decision case. Use `Platform.select({ ios, android })` at one module boundary, or `Foo.ios.tsx` and `Foo.android.tsx` files where the bundler picks the file, so the code has no branch.

## Backend forms

- **Adapter interface.** `Gateway`, `StorageDriver`, and `Notifier` each have one interface and one implementation per provider. The composition root selects the implementation from config.
- **Handler map by message type.** Use option 2 for a closed set of message types, and option 5 when handlers ship independently.
- **Wire discriminated union.** A payload with a `type` tag is validated once at the edge, then dispatched with option 3 so the compiler tracks every case.
