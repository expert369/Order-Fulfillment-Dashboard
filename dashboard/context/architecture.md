# UI Architecture — shadcn/ui + Glassmorphism

## 34. UI Design System

The Order Fulfillment Dashboard will use **shadcn/ui** as the primary UI component approach, with **Tailwind CSS** for styling and layout.

The visual design will use **glassmorphism** as the primary aesthetic direction.

### Design Stack

```text
Frappe Desk Page
       │
       ▼
HTML / JavaScript
       │
       ▼
Tailwind CSS
       │
       ▼
shadcn/ui Components
       │
       ▼
Glassmorphism Visual Layer
```

---

# 35. shadcn/ui

The dashboard should follow the design philosophy and component patterns of **shadcn/ui**.

Recommended component patterns include:

* Card
* Button
* Badge
* Separator
* Scroll Area
* Tooltip
* Dropdown Menu
* Input
* Skeleton
* Alert
* Sheet
* Dialog

The project should avoid unnecessarily introducing components that are not needed by the dashboard.

## Important Frappe Consideration

Because this is a **Frappe Desk Page**, shadcn/ui should not be assumed to work exactly like it does inside a standalone React/Next.js application.

If the existing Frappe frontend architecture is not React-based, the implementation should reproduce the **shadcn/ui visual language and component patterns using Tailwind CSS and standard HTML/JavaScript**, rather than forcing a React runtime into the Frappe page.

The goal is:

> **shadcn/ui design language and component quality, while respecting Frappe's native page architecture.**

---

# 36. Glassmorphism Design

Glassmorphism should be used throughout the dashboard while maintaining readability and performance.

Core characteristics:

* Translucent surfaces
* Background blur
* Subtle borders
* Soft shadows
* Layered surfaces
* Rounded corners
* Low-contrast backgrounds
* Clear typography

Conceptual styling:

```css
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
```

The actual values should be adjusted according to the final dashboard theme.

---

# 37. Glassmorphism Hierarchy

Glassmorphism should not be applied equally to every element.

Use different visual levels:

```text
Background
    │
    ├── Primary Glass Surface
    │
    │     ├── Sidebar
    │     └── Dashboard Header
    │
    └── Secondary Glass Surface
          │
          ├── Order Cards
          ├── Filters
          └── Controls
```

This creates depth without making the interface visually noisy.

---

# 38. Dashboard Layout

The dashboard should maintain the existing 20/80 layout.

```text
┌───────────────────────────────────────────────────────────────┐
│                    Glass Header                               │
├───────────────────┬───────────────────────────────────────────┤
│                   │                                           │
│   Glass Sidebar   │            Glass Main Content             │
│       ~20%        │                  ~80%                     │
│                   │                                           │
│  Dashboard        │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│                   │  │ Card │ │ Card │ │ Card │ │ Card │   │
│  All Orders       │  └──────┘ └──────┘ └──────┘ └──────┘   │
│  Enqueue          │                                           │
│  Picking          │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  Sorting          │  │ Card │ │ Card │ │ Card │ │ Card │   │
│  Checking         │  └──────┘ └──────┘ └──────┘ └──────┘   │
│  Loading          │                                           │
│                   │              6 columns                    │
└───────────────────┴───────────────────────────────────────────┘
```

---

# 39. Order Card Design

Order cards should use the glassmorphism style.

Example:

```text
┌──────────────────────────┐
│                          │
│  #47375          PICKING │
│                          │
│  ABC Construction        │
│                          │
│  Created                 │
│  Aug 10, 2026 09:42 AM   │
│                          │
└──────────────────────────┘
```

Recommended visual properties:

```text
Rounded corners
Glass background
Backdrop blur
Subtle border
Soft shadow
Phase badge
Clear typography
```

---

# 40. Phase Badges

The current fulfillment phase should be visually prominent.

Example:

```text
┌────────────────────────┐
│ #47375                 │
│                        │
│ [ PICKING ]            │
│                        │
│ ABC Construction       │
│                        │
│ Created                │
│ Aug 10, 2026 09:42 AM │
└────────────────────────┘
```

Each phase can have its own visual treatment.

```text
Enqueue
Picking
Sorting
Checking
Loading
```

The phase badge should remain readable against the glass surface.

---

# 41. Sidebar Design

The sidebar should also use glassmorphism.

Example:

```text
╭────────────────────╮
│                    │
│ Order Fulfillment  │
│                    │
│ ◉ Dashboard        │
│                    │
│ PHASES             │
│                    │
│ ○ All Orders   125 │
│ ○ Enqueue       12 │
│ ○ Picking        8 │
│ ○ Sorting        5 │
│ ○ Checking       7 │
│ ○ Loading        3 │
│                    │
╰────────────────────╯
```

The active phase should have a stronger glass/highlight treatment.

Example:

```text
┌─────────────────────┐
│ ◉ Picking        8  │  ← Active
└─────────────────────┘
```

---

# 42. Dashboard Background

Glassmorphism requires visual contrast behind translucent surfaces.

The dashboard should therefore have a subtle background rather than a completely flat background.

Conceptual structure:

```text
                    Background
                        │
            ┌───────────┴───────────┐
            │                       │
       Background              Soft gradients
       base color              / blurred shapes
            │                       │
            └───────────┬───────────┘
                        │
                        ▼
                  Glass surfaces
```

The background should remain subtle enough that text and cards remain easy to read.

Avoid excessive decorative effects that compete with the order information.

---

# 43. Component Design System

Recommended reusable UI components:

```text
components/
│
├── GlassCard
├── GlassPanel
├── GlassSidebar
├── PhaseBadge
├── OrderCard
├── OrderGrid
├── PhaseFilter
├── RefreshButton
├── LoadingSkeleton
├── EmptyState
├── ErrorState
└── LastUpdated
```

Conceptually:

```text
Dashboard
│
├── GlassSidebar
│   └── PhaseFilter
│
└── MainContent
    │
    ├── GlassPanel
    │   ├── RefreshButton
    │   └── LastUpdated
    │
    └── OrderGrid
        └── OrderCard
            └── PhaseBadge
```

---

# 44. Design Tokens

The UI should use centralized design values rather than hardcoding styles throughout the application.

Example:

```text
Border Radius
    ├── Small
    ├── Medium
    └── Large

Glass
    ├── Background Opacity
    ├── Border Opacity
    └── Blur Amount

Spacing
    ├── XS
    ├── SM
    ├── MD
    ├── LG
    └── XL

Typography
    ├── Heading
    ├── Body
    ├── Label
    └── Caption
```

This allows the visual design to be changed globally.

---

# 45. Tailwind CSS

Tailwind CSS should be used for:

* Layout
* Grid
* Flexbox
* Spacing
* Typography
* Responsive design
* Borders
* Rounded corners
* Shadows
* Backdrop blur
* Transitions
* Hover states

Example conceptual utility combination:

```text
rounded-xl
border
backdrop-blur-xl
shadow-lg
transition
```

The exact classes should be adapted to the project's Tailwind configuration.

---

# 46. Responsive Design

The shadcn/glass design should remain responsive.

```text
Desktop
┌──────────────┬───────────────────────────────────────┐
│   Sidebar    │       6-column Order Grid             │
│     20%      │                                       │
└──────────────┴───────────────────────────────────────┘


Laptop
┌──────────────┬──────────────────────────────┐
│   Sidebar    │     4-column Order Grid      │
└──────────────┴──────────────────────────────┘


Tablet
┌────────────┬───────────────────────┐
│  Sidebar   │   2-column Grid       │
└────────────┴───────────────────────┘


Mobile
┌──────────────────────────┐
│      Mobile Controls     │
├──────────────────────────┤
│       Order Card         │
├──────────────────────────┤
│       Order Card         │
└──────────────────────────┘
```

The desktop requirement remains:

```text
6 columns
```

---

# 47. Accessibility

Glassmorphism must not compromise accessibility.

The implementation should ensure:

* Sufficient text contrast
* Visible active states
* Keyboard navigation
* Focus states
* Accessible buttons
* Accessible labels
* No information conveyed only through color
* Readable text over translucent backgrounds

Phase colors should be supplemental rather than the only indication of status.

---

# 48. Performance

Glassmorphism effects can be expensive when heavily applied.

Therefore:

* Avoid excessive `backdrop-filter`
* Avoid large numbers of animated blurred elements
* Avoid unnecessary animations
* Keep background effects lightweight
* Avoid applying blur to every nested element
* Prefer a small number of glass layers

Recommended hierarchy:

```text
1 Background effect
        ↓
2 Main glass container
        ↓
3 Sidebar glass surface
        ↓
4 Order cards
        ↓
5 Small badges/buttons
```

Do not create multiple nested backdrop blur layers unnecessarily.

---

# 49. UI Architecture Rules

The following rules should be followed during implementation:

1. Use **shadcn/ui design principles** for UI components.
2. Use **Tailwind CSS** for styling and layout.
3. Use **glassmorphism** as the primary visual style.
4. Keep the interface clean and operationally focused.
5. Do not overuse transparency.
6. Maintain strong text contrast.
7. Use reusable UI components.
8. Centralize design tokens.
9. Maintain responsive behavior.
10. Keep the 6-column desktop card grid.
11. Keep the sidebar approximately 20% wide.
12. Avoid introducing React solely for shadcn if the Frappe page is not React-based.
13. Prefer native Frappe page architecture with shadcn-inspired/Tailwind components when appropriate.
14. Keep animations subtle.
15. Prioritize order information over decorative effects.

---

# 50. Updated Technology Stack

The project technology stack is:

| Layer          | Technology                       |
| -------------- | -------------------------------- |
| ERP            | ERPNext                          |
| Framework      | Frappe                           |
| Backend        | Python                           |
| External API   | WooCommerce / WordPress REST API |
| Frontend       | Frappe Desk Page                 |
| UI Design      | shadcn/ui design system          |
| Styling        | Tailwind CSS                     |
| Visual Style   | Glassmorphism                    |
| Data           | WooCommerce + ERPNext            |
| Communication  | REST API                         |
| Refresh        | Polling / 30 seconds             |
| Authentication | WooCommerce Consumer Key/Secret  |

---

# 51. Updated Architecture

```text
                         WOOCOMMERCE
                              │
                              │ REST API
                              ▼
                 ┌────────────────────────┐
                 │    WooCommerce Client  │
                 └────────────┬───────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Order Fulfillment      │
                 │ Service                │
                 └────────────┬───────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             WooCommerce Data      ERPNext Customer
                    │                   │
                    └─────────┬─────────┘
                              ▼
                 ┌────────────────────────┐
                 │       Frappe API       │
                 └────────────┬───────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 ORDER FULFILLMENT DASHBOARD                  │
│                                                              │
│  ┌─────────────────┐       ┌───────────────────────────────┐ │
│  │ Glass Sidebar   │       │      Glass Main Content       │ │
│  │                 │       │                               │ │
│  │ Dashboard       │       │  ┌────┐ ┌────┐ ┌────┐ ┌────┐│ │
│  │                 │       │  │Card│ │Card│ │Card│ │Card││ │
│  │ All Orders      │       │  └────┘ └────┘ └────┘ └────┘│ │
│  │ Enqueue         │       │                               │ │
│  │ Picking         │       │  ┌────┐ ┌────┐ ┌────┐ ┌────┐│ │
│  │ Sorting         │       │  │Card│ │Card│ │Card│ │Card││ │
│  │ Checking        │       │  └────┘ └────┘ └────┘ └────┘│ │
│  │ Loading         │       │                               │ │
│  │                 │       │          6 columns            │ │
│  └─────────────────┘       └───────────────────────────────┘ │
│                                                              │
│            shadcn/ui + Tailwind + Glassmorphism              │
└──────────────────────────────────────────────────────────────┘
```

---

# 52. Final UI Direction

The final dashboard should feel like a **modern warehouse operations monitoring system**, not a traditional ERP table.

The visual hierarchy should be:

```text
                  ORDER FULFILLMENT
                         │
             ┌───────────┴───────────┐
             │                       │
          PHASES                  ORDERS
             │                       │
       Sidebar Filters          Glass Cards
             │                       │
       Order Counts             Order ID
                                     │
                                Phase Badge
                                     │
                                  Customer
                                     │
                                Created At
```

The desired visual character is:

> **Modern + clean + operational + glassmorphic + information-dense without feeling cluttered.**

# 53. Frontend State Management — Zustand

The Order Fulfillment Dashboard will use **Zustand** as the frontend state management solution.

Zustand will manage the dashboard's client-side state and provide a centralized store that can be accessed by the dashboard components.

## State Architecture

```text
                    Frappe Backend
                          │
                          │ API Response
                          ▼
                 ┌───────────────────┐
                 │  Zustand Store    │
                 │                   │
                 │ orders            │
                 │ selectedPhase     │
                 │ loading           │
                 │ error             │
                 │ lastUpdated       │
                 │ autoRefresh       │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Sidebar        Order Grid     Dashboard
        Filters        / Cards        Controls
```

---

# 54. Why Zustand

Zustand is preferred because the dashboard has multiple UI components that need access to the same state.

For example:

```text
Sidebar
    │
    └── selectedPhase

Order Grid
    │
    └── orders

Refresh Button
    │
    └── fetchOrders()

Dashboard
    │
    └── loading / error / lastUpdated
```

Without centralized state, these components could become tightly coupled.

Zustand allows the components to communicate through a shared store.

---

# 55. Recommended Store

Suggested location:

```text
qgc_erp/
└── page/
    └── order_fulfillment_dashboard/
        ├── order_fulfillment_dashboard.js
        ├── order_fulfillment_dashboard.html
        └── store/
            └── orderFulfillmentStore.js
```

If the project is structured as a React/Vite frontend:

```text
src/
├── stores/
│   └── orderFulfillmentStore.ts
│
├── components/
│   ├── OrderCard.tsx
│   ├── OrderGrid.tsx
│   ├── Sidebar.tsx
│   └── PhaseBadge.tsx
│
└── pages/
    └── OrderFulfillmentDashboard.tsx
```

---

# 56. Zustand Store State

The initial store should contain:

```javascript
{
    orders: [],
    selectedPhase: "all",
    loading: false,
    error: null,
    lastUpdated: null,
    autoRefresh: true
}
```

The store should also expose actions:

```javascript
{
    fetchOrders,
    fetchOrder,
    setSelectedPhase,
    setAutoRefresh,
    clearError
}
```

---

# 57. Example Store Structure

Conceptually:

```javascript
import { create } from "zustand";

export const useOrderFulfillmentStore = create((set) => ({
    orders: [],
    selectedPhase: "all",
    loading: false,
    error: null,
    lastUpdated: null,
    autoRefresh: true,

    setSelectedPhase: (phase) => {
        set({
            selectedPhase: phase,
        });
    },

    fetchOrders: async () => {
        set({
            loading: true,
            error: null,
        });

        try {
            const response = await fetchOrdersFromFrappe();

            set({
                orders: response,
                loading: false,
                lastUpdated: new Date(),
            });
        } catch (error) {
            set({
                loading: false,
                error: "Unable to retrieve orders.",
            });
        }
    },

    setAutoRefresh: (enabled) => {
        set({
            autoRefresh: enabled,
        });
    },
}));
```

The exact implementation will depend on whether the dashboard uses React or Frappe's native JavaScript architecture.

---

# 58. Store Responsibilities

Zustand should manage **frontend state**, not business logic that belongs to the backend.

### Zustand should handle

* Current orders
* Selected phase
* Loading state
* Error state
* Last updated timestamp
* Auto-refresh state
* UI-related filters
* Refresh actions

### Zustand should NOT handle

* WooCommerce credentials
* Consumer Secret
* WooCommerce authentication
* Direct database queries
* ERPNext business rules
* Sensitive server-side logic

The correct architecture is:

```text
Zustand
   │
   │ Frappe API request
   ▼
Frappe Backend
   │
   ▼
Order Fulfillment Service
   │
   ▼
WooCommerce
```

---

# 59. Order Filtering with Zustand

The sidebar will update the active phase through the Zustand store.

Example:

```text
User clicks:

Picking
   │
   ▼
setSelectedPhase("Picking")
   │
   ▼
Zustand Store
   │
   ▼
Order Grid reads selectedPhase
   │
   ▼
Display Picking orders
```

The dashboard does not need to request the API again simply because the user changed the phase filter.

The existing order collection can be filtered client-side.

---

# 60. Derived Order List

The dashboard can derive the visible orders from:

```text
orders
+
selectedPhase
```

Conceptually:

```javascript
const visibleOrders =
    selectedPhase === "all"
        ? orders
        : orders.filter(
            order => order.current_phase === selectedPhase
        );
```

This keeps filtering fast and avoids unnecessary API requests.

---

# 61. Zustand + Auto Refresh

Zustand should also coordinate the dashboard's refresh behavior.

```text
                 Zustand
                    │
              autoRefresh
                    │
                    ▼
             30-second timer
                    │
                    ▼
              fetchOrders()
                    │
                    ▼
              Frappe API
                    │
                    ▼
             Updated orders
                    │
                    ▼
              Zustand Store
                    │
                    ▼
              Order Grid
```

When new data arrives, the store is updated and the dashboard automatically reflects the new state.

---

# 62. Preserve Active Filter

The selected phase should remain unchanged when orders are refreshed.

Example:

```text
Before refresh:

selectedPhase = "Picking"

orders = 23
```

After refresh:

```text
fetchOrders()
      │
      ▼
orders = 25
```

The store should maintain:

```text
selectedPhase = "Picking"
```

Therefore, the dashboard continues displaying:

```text
Picking
25 orders
```

rather than returning to "All Orders".

---

# 63. Component-State Relationship

The expected relationship is:

```text
                         Zustand Store
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
         Sidebar           Header          Order Grid
            │                 │                 │
            ▼                 ▼                 ▼
      selectedPhase      lastUpdated         orders
      phase filters      refresh             visibleOrders
                         loading
                              │
                              ▼
                        Refresh Button
```

Components should subscribe only to the state they need.

For example:

```text
Sidebar
    → selectedPhase
    → setSelectedPhase()

OrderGrid
    → orders
    → selectedPhase

RefreshButton
    → loading
    → fetchOrders()

LastUpdated
    → lastUpdated
```

This keeps component updates efficient and avoids unnecessary re-renders.

---

# 64. Updated Frontend Architecture

The frontend architecture is now:

```text
┌──────────────────────────────────────────────────────────────┐
│                 ORDER FULFILLMENT DASHBOARD                  │
│                                                              │
│                  shadcn/ui Design System                     │
│                           │                                  │
│                      Tailwind CSS                            │
│                           │                                  │
│                     Glassmorphism                            │
│                           │                                  │
│                      UI Components                           │
│                           │                                  │
│                           ▼                                  │
│                    Zustand Store                             │
│                           │                                  │
│          ┌────────────────┼─────────────────┐                │
│          │                │                 │                │
│          ▼                ▼                 ▼                │
│       Sidebar          Order Grid       Dashboard Controls   │
│          │                │                 │                │
│          └────────────────┼─────────────────┘                │
│                           │                                  │
│                           ▼                                  │
│                      Frappe API                              │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
                  Order Fulfillment Service
                            │
                            ▼
                       WooCommerce
```

---

# 65. Updated Technology Stack

| Layer            | Technology                             |
| ---------------- | -------------------------------------- |
| ERP              | ERPNext                                |
| Framework        | Frappe                                 |
| Backend          | Python                                 |
| External API     | WooCommerce / WordPress REST API       |
| Frontend         | Frappe Desk Page / React if applicable |
| UI Components    | shadcn/ui design system                |
| Styling          | Tailwind CSS                           |
| Visual Style     | Glassmorphism                          |
| State Management | **Zustand**                            |
| Data Source      | WooCommerce + ERPNext                  |
| Communication    | REST API                               |
| Refresh          | Polling / 30 seconds                   |
| Authentication   | WooCommerce Consumer Key/Secret        |

---

# 66. Updated Frontend Rules

The implementation should follow these rules:

1. Use **Zustand** for shared frontend state.
2. Use **shadcn/ui** design patterns/components where the frontend architecture supports them.
3. Use **Tailwind CSS** for styling.
4. Use **glassmorphism** as the visual design language.
5. Keep WooCommerce credentials exclusively server-side.
6. Keep API/business logic in the Frappe backend.
7. Do not place WooCommerce API calls directly inside UI components.
8. Use Zustand actions to communicate with the Frappe API layer.
9. Keep order filtering client-side for the initial implementation.
10. Preserve the selected phase during automatic refresh.
11. Keep the desktop order grid at **6 columns**.
12. Keep the sidebar approximately **20%** of the dashboard width.
13. Use reusable components rather than duplicating UI code.
14. Keep loading, error, empty, and success states centralized.
15. Avoid unnecessary global state; only shared dashboard state belongs in Zustand.

---

# 67. Final Technology Architecture

The complete project architecture is now:

```text
                         ┌───────────────────────┐
                         │      WooCommerce      │
                         │                       │
                         │ Order Fulfillment API │
                         └───────────┬───────────┘
                                     │
                                     │ REST
                                     ▼
                         ┌───────────────────────┐
                         │   WooCommerce Client  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │ Order Fulfillment     │
                         │ Service               │
                         └───────────┬───────────┘
                                     │
                            ┌────────┴────────┐
                            │                 │
                            ▼                 ▼
                     WooCommerce         ERPNext
                       Order Data         Customer
                            │                 │
                            └────────┬────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      Frappe API       │
                         └───────────┬───────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────┐
│                    FRONTEND DASHBOARD                          │
│                                                                │
│                 shadcn/ui Design System                        │
│                          +                                     │
│                     Tailwind CSS                               │
│                          +                                     │
│                   Glassmorphism                                │
│                          +                                     │
│                      Zustand                                   │
│                                                                │
│  ┌─────────────────┐      ┌─────────────────────────────────┐ │
│  │                 │      │                                 │ │
│  │ Glass Sidebar   │      │       Glass Order Grid          │ │
│  │                 │      │                                 │ │
│  │ Dashboard       │      │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ │ │
│  │ All Orders      │      │  │    │ │    │ │    │ │    │ │ │
│  │ Enqueue         │      │  └────┘ └────┘ └────┘ └────┘ │ │
│  │ Picking         │      │                                 │ │
│  │ Sorting         │      │  ┌────┐ ┌────┐ ┌────┐ ┌────┐ │ │
│  │ Checking        │      │  │    │ │    │ │    │ │    │ │ │
│  │ Loading         │      │  └────┘ └────┘ └────┘ └────┘ │ │
│  │                 │      │                                 │ │
│  │     ~20%        │      │          6 Columns              │ │
│  └─────────────────┘      └─────────────────────────────────┘ │
│                                                                │
│                    ~80% Main Content                           │
└────────────────────────────────────────────────────────────────┘
```

### Final frontend stack

**Frappe + Tailwind CSS + shadcn/ui design system + Zustand + Glassmorphism**

This gives us a clean separation:

**Frappe/Python** → integration and business logic
**Frappe API** → communication boundary
**Zustand** → frontend state
**shadcn/ui** → component/design language
**Tailwind** → styling/layout
**Glassmorphism** → visual identity
**WooCommerce** → fulfillment source of truth
**ERPNext** → customer source of truth


# 68. WooCommerce Order Fulfillment API Contract

The Frappe Order Fulfillment Dashboard consumes the custom WordPress/WooCommerce REST API:

```text
GET /wp-json/qgc-erp/v1/order-fulfillment
```

The API provides the fulfillment monitoring data stored in:

```text
bm_order_fulfillment
```

WooCommerce/WordPress is the **source of truth for fulfillment state and phase timing**.

ERPNext is responsible for resolving the corresponding **customer information**.

---

# 69. API Endpoints

## Get All Orders

```text
GET https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment
```

This endpoint retrieves the fulfillment records used by the dashboard.

---

## Get Specific Order

```text
GET https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment?order_id=47375
```

The `order_id` parameter is used to retrieve the fulfillment record for a specific WooCommerce order.

Example:

```text
order_id=47375
```

---

# 70. Actual API Response

The current API returns the following structure:

```json
{
    "success": true,
    "table": "bm_order_fulfillment",
    "total": 1,
    "count": 1,
    "per_page": 100,
    "offset": 0,
    "order": "ASC",
    "rows": [
        {
            "id": "2062",
            "order_id": 47375,
            "current_phase": "enqueueing",
            "created_at": "2026-07-28 16:42:28",
            "enqueueing_start": "2026-07-28 16:42:28",
            "enqueueing_end": null,
            "picking_start": null,
            "picking_end": null,
            "sorting_start": null,
            "sorting_end": null,
            "checking_start": null,
            "checking_end": null,
            "loading_start": null,
            "loading_end": null,
            "enqueueing_elapsed": 0,
            "picking_elapsed": 0,
            "sorting_elapsed": 0,
            "checking_elapsed": 0,
            "loading_elapsed": 0
        }
    ]
}
```

---

# 71. API Response Structure

The top-level response contains:

```text
success
table
total
count
per_page
offset
order
rows
```

The important dashboard data is contained inside:

```text
rows[]
```

Each object inside `rows` represents an order fulfillment record.

---

# 72. Response Metadata

| Field      | Type    | Description                              |
| ---------- | ------- | ---------------------------------------- |
| `success`  | Boolean | Indicates whether the request succeeded  |
| `table`    | String  | Source table containing fulfillment data |
| `total`    | Integer | Total number of matching records         |
| `count`    | Integer | Number of records returned               |
| `per_page` | Integer | Maximum records returned                 |
| `offset`   | Integer | Pagination offset                        |
| `order`    | String  | Sort direction                           |
| `rows`     | Array   | Fulfillment records                      |

The dashboard primarily consumes:

```text
rows[]
```

while the metadata can be used for pagination, counters, and debugging.

---

# 73. Fulfillment Row Structure

Each fulfillment row contains:

```text
id
order_id
current_phase
created_at

enqueueing_start
enqueueing_end

picking_start
picking_end

sorting_start
sorting_end

checking_start
checking_end

loading_start
loading_end

enqueueing_elapsed
picking_elapsed
sorting_elapsed
checking_elapsed
loading_elapsed
```

---

# 74. Fulfillment Record Fields

| Field                | Type           | Description                      |
| -------------------- | -------------- | -------------------------------- |
| `id`                 | String/Integer | Fulfillment record ID            |
| `order_id`           | Integer        | WooCommerce order ID             |
| `current_phase`      | String         | Current fulfillment phase        |
| `created_at`         | Datetime       | Fulfillment record creation time |
| `enqueueing_start`   | Datetime/Null  | Enqueueing start time            |
| `enqueueing_end`     | Datetime/Null  | Enqueueing completion time       |
| `picking_start`      | Datetime/Null  | Picking start time               |
| `picking_end`        | Datetime/Null  | Picking completion time          |
| `sorting_start`      | Datetime/Null  | Sorting start time               |
| `sorting_end`        | Datetime/Null  | Sorting completion time          |
| `checking_start`     | Datetime/Null  | Checking start time              |
| `checking_end`       | Datetime/Null  | Checking completion time         |
| `loading_start`      | Datetime/Null  | Loading start time               |
| `loading_end`        | Datetime/Null  | Loading completion time          |
| `enqueueing_elapsed` | Number         | Enqueueing elapsed time          |
| `picking_elapsed`    | Number         | Picking elapsed time             |
| `sorting_elapsed`    | Number         | Sorting elapsed time             |
| `checking_elapsed`   | Number         | Checking elapsed time            |
| `loading_elapsed`    | Number         | Loading elapsed time             |

---

# 75. Fulfillment Phases

The API currently uses the following phase values:

```text
enqueueing
picking
sorting
checking
loading
```

These should be treated as the canonical backend values.

The frontend can display user-friendly labels:

| API Value    | Display Label |
| ------------ | ------------- |
| `enqueueing` | Enqueue       |
| `picking`    | Picking       |
| `sorting`    | Sorting       |
| `checking`   | Checking      |
| `loading`    | Loading       |

The application should **not modify the backend phase value**.

Instead, it should map the value for presentation.

Example:

```javascript
const PHASE_LABELS = {
    enqueueing: "Enqueue",
    picking: "Picking",
    sorting: "Sorting",
    checking: "Checking",
    loading: "Loading",
};
```

---

# 76. Customer Resolution

The WooCommerce API response does **not** currently contain customer information.

Therefore:

```text
WooCommerce API
      │
      │ order_id = 47375
      ▼
Frappe Backend
      │
      │ Find corresponding customer
      ▼
ERPNext
      │
      ▼
Customer
```

The `order_id` should be used as the reference for resolving the customer.

The exact ERPNext lookup strategy should be determined based on how WooCommerce orders are currently linked to ERPNext customers.

---

# 77. Normalized Backend Response

The frontend should not need to understand the raw WooCommerce response structure.

The Frappe backend should normalize the response into a dashboard-friendly format.

Recommended structure:

```json
{
    "success": true,
    "total": 1,
    "count": 1,
    "orders": [
        {
            "id": "2062",
            "order_id": 47375,
            "current_phase": "enqueueing",
            "created_at": "2026-07-28 16:42:28",

            "customer": {
                "id": "CUST-00001",
                "name": "ABC Construction"
            },

            "phases": {
                "enqueueing": {
                    "start": "2026-07-28 16:42:28",
                    "end": null,
                    "elapsed": 0
                },
                "picking": {
                    "start": null,
                    "end": null,
                    "elapsed": 0
                },
                "sorting": {
                    "start": null,
                    "end": null,
                    "elapsed": 0
                },
                "checking": {
                    "start": null,
                    "end": null,
                    "elapsed": 0
                },
                "loading": {
                    "start": null,
                    "end": null,
                    "elapsed": 0
                }
            }
        }
    ]
}
```

This normalized response is optional, but recommended because it creates a clean contract between the backend and frontend.

---

# 78. Raw vs Normalized Data

The architecture should distinguish between the external API response and frontend data.

```text
                    WooCommerce
                         │
                         ▼
                 RAW API RESPONSE
                         │
                         │
                         ▼
                 Frappe Service
                         │
                 ┌───────┴────────┐
                 │                │
                 ▼                ▼
          Normalize Data     ERPNext Lookup
                 │                │
                 └───────┬────────┘
                         ▼
                 DASHBOARD RESPONSE
                         │
                         ▼
                   Zustand Store
                         │
                         ▼
                  UI Components
```

This prevents the frontend from becoming tightly coupled to the WordPress database/API structure.

---

# 79. Zustand Store Data

The normalized order data should be stored in Zustand.

Conceptually:

```javascript
{
    orders: [
        {
            id: "2062",
            order_id: 47375,
            current_phase: "enqueueing",
            created_at: "2026-07-28 16:42:28",

            customer: {
                id: "CUST-00001",
                name: "ABC Construction"
            },

            phases: {
                enqueueing: {
                    start: "2026-07-28 16:42:28",
                    end: null,
                    elapsed: 0
                },

                picking: {
                    start: null,
                    end: null,
                    elapsed: 0
                },

                sorting: {
                    start: null,
                    end: null,
                    elapsed: 0
                },

                checking: {
                    start: null,
                    end: null,
                    elapsed: 0
                },

                loading: {
                    start: null,
                    end: null,
                    elapsed: 0
                }
            }
        }
    ],

    selectedPhase: "all",
    loading: false,
    error: null,
    lastUpdated: null
}
```

---

# 80. Order Card Data

The initial order card should primarily show:

```text
┌──────────────────────────────┐
│                              │
│  #47375        [ ENQUEUE ]   │
│                              │
│  ABC Construction            │
│                              │
│  Created                     │
│  Jul 28, 2026 04:42 PM       │
│                              │
└──────────────────────────────┘
```

Required fields:

```text
Order ID
Current Phase
Customer
Created At
```

Additional phase timing information can be introduced later.

---

# 81. Phase Timing — Future UI

The API already provides detailed timing information.

For example:

```text
enqueueing_start
enqueueing_end
enqueueing_elapsed
```

This makes it possible to eventually display:

```text
┌──────────────────────────────┐
│ #47375       [ PICKING ]     │
│                              │
│ ABC Construction             │
│                              │
│ Enqueueing       ✓ 02:14     │
│ Picking          ● 05:32     │
│ Sorting          ○ --        │
│ Checking         ○ --        │
│ Loading          ○ --        │
│                              │
└──────────────────────────────┘
```

For the MVP, the card can remain focused on:

```text
Order ID
Customer
Current Phase
Created At
```

The timing information should still be preserved in the backend response so it is available for future functionality.

---

# 82. API Error Contract

The backend should safely handle cases where the WooCommerce API returns an error.

Possible situations:

```text
API unavailable
Authentication failure
Invalid order ID
Empty result
Malformed response
Timeout
Unexpected response
```

The frontend should receive a safe error structure such as:

```json
{
    "success": false,
    "error": {
        "code": "WOOCOMMERCE_API_ERROR",
        "message": "Unable to retrieve order fulfillment data."
    }
}
```

The actual WooCommerce credentials or sensitive backend information must never be exposed.

---

# 83. Empty Result

If no orders match the request:

```json
{
    "success": true,
    "total": 0,
    "count": 0,
    "orders": []
}
```

The dashboard should display an appropriate empty state:

```text
┌─────────────────────────────────┐
│                                 │
│        No orders found          │
│                                 │
│   No orders are currently in   │
│       this fulfillment phase.  │
│                                 │
└─────────────────────────────────┘
```

---

# 84. Pagination

The current API provides:

```text
per_page
offset
total
count
```

Therefore, pagination is supported at the API level.

For the MVP:

```text
per_page = 100
offset = 0
```

can be used initially.

If the number of orders grows beyond the API page size, the service layer should support retrieving subsequent pages.

Future architecture:

```text
Page 1
    ↓
Page 2
    ↓
Page 3
    ↓
...
    ↓
Combined order collection
```

The frontend should not need to understand the WooCommerce pagination implementation.

---

# 85. Updated Data Flow

The complete data flow is now:

```text
┌──────────────────────────┐
│       WooCommerce        │
│                          │
│ bm_order_fulfillment     │
└────────────┬─────────────┘
             │
             │ GET
             ▼
┌──────────────────────────┐
│ Order Fulfillment API    │
│                          │
│ /order-fulfillment       │
└────────────┬─────────────┘
             │
             │ Raw Response
             ▼
┌──────────────────────────┐
│ Frappe WooCommerce       │
│ Client                   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Fulfillment Service      │
│                          │
│ Normalize                │
│ Validate                 │
│ Resolve Customer         │
└────────────┬─────────────┘
             │
             │
       ┌─────┴──────┐
       │            │
       ▼            ▼
 WooCommerce     ERPNext
 Order Data      Customer
       │            │
       └─────┬──────┘
             │
             ▼
┌──────────────────────────┐
│       Frappe API         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Zustand Store       │
│                          │
│ orders                   │
│ selectedPhase            │
│ loading                  │
│ error                    │
│ lastUpdated              │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Dashboard UI         │
│                          │
│ shadcn/ui                │
│ Tailwind CSS             │
│ Glassmorphism            │
└──────────────────────────┘
```

---

# 86. Final Source-of-Truth Model

The project should follow this ownership model:

```text
┌──────────────────────────────────────────┐
│               WOOCOMMERCE                │
│                                          │
│ Order ID                                 │
│ Current Phase                            │
│ Created At                               │
│ Phase Start/End Times                    │
│ Phase Elapsed Times                      │
└───────────────────┬──────────────────────┘
                    │
                    │
                    ▼
┌──────────────────────────────────────────┐
│                 ERPNext                  │
│                                          │
│ Customer                                 │
│ Customer Name                            │
│ Customer Details                         │
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│                  FRAPPE                  │
│                                          │
│ Integration                              │
│ Normalization                            │
│ Authentication                           │
│ API                                      │
│ Dashboard                                │
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│                 ZUSTAND                  │
│                                          │
│ Client-side dashboard state              │
│ Filters                                  │
│ Orders                                   │
│ Loading                                  │
│ Refresh                                  │
└───────────────────┬──────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│                   UI                     │
│                                          │
│ shadcn/ui                                │
│ Tailwind CSS                             │
│ Glassmorphism                            │
└──────────────────────────────────────────┘
```

---

# 87. Updated Core Architecture Rule

The most important integration rule is:

> **WooCommerce provides fulfillment information, ERPNext provides customer information, Frappe performs the integration and normalization, Zustand manages client-side state, and the dashboard presents the combined data.**

This gives the project a clear separation of responsibility and prevents the frontend from becoming dependent on the raw WordPress database response.
