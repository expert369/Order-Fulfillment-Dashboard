# Order Fulfillment Dashboard

## 1. Project Overview

The **Order Fulfillment Dashboard** is a Frappe application designed to monitor WooCommerce orders as they move through different fulfillment phases.

The system will retrieve order fulfillment data from a WooCommerce/WordPress REST API and display the orders in a monitoring dashboard inside Frappe/ERPNext.

The dashboard will allow users to filter orders by their current fulfillment phase:

* Enqueue
* Picking
* Sorting
* Checking
* Loading

The system will also retrieve the corresponding customer information from ERPNext and display it alongside the WooCommerce order information.

The application will primarily function as a **monitoring dashboard**. WooCommerce remains the source of fulfillment/order data, while ERPNext provides customer information.

---

# 2. Objectives

The main objectives are:

1. Provide a centralized dashboard for monitoring order fulfillment.
2. Retrieve fulfillment status from WooCommerce.
3. Display orders according to their current fulfillment phase.
4. Allow users to filter orders by fulfillment phase.
5. Retrieve customer information from ERPNext.
6. Provide a visual card-based interface suitable for warehouse/operations monitoring.
7. Automatically refresh the dashboard so users can see updated fulfillment statuses.
8. Keep WooCommerce credentials secure on the Frappe backend.

---

# 3. System Architecture

```text
                    WooCommerce / WordPress
                             │
                             │ REST API
                             ▼
                ┌─────────────────────────┐
                │   Frappe Backend        │
                │                         │
                │ WooCommerce API Client  │
                └────────────┬────────────┘
                             │
                    ┌────────┴─────────┐
                    │                  │
                    ▼                  ▼
             WooCommerce Data     ERPNext Customer
                    │                  │
                    └────────┬─────────┘
                             ▼
                ┌─────────────────────────┐
                │ Order Fulfillment       │
                │ Dashboard               │
                │                         │
                │ Sidebar  │ Order Cards  │
                └─────────────────────────┘
```

---

# 4. WooCommerce Integration

The dashboard will retrieve fulfillment information from the following REST API:

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment
```

## Get All Orders

```http
GET /wp-json/qgc-erp/v1/order-fulfillment
```

Full endpoint:

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment
```

## Get Specific Order

A specific order can be retrieved using the `order_id` query parameter.

Example:

```http
GET /wp-json/qgc-erp/v1/order-fulfillment?order_id=47375
```

Full endpoint:

```text
https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment?order_id=47375
```

---

# 5. Authentication

WooCommerce API authentication will use:

* Consumer Key
* Consumer Secret

These credentials must be stored securely in Frappe.

The credentials **must not be exposed to the browser or frontend JavaScript**.

The intended architecture is:

```text
Browser
   │
   │ Frappe API request
   ▼
Frappe Backend
   │
   │ Consumer Key + Consumer Secret
   ▼
WooCommerce REST API
```

---

# 6. Configuration DocType

Create a **Single DocType** named:

```text
Order Fulfillment Settings
```

This DocType will contain the WooCommerce integration configuration.

## Fields

| Field           | Type       | Description                         |
| --------------- | ---------- | ----------------------------------- |
| WooCommerce URL | Data / URL | Base URL of the WooCommerce website |
| Consumer Key    | Password   | WooCommerce API consumer key        |
| Consumer Secret | Password   | WooCommerce API consumer secret     |
| API Path        | Data       | REST API path for order fulfillment |
| Enabled         | Check      | Enables/disables the integration    |

Example configuration:

```text
Order Fulfillment Settings

WooCommerce URL:
https://cms-staging.buildmaster.ph

Consumer Key:
ck_xxxxxxxxxxxxx

Consumer Secret:
cs_xxxxxxxxxxxxx

API Path:
/wp-json/qgc-erp/v1/order-fulfillment

Enabled:
Yes
```

The API path may be made read-only if it should not be changed by regular administrators.

---

# 7. Order Data

The dashboard expects the WooCommerce API to provide information representing the fulfillment status of each order.

The expected conceptual data structure is:

```json
{
    "order_id": 47375,
    "current_phase": "Picking",
    "created_at": "2026-08-10T09:42:00",
    "customer_id": "CUST-00001"
}
```

The actual implementation should adapt to the response structure provided by the existing API.

## Required Order Information

The dashboard needs the following information:

* `order_id`
* `current_phase`
* `created_at`
* Customer

The customer information should come from ERPNext.

---

# 8. ERPNext Customer Lookup

The WooCommerce order information will be combined with ERPNext customer data.

The intended flow is:

```text
WooCommerce Order
       │
       │ customer identifier
       ▼
Frappe Backend
       │
       │ lookup
       ▼
ERPNext Customer
```

The preferred approach is to use a stable customer identifier shared between WooCommerce and ERPNext.

For example:

```json
{
    "order_id": 47375,
    "customer_id": "CUST-00001"
}
```

The Frappe backend can then retrieve the corresponding ERPNext Customer.

If the API currently provides a different customer identifier, the customer lookup logic should be adapted accordingly.

---

# 9. Dashboard

The main interface will be a custom **Frappe Desk Page**.

Suggested page name:

```text
Order Fulfillment Dashboard
```

Suggested route:

```text
/order-fulfillment-dashboard
```

The dashboard will consist of:

```text
┌──────────────────────────────────────────────────────────────┐
│                ORDER FULFILLMENT DASHBOARD                   │
├───────────────────┬──────────────────────────────────────────┤
│                   │                                          │
│     SIDEBAR       │              ORDER CARDS                 │
│                   │                                          │
│ Dashboard         │  ┌──────┐ ┌──────┐ ┌──────┐ ...        │
│                   │  │Order │ │Order │ │Order │             │
│ Enqueue           │  │Card  │ │Card  │ │Card  │             │
│                   │  └──────┘ └──────┘ └──────┘             │
│ Picking           │                                          │
│                   │  ┌──────┐ ┌──────┐ ┌──────┐ ...        │
│ Sorting           │  │Order │ │Order │ │Order │             │
│                   │  │Card  │ │Card  │ │Card  │             │
│ Checking          │  └──────┘ └──────┘ └──────┘             │
│                   │                                          │
│ Loading           │                                          │
│                   │                                          │
└───────────────────┴──────────────────────────────────────────┘
```

---

# 10. Sidebar

The sidebar will be located on the **left side** of the dashboard.

Target width:

```text
20%
```

The dashboard content will occupy approximately:

```text
80%
```

## Sidebar Options

```text
Order Fulfillment

Dashboard

PHASES

All Orders
Enqueue
Picking
Sorting
Checking
Loading
```

The sidebar may also display the number of orders currently in each phase.

Example:

```text
All Orders       125
Enqueue           12
Picking            8
Sorting            5
Checking           7
Loading            3
```

---

# 11. Phase Filtering

Users should be able to filter orders by their current fulfillment phase.

Available phases:

```text
Enqueue
Picking
Sorting
Checking
Loading
```

When the user selects a phase, only orders belonging to that phase should be displayed.

Example:

```text
Picking
```

will display:

```text
current_phase == "Picking"
```

Selecting:

```text
All Orders
```

will display orders from all phases.

Filtering should happen dynamically without requiring a full page reload.

---

# 12. Order Card Grid

Orders will be displayed as cards.

The desktop dashboard should use a **6-column grid**.

```text
grid-template-columns: repeat(6, 1fr);
```

Example:

```text
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ #47375 │ │ #47376 │ │ #47377 │ │ #47378 │ │ #47379 │ │ #47380 │
│ Picking│ │ Enqueue│ │ Sorting│ │Checking│ │ Loading│ │ Picking│
│Customer│ │Customer│ │Customer│ │Customer│ │Customer│ │Customer│
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
```

---

# 13. Responsive Grid

The dashboard should be responsive.

Recommended layout:

| Screen  | Columns |
| ------- | ------: |
| Desktop |       6 |
| Laptop  |       4 |
| Tablet  |       2 |
| Mobile  |       1 |

The sidebar may also be adapted for smaller screens.

---

# 14. Order Card

Each order card should display the following information:

### Order ID

Example:

```text
#47375
```

### Current Phase

Example:

```text
PICKING
```

### Customer

Retrieved from ERPNext.

Example:

```text
Customer
ABC Construction
```

### Created At

Example:

```text
Created
Aug 10, 2026 09:42 AM
```

Example complete card:

```text
┌──────────────────────┐
│ #47375               │
│                      │
│ PICKING              │
│                      │
│ Customer             │
│ ABC Construction     │
│                      │
│ Created              │
│ Aug 10, 2026 09:42   │
└──────────────────────┘
```

---

# 15. Dashboard Refresh

Because the application is intended for order monitoring, the dashboard should automatically refresh.

Recommended initial interval:

```text
30 seconds
```

Flow:

```text
Dashboard
    │
    ▼
Fetch latest orders
    │
    ▼
Process customer information
    │
    ▼
Update cards
    │
    ▼
Wait 30 seconds
    │
    └───────────────► Repeat
```

The dashboard should also provide a manual refresh option.

Example:

```text
Last updated: 10:42:31 AM

[ Refresh ]
```

Optional:

```text
Auto Refresh: ON
```

---

# 16. Backend API Layer

The frontend should communicate with Frappe backend methods rather than directly communicating with WooCommerce.

Suggested API functions:

```python
get_orders()
get_order(order_id)
```

Conceptual flow:

```text
Frontend
   │
   │ frappe.call()
   ▼
Frappe API
   │
   ▼
Order Fulfillment Service
   │
   ▼
WooCommerce API
```

---

# 17. Suggested Application Structure

If the implementation is part of the existing `qgc_erp` app:

```text
qgc_erp/
│
├── qgc_erp/
│   │
│   ├── api/
│   │   └── order_fulfillment.py
│   │
│   ├── services/
│   │   └── order_fulfillment/
│   │       ├── __init__.py
│   │       └── woo_client.py
│   │
│   ├── doctype/
│   │   │
│   │   └── order_fulfillment_settings/
│   │       ├── order_fulfillment_settings.json
│   │       ├── order_fulfillment_settings.py
│   │       └── order_fulfillment_settings.js
│   │
│   └── page/
│       │
│       └── order_fulfillment_dashboard/
│           ├── order_fulfillment_dashboard.json
│           ├── order_fulfillment_dashboard.js
│           └── order_fulfillment_dashboard.html
```

---

# 18. Core Data Flow

```text
1. User opens Order Fulfillment Dashboard
                    │
                    ▼
2. Dashboard calls Frappe backend
                    │
                    ▼
3. Frappe loads Order Fulfillment Settings
                    │
                    ▼
4. Frappe authenticates with WooCommerce
                    │
                    ▼
5. WooCommerce returns fulfillment orders
                    │
                    ▼
6. Frappe processes the order information
                    │
                    ▼
7. Frappe looks up the ERPNext Customer
                    │
                    ▼
8. Combined data is returned to frontend
                    │
                    ▼
9. Dashboard renders order cards
                    │
                    ▼
10. User filters by fulfillment phase
                    │
                    ▼
11. Dashboard displays matching orders
```

---

# 19. Phase Definition

The fulfillment phases should be centrally defined.

Recommended phases:

```python
ORDER_PHASES = [
    "Enqueue",
    "Picking",
    "Sorting",
    "Checking",
    "Loading",
]
```

This avoids having phase names hardcoded in multiple places.

---

# 20. No Order DocType for MVP

The initial implementation should **not create a separate ERPNext DocType for every WooCommerce order**.

The system should use:

```text
Order Fulfillment Settings
```

as the only configuration DocType.

Orders will remain sourced from WooCommerce:

```text
WooCommerce
     │
     ▼
Order Fulfillment API
     │
     ▼
Frappe Dashboard
```

This avoids unnecessary duplication and synchronization problems.

A local Order Fulfillment DocType can be introduced later if historical tracking, reporting, audit logs, or local caching becomes necessary.

---

# 21. Security Requirements

The following security rules should be followed:

1. Consumer Key must not be exposed to the frontend.
2. Consumer Secret must never be exposed to the frontend.
3. WooCommerce requests should be performed server-side.
4. Frappe API methods should have appropriate permission checks.
5. Credentials should use Frappe's Password field type.
6. API errors should not expose credentials.
7. API credentials should not be logged.
8. Only authorized users should access the dashboard and configuration.

---

# 22. Error Handling

The application should gracefully handle:

### WooCommerce API unavailable

Display:

```text
Unable to connect to WooCommerce.
Please try again later.
```

### Invalid credentials

Display:

```text
WooCommerce authentication failed.
Please check the integration settings.
```

### Empty results

Display:

```text
No orders found.
```

### Customer not found

The order should still be displayed.

Example:

```text
Customer
Customer not found
```

The failure to find a customer should not prevent the remaining orders from being displayed.

---

# 23. MVP Features

## Configuration

* [ ] Create Order Fulfillment Settings Single DocType
* [ ] Add WooCommerce URL
* [ ] Add Consumer Key
* [ ] Add Consumer Secret
* [ ] Add API Path
* [ ] Add Enabled field

## WooCommerce Integration

* [ ] Implement WooCommerce API client
* [ ] Fetch all fulfillment orders
* [ ] Fetch specific order
* [ ] Handle authentication
* [ ] Handle API errors
* [ ] Validate API response

## ERPNext Integration

* [ ] Identify customer mapping
* [ ] Retrieve ERPNext Customer
* [ ] Handle missing customers

## Dashboard

* [ ] Create Frappe Desk Page
* [ ] Create left sidebar
* [ ] Sidebar width approximately 20%
* [ ] Create Dashboard option
* [ ] Add Enqueue filter
* [ ] Add Picking filter
* [ ] Add Sorting filter
* [ ] Add Checking filter
* [ ] Add Loading filter
* [ ] Create order cards
* [ ] Implement 6-column desktop grid
* [ ] Display Order ID
* [ ] Display Current Phase
* [ ] Display Created At
* [ ] Display ERPNext Customer

## Monitoring

* [ ] Manual refresh
* [ ] Automatic refresh
* [ ] Last updated indicator
* [ ] Phase order counts

---

# 24. Future Enhancements

Potential features for future versions:

* Order detail modal
* Search by order ID
* Search by customer
* Search by customer name
* Date filtering
* Warehouse filtering
* Fulfillment performance metrics
* Phase duration tracking
* Order aging indicators
* Delayed order alerts
* Sound notifications for new orders
* Real-time updates using WebSockets
* Historical fulfillment reports
* Dashboard analytics
* Order movement history
* Local order caching
* Audit logs

---

# 25. Final MVP Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                     Frappe / ERPNext                         │
│                                                              │
│  ┌─────────────────────┐                                    │
│  │ Order Fulfillment   │                                    │
│  │ Settings            │                                    │
│  │                     │                                    │
│  │ WooCommerce URL     │                                    │
│  │ Consumer Key        │                                    │
│  │ Consumer Secret     │                                    │
│  │ API Path            │                                    │
│  └──────────┬──────────┘                                    │
│             │                                                │
│             ▼                                                │
│  ┌─────────────────────┐                                    │
│  │ WooCommerce API     │                                    │
│  │ Service             │                                    │
│  └──────────┬──────────┘                                    │
│             │                                                │
│             ▼                                                │
│  ┌─────────────────────┐       ┌──────────────────────┐     │
│  │ Fulfillment Orders  │──────►│ ERPNext Customer     │     │
│  └──────────┬──────────┘       └──────────┬───────────┘     │
│             │                             │                 │
│             └──────────────┬──────────────┘                 │
│                            ▼                                 │
│             ┌──────────────────────────────┐                │
│             │ Order Fulfillment Dashboard  │                │
│             │                              │                │
│             │ ┌────────┐ ┌──────────────┐ │                │
│             │ │Sidebar │ │ Order Cards  │ │                │
│             │ │  20%   │ │    80%       │ │                │
│             │ │        │ │              │ │                │
│             │ │All     │ │ 6-column     │ │                │
│             │ │Enqueue │ │ card grid    │ │                │
│             │ │Picking │ │              │ │                │
│             │ │Sorting │ │              │ │                │
│             │ │Checking│ │              │ │                │
│             │ │Loading │ │              │ │                │
│             │ └────────┘ └──────────────┘ │                │
│             └──────────────────────────────┘                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                             │
                             │ REST API
                             ▼
              ┌──────────────────────────────┐
              │ WooCommerce / WordPress      │
              │                              │
              │ /wp-json/qgc-erp/v1/        │
              │ order-fulfillment            │
              └──────────────────────────────┘
```

---

# 26. Project Success Criteria

The project will be considered successful when:

1. An administrator can configure WooCommerce credentials through **Order Fulfillment Settings**.
2. Frappe can successfully authenticate with the WooCommerce API.
3. The dashboard can retrieve fulfillment orders.
4. Orders are displayed in a card-based interface.
5. The dashboard displays six cards per row on desktop.
6. Each card displays:

   * Order ID
   * Current Phase
   * Created At
   * ERPNext Customer
7. Users can filter orders by:

   * Enqueue
   * Picking
   * Sorting
   * Checking
   * Loading
8. The dashboard automatically refreshes.
9. WooCommerce credentials are never exposed to the browser.
10. API failures and missing customer records are handled gracefully.

---

# 27. Implementation Principle

The initial implementation should remain **simple and focused**:

```text
WooCommerce = Order / Fulfillment Source
ERPNext      = Customer Source
Frappe       = Integration + Dashboard
```

The dashboard should not unnecessarily duplicate WooCommerce order data inside ERPNext unless a future requirement for historical records, reporting, or synchronization makes local storage necessary.
