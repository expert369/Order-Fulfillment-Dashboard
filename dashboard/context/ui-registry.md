# UI Component Registry

Central registry of all UI components used by the Order Fulfillment Dashboard.

**Last Updated:** 2026-08-10

---

## Registry Rules

- Every reusable component belongs in this registry.
- Status legend: `Planned` / `In Progress` / `Done` / `Removed`
- Update this file after every feature (AGENTS.md rule).
- Styling follows the rules in `architecture.md`: Tailwind utilities + design tokens only — never hardcoded hex or raw color classes.

---

## Layout Components

| Component    | Status   | Notes                              |
| ------------ | -------- | ---------------------------------- |
| Dashboard    | Planned  | Page shell, 20/80 sidebar split    |
| GlassPanel   | Planned  | Primary/secondary glass surface    |
| GlassSidebar | Planned  | Left nav, ~20% width               |
| OrderGrid    | Planned  | 6-col desktop / 4 / 2 / 1 grid     |

## Order Components

| Component  | Status   | Notes                              |
| ---------- | -------- | ---------------------------------- |
| OrderCard  | Planned  | Order ID, phase, customer, created |
| PhaseBadge | Planned  | Badge per fulfillment phase        |
| PhaseFilter| Planned  | Sidebar filter with counts         |

## Status / Feedback Components

| Component       | Status   | Notes                              |
| --------------- | -------- | ---------------------------------- |
| RefreshButton   | Planned  | Manual refresh                     |
| LastUpdated     | Planned  | "Last updated: HH:MM:SS" indicator |
| LoadingSkeleton | Planned  | Loading state                      |
| EmptyState      | Planned  | "No orders found."                 |
| ErrorState      | Planned  | WooCommerce connection / auth errors |

## Design Tokens

Token categories defined in `architecture.md` §44:

```text
Border Radius   Small / Medium / Large
Glass           Background opacity / border opacity / blur
Spacing         XS / SM / MD / LG / XL
Typography      Heading / Body / Label / Caption
```

Tokens will be implemented once the dashboard styling layer is added (Tailwind CSS).

---

## Change Log

| Date       | Change                    |
| ---------- | ------------------------- |
| 2026-08-10 | Registry initialized with planned components |