# Replace the Growing Conditional

---

## Option 1. Move the branch onto the type

A new requirement says that deleted users render as `"[deleted]"`.

```python
def display_name(user):
    if user.deleted:
        return "[deleted]"
    return f"{user.first} {user.last}"
```

Every caller that formats a name now depends on this branch, and each new user state (banned, system, unverified) adds another branch. Move the branch onto `User`:

```python
def display_name(user):
    return user.display_label()

class User:
    def display_label(self):
        if self.deleted:
            return "[deleted]"
        return f"{self.first} {self.last}"
```

The branch now sits in one method next to the data it reads. You can remove repeated `None` checks the same way by returning a stand-in guest object with the same methods as `User`.

---

## Option 2. Data-driven dispatch

When each branch picks a small behavior based on one field, such as `file.kind`, replace the `if` chain with a lookup map:

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

Adding a file kind adds one map entry, and `Record<FileKind, ...>` makes a missing entry a compile error. When a second map on `kind` computes an icon, type it as `Record<FileKind, ...>` so the compiler checks both maps.

---

## Option 3. Tagged union with an exhaustive switch

When each branch reads different fields, use a tagged union and an exhaustive `switch`:

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

When you add a variant to `DomainEvent`, the `default` arm fails to compile until you handle the new `case`.

---

## Option 4. Polymorphism

When each case keeps its own private state or dependencies, give each case a class behind a shared interface:

```ts
interface Gateway {
  charge(payment: Payment): Promise<ChargeResult>;
  refund(chargeId: string): Promise<RefundResult>;
}

class StripeGateway implements Gateway {
  // stores the Stripe SDK client, API key, and retry policy
}

class LegacyBankGateway implements Gateway {
  // stores a SOAP client, client cert, and nightly batch file
}

const gateway: Gateway = GATEWAYS[config.gatewayName];
```

Use polymorphism when you keep adding cases that hold distinct state or clients, and use a lookup map (Option 2) for small stateless branches.

---

## Option 5. Registry

Use a runtime registry only when external plugins or independently loaded modules must add cases without editing a central file:

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

Each handler module calls `registerHandler` at startup, so the dispatcher never imports them. Because registration hides call targets and depends on module load order, reserve it for third-party plugins.

---

## Frontend examples

- **Status to component:** replace a `switch (status)` in render with a `Record<Status, FC>` lookup map.
- **Growing variant prop:** when `<Button variant="...">` gains variants every quarter, map `variant` to a style object or split into purpose-named components.
- **Schema form fields:** map `field.type` to an input component in a lookup object and keep the switch out of JSX.
- **Platform branches:** replace scattered `Platform.OS === "ios"` checks with `Platform.select({ ios, android })` in one module or `.ios.tsx` / `.android.tsx` files.

## Backend examples

- **Provider adapters:** give `Gateway`, `StorageDriver`, and `Notifier` one interface and one class per provider, selected from config at startup.
- **Message handlers:** use a lookup map for a fixed set of message types, and a registry only when handlers ship in separate packages.
- **Wire payloads:** validate a tagged payload once at the entry point, then dispatch it with an exhaustive switch.
