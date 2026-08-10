# Library Docs — Project-Specific Rules

Project-specific usage rules for third party libraries.
**Last Updated:** 2026-08-10

---

## Reading Order

Before adding ANY third party library:

1. Load its installed skill (AGENTS.md rule).
2. Read this file for project rules.
3. Read `ui-registry.md` to see if a component already exists.

---

## Current Stack

| Library         | Version       | Status      | Notes                                   |
| --------------- | ------------- | ----------- | --------------------------------------- |
| React           | ^19.2.8       | Installed   | Frontend runtime                        |
| Vite            | ^8.2.0        | Installed   | Build tool, dev server on :8080         |
| frappe-react-sdk| ^1.3.11       | Installed   | Frappe backend communication            |
| Tailwind CSS    | —             | Not yet     | To be added for styling (Phase 6+)      |
| shadcn/ui       | —             | Not yet     | Design language only — see rules below  |

---

## frappe-react-sdk

- Already used in `src/main.tsx` (`FrappeProvider`) — the only sanctioned way for the dashboard to call the Frappe backend.
- All backend calls go through this SDK; never call WooCommerce directly from the browser (security requirement, `project-overview.md` §21).
- Dashboard API calls will use `useFrappeGetCall` / `frappe.call` against whitelisted methods (Phase 4+).

## shadcn/ui

- NOT a package — it is a **design language** reproduced by hand per `architecture.md` §35 and §49 clause 12-13.
- Components are hand-built with Tailwind + React following shadcn patterns; never `npm install` shadcn CLI components into this app.
- Before adding a component, load the `shadcn` skill and check the registry.

## Tailwind CSS

- Adding Tailwind requires: load installed skill first, then verify no duplicate tokens exist in `ui-registry.md`.
- Never use hardcoded hex values or raw color classes (AGENTS.md rule) — all styling via design tokens.

---

## Change Log

| Date       | Change                        |
| ---------- | ----------------------------- |
| 2026-08-10 | Initialized library docs      |