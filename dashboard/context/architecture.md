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
