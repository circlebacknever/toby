# Web SPAs (React, Solid, Svelte)

## Hook return type

A hook that returns `[Product | null, Error | null, boolean, refetch, mutate]` needs a seven-sentence comment about positions and null combinations. Each caller also names the positions its own way. Return a discriminated union:

```tsx
type ProductQuery =
  | { status: 'loading'; product: null; error: null }
  | { status: 'success'; product: Product; error: null }
  | { status: 'error'; product: null; error: Error }
  | { status: 'stale';  product: Product; error: Error };

function useProduct(id: string): ProductQuery & { refetch(): Promise<void>; mutate(p: Product): Promise<void> };
```

> Returns the current query state for the product with this id. The status discriminator has one value for each of the four legal combinations (loading, success, error, stale). refetch triggers a fresh load. mutate updates locally and reconciles with the server.

In Solid, return the same union inside a signal, and in Svelte, return it inside a store.

## Component props

A `Dialog` with twelve props, including `variant`, `initialFocus`, `closeOnEsc`, and `closeOnOverlayClick`, needs a comment that tells callers which combination is safe for a destructive action. When the call sites use the dialog for three different purposes, make one component for each purpose. Build all three on one shared inner component:

```tsx
<ConfirmDialog open={open} onClose={close} title="Save changes?" onConfirm={doSave} />
<DestructiveConfirmDialog open={open} onClose={close} title="Delete account?"
  body="This cannot be undone." confirmLabel="Delete" onConfirm={doDelete} />
<InfoDialog open={open} onClose={close} title="Heads up" body="..." />
```

> DestructiveConfirmDialog — Renders a destructive-action confirmation when open is true. Calls onConfirm if the user proceeds. Every other path counts as cancel and calls onClose, including esc and overlay click. Focus defaults to the cancel button.

`DestructiveConfirmDialog` locks in the safe settings, so no caller can build an unsafe version. If callers repeat three prop combinations but use them for the same purpose, keep one component.

## Headless hook

A `useCombobox` that takes `isOpen`, `setIsOpen`, `highlightedIndex`, and their setters makes every caller write and track the open, closed, and highlighted state itself. Keep that state inside the hook, and return prop bundles. A prop bundle is an object of props that the caller spreads onto one element:

```tsx
function useCombobox<T>(opts: {
  items: T[];
  getId: (item: T) => string;
  filter?: (item: T, query: string) => boolean;
  getLabel?: (item: T) => string;
  onSelect?: (item: T) => void;
}): {
  rootProps: HTMLAttributes<HTMLDivElement>;
  inputProps: InputHTMLAttributes<HTMLInputElement>;
  listProps: HTMLAttributes<HTMLUListElement>;
  itemProps(index: number): LiHTMLAttributes<HTMLLIElement>;
  isOpen: boolean; filteredItems: T[]; highlightedIndex: number; selectedItem: T | null;
  open(): void; close(): void; reset(): void;
};
```

> Implements a headless combobox state machine for the items and id function the caller passes. Returns prop bundles that wire ARIA attributes and keyboard handlers to the input, list, and items. Rendering state includes filteredItems, computed from the current input value through filter, and highlightedIndex, which tracks keyboard navigation. onSelect fires when the user confirms a choice via Enter or click.

The caller spreads the bundles and renders `filteredItems`. Keyboard handling, IME composition, ARIA, and focus stay inside the hook.
