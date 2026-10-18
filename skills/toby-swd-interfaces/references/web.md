# Web SPAs

## Hook return type

A hook that returns `[Product | null, Error | null, boolean, refetch, mutate]` needs a long comment about positions and null combinations. Return a tagged union with one variant per valid state:

```tsx
type ProductQuery =
  | { status: 'loading'; product: null; error: null }
  | { status: 'success'; product: Product; error: null }
  | { status: 'error'; product: null; error: Error }
  | { status: 'stale';  product: Product; error: Error };

function useProduct(id: string): ProductQuery & { refetch(): Promise<void>; mutate(p: Product): Promise<void> };
```

> Returns the current query state for the product with this id. The status field has one value for each valid state (loading, success, error, stale). refetch triggers a fresh load. mutate updates locally and reconciles with the server.

In Solid, return the same union inside a signal, and in Svelte, return it inside a store.

## Component props

A `Dialog` with twelve props (`variant`, `initialFocus`, `closeOnEsc`, `closeOnOverlayClick`) needs a comment explaining which combination is safe for a destructive action. When callers use the dialog for three distinct purposes, export one component per purpose built on one shared inner component:

```tsx
<ConfirmDialog open={open} onClose={close} title="Save changes?" onConfirm={doSave} />
<DestructiveConfirmDialog open={open} onClose={close} title="Delete account?"
  body="This cannot be undone." confirmLabel="Delete" onConfirm={doDelete} />
<InfoDialog open={open} onClose={close} title="Heads up" body="..." />
```

> DestructiveConfirmDialog — Renders a destructive-action confirmation when open is true. Calls onConfirm if the user proceeds. Every other path counts as cancel and calls onClose, including esc and overlay click. Focus defaults to the cancel button.

`DestructiveConfirmDialog` locks in the safe settings so callers can't build an unsafe version.

## Headless hook

A `useCombobox` that takes `isOpen`, `setIsOpen`, and `highlightedIndex` forces every caller to manage open and keyboard state. Keep that state inside the hook and return grouped element props that the caller spreads onto each element:

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

> Manages open state, filtering, and keyboard navigation for a combobox. Returns element prop objects that wire ARIA attributes and keyboard handlers to the root, input, list, and items. Calls onSelect when the user confirms a choice via Enter or click.

The caller spreads the returned props and renders `filteredItems`, while keyboard, IME, ARIA, and focus logic stay inside the hook.
