# Order Fulfillment Dashboard — Progress Tracker

## Project Status

**Overall Status:** 🟢 Phase 4 Complete

**Current Phase:** Phase 5 — ERPNext Customer Mapping

**Progress:** `31%`

**Last Updated:** 2026-08-10

---

# Progress Summary

| Phase                       | Status        | Progress |
| --------------------------- | ------------- | -------: |
| 1. Project Foundation       | ✅ Completed  |     100% |
| 2. Configuration            | ✅ Completed  |     100% |
| 3. WooCommerce API Client   | ✅ Completed  |     100% |
| 4. Frappe Backend API       | 🟢 Completed |     100% |
| 5. ERPNext Customer Mapping | ⬜ Not Started |       0% |
| 6. Dashboard Foundation     | ⬜ Not Started |       0% |
| 7. Order Cards              | ⬜ Not Started |       0% |
| 8. Phase Filtering          | ⬜ Not Started |       0% |
| 9. Refresh System           | ⬜ Not Started |       0% |
| 10. Error Handling          | ⬜ Not Started |       0% |
| 11. UI/UX Improvements      | ⬜ Not Started |       0% |
| 12. Testing                 | ⬜ Not Started |       0% |
| 13. Deployment              | ⬜ Not Started |       0% |

---

# Status Legend

```text
⬜ Not Started
🟡 In Progress
🟢 Completed
🔴 Blocked
⚠️ Needs Review
```

---

# Phase 1 — Project Foundation

**Status:** ✅ Completed

### Tasks

* [x] Confirm target Frappe app — `order_fulfillment_dashboard`
* [x] Confirm Frappe/ERPNext version — Frappe 15.103.1, ERPNext 15.103.1
* [x] Confirm module — `Order Fulfillment Dashboard`
* [x] Confirm dashboard page name — `/order_fulfillment` (www page)
* [x] Create project structure — `api/`, `services/order_fulfillment/`, `doctype/`
* [x] Review existing app conventions
* [x] Review required permissions

### Deliverables

* [x] Project structure ready
* [x] Development environment confirmed

### Notes

```text
APP STRUCTURE (adapted from build plan; target app is order_fulfillment_dashboard, not qgc_erp)

order_fulfillment_dashboard/
├── order_fulfillment_dashboard/
│   ├── api/                        <- backend API layer (Phase 4)
│   ├── services/order_fulfillment/ <- WooCommerce client (Phase 3)
│   ├── doctype/                    <- settings DocType (Phase 2)
│   ├── www/order_fulfillment.py    <- dashboard entry (Vite build)
│   └── public/order_fulfillment/   <- built dashboard assets
├── dashboard/                      <- Vite + React 19 + frappe-react-sdk
└── context/                        <- planning docs

KEY DEVIATIONS FROM ORIGINAL PLAN
- Target app is `order_fulfillment_dashboard` (dedicated app exists; build
  plan's `qgc_erp` structure was illustrative only).
- Dashboard is NOT a Frappe Desk Page: it is a standalone Vite/React app
  served from `www/order_fulfillment` at route /order_fulfillment.
- shadcn/ui is a design language to reproduce manually with Tailwind
  (architecture.md §35, §49), per library-docs.md.
- Tailwind CSS not yet installed — required before building UI (Phase 6+).
- CORRECTION (discovered in Phase 2): the nested package
  `order_fulfillment_dashboard/order_fulfillment_dashboard/order_fulfillment_dashboard/`
  was NOT a scaffold artifact — it is the **module folder** for module
  "Order Fulfillment Dashboard" (module folder = scrub(module name)).
  Frappe discovers doctypes under module folders (e.g. `chat/frappe_chat/doctype`).
  It was restored and all doctypes live under it:
  `<module folder>/doctype/`. `api/` and `services/` stay at app-package
  level (matches `chat/` app convention).
- `bench new-doctype` is NOT available on this bench version (5.29.1) —
  DocTypes are hand-authored and synced via `frappe.model.sync.sync_for()`.

PERMISSIONS (reviewed, applied in later phases)
- Configuration: Restrict `Order Fulfillment Settings` to System Manager (Phase 2).
- Dashboard: requires logged-in user; server-side WooCommerce calls only (Phase 4).
- Credentials: Password fields, never exposed to frontend (Phase 2/3).
```

---

# Phase 2 — Configuration

**Status:** ✅ Completed

### DocType

```text
Order Fulfillment Settings
```

### Tasks

* [x] Create Single DocType — `doctype/order_fulfillment_settings/`
* [x] Add WooCommerce URL — Data field
* [x] Add Consumer Key — Password field
* [x] Add Consumer Secret — Password field
* [x] Add API Path — Data field
* [x] Add Enabled field — Check field
* [x] Configure Password field — encrypted at rest, masked in API reads
* [x] Configure permissions — System Manager only (read/write/create)
* [x] Test saving settings — 9 unit tests pass (validation + security)

### Deliverables

* [x] Configuration page available
* [x] Credentials saved securely

### Notes

```text
VALIDATION (enforced when Enabled = 1, skipped when disabled)
- WooCommerce URL: required, must be http(s) with host
- API Path: required, must start with /
- Consumer Key / Secret: required

SECURITY
- Password fields stored encrypted (fernet), masked as ******* in reads
- get_password() is NOT whitelisted — credentials never reach the browser
- Permissions: only System Manager role on the DocType JSON

TESTS
- tests/test_order_fulfillment_settings.py — 9 tests, all passing
  (validation per field, invalid URLs, disabled integration allowed
   to be empty, encrypted storage, password round trip)
```

---

# Phase 3 — WooCommerce API Client

**Status:** ✅ Completed

### API

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment
```

### Tasks

* [x] Create WooCommerce client — `services/order_fulfillment/woo_client.py`
* [x] Load settings — `get_settings()` (disabled/partial config raise)
* [x] Implement authentication — HTTP Basic Auth (consumer key/secret)
* [x] Implement get_orders()
* [x] Implement get_order(order_id)
* [x] Test all orders endpoint — mocked (19 unit tests)
* [x] Test specific order endpoint — mocked
* [x] Implement timeout handling — 10s, mapped to ConnectionError
* [x] Implement HTTP error handling — 401/403 → AuthError, 4xx/5xx → APIError
* [x] Implement response validation — list / `orders` / `data` / `results` keys
* [x] Verify credentials aren't logged — credentials only in auth header, never in URL

### Deliverables

* [x] WooCommerce client working
* [x] All orders retrieval working
* [x] Specific order retrieval working

### Notes

```text
ERROR TAXONOMY (used by Phase 4/10 for friendly messages)
- IntegrationDisabledError      (integration turned off)
- IntegrationNotConfiguredError (incomplete settings)
- WooCommerceConnectionError    (network/timeout)
- WooCommerceAuthenticationError (401/403)
- WooCommerceAPIError           (other HTTP errors)
- WooCommerceInvalidResponseError (bad JSON / unexpected shape)

LIVE API PROBE (2026-08-10)
- Endpoint resolves, requires WooCommerce API credentials:
  HTTP 401 {"code":"rest_forbidden","message":"Invalid or missing
  WooCommerce API credentials."}
- Confirms Basic-Auth-style consumer key auth. Actual response
  structure still unconfirmed — needs real credentials (blocker).
```

---

# Phase 4 — Frappe Backend API

**Status:** ✅ Completed

### Tasks

* [x] Create backend API module — `api/order_fulfillment.py`
* [x] Implement get_orders()
* [x] Implement get_order(order_id)
* [x] Add whitelisted methods — `@frappe.whitelist()` (no `allow_guest`)
* [x] Add permission validation — guest session rejected with PermissionError
* [x] Normalize API response — `success/total/count/orders` + per-order `phases`
* [x] Handle exceptions — mapped to safe error structures, logged, never leaked
* [x] Test from browser/frontend — live HTTP smoke test on test.site (port 8011)

### Deliverables

* [x] Frontend can safely request order data
* [x] WooCommerce credentials remain server-side

### Notes

```text
WHITELISTED METHODS (frappe.call endpoints)
- get_orders()  -> {"success": true, "total": n, "count": n, "orders": [...]}
- get_order(id) -> {"success": true, "order": {...}} | {"order": null} if not found
- Both require a logged-in session; the framework rejects guests (403) and
  _check_permission() adds defense-in-depth.

NORMALIZED ORDER (per architecture.md §77; raw WC response never exposed)
- id, order_id, current_phase, created_at
- customer: null (placeholder — populated in Phase 5)
- phases: {enqueueing, picking, sorting, checking, loading}
  -> {start, end, elapsed} derived from *_start /*_end /*_elapsed

ERROR CONTRACT (architecture.md §82) — returned as JSON, not thrown:
- INTEGRATION_DISABLED / INTEGRATION_NOT_CONFIGURED
- WOOCOMMERCE_CONNECTION_ERROR   ("Unable to connect to WooCommerce...")
- WOOCOMMERCE_AUTHENTICATION_ERROR ("...check the integration settings.")
- WOOCOMMERCE_API_ERROR / WOOCOMMERCE_INVALID_RESPONSE
- INVALID_REQUEST (missing order_id)
- INTERNAL_ERROR (unexpected; logged via frappe.log_error, masked to client)

LIVE SMOKE TEST (2026-08-10, test.site via temp server on :8011)
- Guest call -> HTTP 403 PermissionError (framework whitelist gate)
- Admin + integration disabled -> INTEGRATION_DISABLED payload
- Admin + enabled w/ bogus creds -> real request to WooCommerce ->
  HTTP 401 -> WOOCOMMERCE_AUTHENTICATION_ERROR payload
- Password fields stay masked (*******) in API responses
- NOTE: dev server on :8000 only serves qgc_erp3.site (app NOT installed
  there); test.site must be served explicitly for dashboard dev/test.

TESTS
- tests/test_order_fulfillment_api.py — 19 tests, all passing
  (normalization incl. phase timing, empty/missing order, error mapping
   for all 6 taxonomy codes + unexpected, guest permission, masking)
- Suite total now 47 tests (was 28)
```

---

# Phase 5 — ERPNext Customer Mapping

**Status:** ⬜ Not Started

### Tasks

* [ ] Determine customer identifier from API
* [ ] Determine ERPNext Customer mapping
* [ ] Implement customer lookup
* [ ] Add customer to normalized response
* [ ] Handle missing customer
* [ ] Test customer mapping

### Deliverables

* [ ] Orders display ERPNext Customer

### Notes

```text
Customer mapping strategy:
TBD
```

---

# Phase 6 — Dashboard Foundation

**Status:** ⬜ Not Started

### Tasks

* [ ] Create Frappe Desk Page
* [ ] Create dashboard HTML
* [ ] Create sidebar
* [ ] Set sidebar to approximately 20%
* [ ] Set main content to approximately 80%
* [ ] Create dashboard header
* [ ] Add loading state
* [ ] Add empty state
* [ ] Add error state

### Deliverables

* [ ] Dashboard page accessible
* [ ] Sidebar visible
* [ ] Main content area ready

### Notes

```text
No notes yet.
```

---

# Phase 7 — Order Cards

**Status:** ⬜ Not Started

### Tasks

* [ ] Create order card markup
* [ ] Display order ID
* [ ] Display current phase
* [ ] Display customer
* [ ] Display created_at
* [ ] Format date
* [ ] Handle missing values
* [ ] Create 6-column desktop grid
* [ ] Add responsive grid

### Target Grid

```text
Desktop: 6
Laptop:  4
Tablet:  2
Mobile:  1
```

### Deliverables

* [ ] Orders appear as cards
* [ ] Cards display required information

### Notes

```text
No notes yet.
```

---

# Phase 8 — Phase Filtering

**Status:** ⬜ Not Started

### Sidebar Filters

* [ ] All Orders
* [ ] Enqueue
* [ ] Picking
* [ ] Sorting
* [ ] Checking
* [ ] Loading

### Tasks

* [ ] Implement All Orders
* [ ] Implement Enqueue
* [ ] Implement Picking
* [ ] Implement Sorting
* [ ] Implement Checking
* [ ] Implement Loading
* [ ] Add active filter state
* [ ] Add phase counts
* [ ] Verify filtering without page reload

### Deliverables

* [ ] All phase filters work
* [ ] Active filter is visually clear

### Notes

```text
No notes yet.
```

---

# Phase 9 — Refresh System

**Status:** ⬜ Not Started

### Tasks

* [ ] Add manual refresh button
* [ ] Add loading state
* [ ] Implement 30-second polling
* [ ] Prevent duplicate requests
* [ ] Preserve active filter
* [ ] Update phase counts
* [ ] Update last refreshed time

### Deliverables

* [ ] Manual refresh works
* [ ] Auto-refresh works
* [ ] Last updated time is visible

### Notes

```text
Refresh interval:
30 seconds
```

---

# Phase 10 — Error Handling

**Status:** ⬜ Not Started

### Tasks

* [ ] Handle WooCommerce connection failure
* [ ] Handle authentication failure
* [ ] Handle timeout
* [ ] Handle malformed API response
* [ ] Handle empty order list
* [ ] Handle missing customer
* [ ] Handle backend errors
* [ ] Handle permission errors
* [ ] Add user-friendly error messages

### Deliverables

* [ ] Dashboard fails gracefully
* [ ] Errors don't expose sensitive information

### Notes

```text
No notes yet.
```

---

# Phase 11 — UI/UX Improvements

**Status:** ⬜ Not Started

### Tasks

* [ ] Improve sidebar design
* [ ] Improve card design
* [ ] Improve phase indicators
* [ ] Improve spacing
* [ ] Add hover states
* [ ] Improve loading state
* [ ] Improve empty state
* [ ] Improve error state
* [ ] Improve responsive layout
* [ ] Verify 6-column desktop layout

### Optional

* [ ] Full-screen mode
* [ ] Dark mode
* [ ] Sound notification
* [ ] New order animation

### Deliverables

* [ ] Dashboard is suitable for daily operations use

### Notes

```text
No notes yet.
```

---

# Phase 12 — Testing

**Status:** ⬜ Not Started

## Backend

* [ ] Settings save successfully
* [ ] Credentials remain secure
* [ ] WooCommerce API works
* [ ] All orders work
* [ ] Specific order works
* [ ] Customer lookup works
* [ ] API errors handled
* [ ] Invalid credentials handled

## Frontend

* [ ] Dashboard loads
* [ ] Orders render
* [ ] Cards display correct information
* [ ] Six-column layout works
* [ ] Sidebar works
* [ ] All Orders works
* [ ] Enqueue works
* [ ] Picking works
* [ ] Sorting works
* [ ] Checking works
* [ ] Loading works
* [ ] Refresh works
* [ ] Auto-refresh works
* [ ] Empty state works
* [ ] Error state works

## Responsive

* [ ] Desktop
* [ ] Laptop
* [ ] Tablet
* [ ] Mobile

### Deliverables

* [ ] MVP passes functional testing

### Notes

```text
No notes yet.
```

---

# Phase 13 — Deployment

**Status:** ⬜ Not Started

### Tasks

* [ ] Review code
* [ ] Commit changes
* [ ] Run migrations
* [ ] Build assets
* [ ] Clear cache
* [ ] Restart services if required
* [ ] Configure production credentials
* [ ] Test production WooCommerce API
* [ ] Test production dashboard
* [ ] Verify permissions
* [ ] Verify automatic refresh

### Deployment Commands

```bash
bench migrate
bench build --app qgc_erp
bench clear-cache
```

### Deliverables

* [ ] Feature deployed
* [ ] Production dashboard working

### Notes

```text
No notes yet.
```

---

# Current Blockers

| Blocker                              | Status  | Impact | Resolution                      |
| ------------------------------------ | ------- | ------ | ------------------------------- |
| Customer mapping not confirmed       | 🔴 Open | High   | Confirm API customer identifier |
| API response structure not confirmed | 🔴 Open | High   | Inspect actual API response     |
| —                                    | —       | —      | —                               |

---

# Technical Decisions

| Decision                             | Status       | Notes                        |
| ------------------------------------ | ------------ | ---------------------------- |
| Target Frappe app                    | ✅ Confirmed | `order_fulfillment_dashboard`|
| Frappe version                       | ✅ Confirmed | 15.103.1                     |
| ERPNext version                      | ✅ Confirmed | 15.103.1                     |
| Module name                          | ✅ Confirmed | `Order Fulfillment Dashboard`|
| Dashboard delivery                   | ✅ Confirmed | Standalone Vite/React app in `dashboard/`, served via `www/` |
| Dashboard route                      | ✅ Confirmed | `/order_fulfillment`         |
| Use Single DocType for configuration | 🟢 Confirmed | `Order Fulfillment Settings` |
| Settings permissions                  | ✅ Confirmed | System Manager only          |
| Credential storage                    | ✅ Confirmed | Password fields, encrypted   |
| Settings validation                   | ✅ Confirmed | URL/path/credentials when enabled |
| Doctype module folder                 | ✅ Confirmed | `<module folder>/doctype/` per Frappe convention |
| Store orders locally                 | 🟢 No        | WooCommerce remains source   |
| Server-side WooCommerce requests     | 🟢 Confirmed | Protect credentials          |
| WC API auth scheme                   | ✅ Confirmed | HTTP Basic (key:secret)      |
| WC client timeouts/errors            | ✅ Confirmed | 10s timeout, typed errors    |
| Dashboard as Frappe Desk Page        | ❌ Superseded| Standalone React page instead (see Foundation notes) |
| Sidebar width                        | 🟢 Confirmed | Approximately 20%            |
| Desktop card grid                    | 🟢 Confirmed | 6 columns                    |
| Auto-refresh                         | 🟢 Planned   | 30 seconds                   |
| ERPNext Customer lookup              | 🟡 Pending   | Mapping needs confirmation   |
| UI library                           | 🟡 Pending   | Tailwind + hand-built shadcn-style components |

---

# API Information

## Base URL

```text
https://cms-staging.buildmaster.ph
```

## Endpoint

```text
/wp-json/qgc-erp/v1/order-fulfillment
```

## Full Endpoint

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment
```

## Specific Order

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment?order_id=47375
```

---

# Fulfillment Phases

```text
1. Enqueue
2. Picking
3. Sorting
4. Checking
5. Loading
```

---

# Progress Log

## 2026-08-10

### Completed

* [x] Project requirements defined
* [x] Dashboard concept defined
* [x] WooCommerce API endpoint identified
* [x] Specific order endpoint identified
* [x] Configuration DocType identified
* [x] Fulfillment phases identified
* [x] Sidebar layout defined
* [x] 6-column card layout defined
* [x] ERPNext customer requirement identified

## 2026-08-10 — Phase 1 (Foundation)

### Completed

* [x] Target app confirmed: `order_fulfillment_dashboard`
* [x] Versions confirmed: Frappe/ERPNext 15.103.1, Node v20
* [x] Module confirmed: `Order Fulfillment Dashboard`
* [x] Dashboard entry confirmed: `www/order_fulfillment` (route `/order_fulfillment`)
* [x] Created `api/`, `services/order_fulfillment/` packages
* [x] Created `context/ui-registry.md` and `context/library-docs.md` (missing)
* [x] Reviewed conventions: ruff (tabs, double quotes), oxlint, pre-commit
* [x] Reviewed permissions plan (settings → System Manager, dashboard → logged-in)

## 2026-08-10 — Phase 2 (Configuration)

### Completed

* [x] Created `Order Fulfillment Settings` Single DocType (5 fields)
* [x] Validation in controller (URL, API path, credentials when enabled)
* [x] System Manager-only permissions in DocType JSON
* [x] Installed app on `test.site`, synced DocType, migrated
* [x] 9 unit tests passing (validation + encrypted password storage)
* [x] Discovered module-folder convention; moved doctype under it
* [x] ruff clean (pyproject rules: tabs, double quotes)

## 2026-08-10 — Phase 3 (WooCommerce API Client)

### Completed

* [x] `woo_client.py`: get_orders(), get_order(id), Basic Auth, 10s timeout
* [x] Typed error taxonomy (connection/auth/api/invalid response/disabled)
* [x] 19 unit tests passing (auth header placement, URL hygiene, error mapping)
* [x] Live probe: endpoint requires WooCommerce credentials (HTTP 401)
* [x] ruff clean

## 2026-08-10 — Phase 4 (Frappe Backend API)

### Completed

* [x] `api/order_fulfillment.py`: whitelisted get_orders() + get_order(id)
* [x] Guest rejection (framework 403 + explicit session check)
* [x] Normalized response contract (§77) with per-phase start/end/elapsed
* [x] Error taxonomy mapped to safe JSON contract (§82), masked + logged
* [x] Live HTTP smoke test on test.site (disabled + bogus-credential paths)
* [x] 19 new unit tests; suite at 47 total
* [x] ruff clean

### Next

* [ ] Inspect actual WooCommerce API response (needs real credentials)
* [ ] Implement ERPNext customer lookup (Phase 5)
* [ ] Build dashboard frontend (Phase 6+)

---

# Change Log

| Date       | Change                            |
| ---------- | --------------------------------- |
| 2026-08-10 | Initial project definition        |
| 2026-08-10 | Added WooCommerce API integration |
| 2026-08-10 | Added ERPNext customer lookup     |
| 2026-08-10 | Added 6-column card dashboard     |
| 2026-08-10 | Added fulfillment phase filters   |
| 2026-08-10 | Added auto-refresh requirement    |
| 2026-08-10 | Phase 1 complete: foundation, structure, conventions confirmed |
| 2026-08-10 | Created ui-registry.md + library-docs.md |
| 2026-08-10 | Phase 2 complete: Order Fulfillment Settings DocType + validation + tests |
| 2026-08-10 | Fixed module folder convention; app installed on test.site |
| 2026-08-10 | Phase 3 complete: WooCommerce client with auth, errors, 19 tests |
| 2026-08-10 | Phase 4 complete: whitelisted backend API, normalization, error contract, 19 tests |

---

# MVP Completion

```text
Overall Progress: 31%

Foundation       ██████████ 100%
Configuration    ██████████ 100%
API Integration  ██████████ 100%
Backend API      ██████████ 100%
Customer Mapping ░░░░░░░░░░ 0%
Dashboard        ░░░░░░░░░░ 0%
Cards            ░░░░░░░░░░ 0%
Filtering        ░░░░░░░░░░ 0%
Refresh          ░░░░░░░░░░ 0%
Error Handling   ░░░░░░░░░░ 0%
Testing          ░░░░░░░░░░ 0%
Deployment       ░░░░░░░░░░ 0%
```

---

# Definition of Done

The MVP is complete when:

* [ ] WooCommerce configuration works
* [ ] WooCommerce API connection works
* [ ] Orders are retrieved
* [ ] ERPNext customer is identified
* [ ] Dashboard loads
* [ ] Orders display as cards
* [ ] Desktop displays 6 cards per row
* [ ] Sidebar filtering works
* [ ] All fulfillment phases work
* [ ] Manual refresh works
* [ ] Automatic refresh works
* [ ] Error handling works
* [ ] Security requirements are satisfied
* [ ] Production deployment succeeds
