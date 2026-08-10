# Order Fulfillment Dashboard — Build Plan

## 1. Project Goal

Build a Frappe/ERPNext Order Fulfillment Dashboard that retrieves fulfillment order data from WooCommerce and displays it as a real-time monitoring interface.

The dashboard will support:

* WooCommerce API integration
* Secure API configuration
* ERPNext customer lookup
* Fulfillment phase filtering
* 6-column order card grid
* Automatic refresh
* Manual refresh
* Phase counts
* Error handling

---

# 2. Implementation Strategy

The project will be implemented in the following order:

```text
Phase 1
Project Foundation
        ↓
Phase 2
Configuration
        ↓
Phase 3
WooCommerce API Client
        ↓
Phase 4
Frappe Backend API
        ↓
Phase 5
ERPNext Customer Mapping
        ↓
Phase 6
Dashboard Foundation
        ↓
Phase 7
Order Cards
        ↓
Phase 8
Filtering
        ↓
Phase 9
Auto Refresh
        ↓
Phase 10
Error Handling
        ↓
Phase 11
Testing
        ↓
Phase 12
Deployment
```

---

# 3. Phase 1 — Project Foundation

## Objective

Prepare the Frappe app structure for the Order Fulfillment feature.

### Tasks

* [ ] Confirm target Frappe app
* [ ] Confirm Frappe/ERPNext version
* [ ] Determine dashboard page name
* [ ] Determine module name
* [ ] Create required directory structure
* [ ] Confirm required Frappe permissions
* [ ] Confirm existing app conventions

### Expected Structure

```text
qgc_erp/
│
├── qgc_erp/
│   ├── api/
│   │   └── order_fulfillment.py
│   │
│   ├── services/
│   │   └── order_fulfillment/
│   │       ├── __init__.py
│   │       └── woo_client.py
│   │
│   ├── doctype/
│   │   └── order_fulfillment_settings/
│   │
│   └── page/
│       └── order_fulfillment_dashboard/
```

### Deliverable

A clean project structure ready for implementation.

---

# 4. Phase 2 — Order Fulfillment Settings

## Objective

Create the Single DocType used to configure the WooCommerce integration.

### DocType

```text
Order Fulfillment Settings
```

### Fields

* [ ] WooCommerce URL
* [ ] Consumer Key
* [ ] Consumer Secret
* [ ] API Path
* [ ] Enabled

### Security

* [ ] Consumer Key stored securely
* [ ] Consumer Secret stored as Password field
* [ ] Credentials never exposed to frontend
* [ ] Configuration permissions reviewed

### Validation

* [ ] Required fields validated
* [ ] URL validated
* [ ] API path validated
* [ ] Disabled integration handled correctly

### Deliverable

An administrator can configure the WooCommerce integration from Frappe.

---

# 5. Phase 3 — WooCommerce API Client

## Objective

Create a backend service responsible for communicating with WooCommerce.

### API

Base URL:

```text
https://cms-staging.buildmaster.ph
```

Endpoint:

```text
/wp-json/qgc-erp/v1/order-fulfillment
```

### Functions

Implement:

```python
get_orders()
get_order(order_id)
```

### Tasks

* [ ] Load integration settings
* [ ] Build API URL
* [ ] Authenticate request
* [ ] Request order list
* [ ] Request specific order
* [ ] Parse response
* [ ] Handle HTTP errors
* [ ] Handle timeout
* [ ] Handle malformed response
* [ ] Prevent credential logging

### Deliverable

A reusable Python service capable of retrieving WooCommerce fulfillment data.

---

# 6. Phase 4 — Frappe Backend API

## Objective

Expose safe backend methods to the dashboard.

### Suggested Methods

```python
get_orders()
get_order(order_id)
```

### Tasks

* [ ] Create Frappe API module
* [ ] Add whitelisted methods
* [ ] Validate user permissions
* [ ] Call WooCommerce service
* [ ] Return normalized response
* [ ] Handle backend exceptions
* [ ] Avoid exposing credentials

### Desired Flow

```text
Dashboard
    │
    │ frappe.call()
    ▼
Frappe API
    │
    ▼
WooCommerce Service
    │
    ▼
WooCommerce
```

### Deliverable

The frontend can safely request fulfillment data through Frappe.

---

# 7. Phase 5 — ERPNext Customer Mapping

## Objective

Connect WooCommerce orders to ERPNext Customers.

### Tasks

* [ ] Determine WooCommerce customer identifier
* [ ] Determine ERPNext customer identifier
* [ ] Confirm mapping strategy
* [ ] Implement customer lookup
* [ ] Handle missing customer
* [ ] Handle invalid customer
* [ ] Include customer information in normalized response

### Preferred Data Flow

```text
WooCommerce Order
       │
       │ customer_id
       ▼
Frappe
       │
       ▼
ERPNext Customer
```

### Deliverable

Every order returned to the dashboard contains customer information where available.

---

# 8. Phase 6 — Dashboard Foundation

## Objective

Create the Frappe Desk Page and establish the main layout.

### Page

```text
Order Fulfillment Dashboard
```

### Layout

```text
┌──────────────────────────────────────────────────────┐
│                  Dashboard Header                    │
├──────────────┬───────────────────────────────────────┤
│              │                                       │
│   Sidebar    │             Main Content              │
│    ~20%      │               ~80%                    │
│              │                                       │
└──────────────┴───────────────────────────────────────┘
```

### Tasks

* [ ] Create Frappe page
* [ ] Create HTML structure
* [ ] Create CSS
* [ ] Create sidebar
* [ ] Set sidebar width to approximately 20%
* [ ] Set content width to approximately 80%
* [ ] Add dashboard header
* [ ] Add loading state
* [ ] Add empty state

### Deliverable

A working dashboard shell without order data.

---

# 9. Phase 7 — Order Cards

## Objective

Display WooCommerce orders as cards.

### Card Data

Each card must contain:

```text
Order ID
Current Phase
Customer
Created At
```

### Tasks

* [ ] Create order card component
* [ ] Display order ID
* [ ] Display current phase
* [ ] Display customer
* [ ] Display created date
* [ ] Format date/time
* [ ] Handle missing customer
* [ ] Handle missing fields
* [ ] Create card hover state
* [ ] Create loading state

### Grid

Desktop:

```text
6 columns
```

Responsive:

```text
Desktop    → 6
Laptop     → 4
Tablet     → 2
Mobile     → 1
```

### Deliverable

The dashboard displays actual WooCommerce orders as cards.

---

# 10. Phase 8 — Sidebar Filtering

## Objective

Allow users to filter orders by fulfillment phase.

### Filters

```text
All Orders
Enqueue
Picking
Sorting
Checking
Loading
```

### Tasks

* [ ] Create filter buttons
* [ ] Implement All Orders
* [ ] Implement Enqueue
* [ ] Implement Picking
* [ ] Implement Sorting
* [ ] Implement Checking
* [ ] Implement Loading
* [ ] Highlight active filter
* [ ] Update card grid dynamically
* [ ] Add order count per phase

### Expected Behavior

```text
User clicks Picking
        ↓
Filter orders
        ↓
current_phase === "Picking"
        ↓
Render matching cards
```

### Deliverable

Users can instantly switch between fulfillment phases.

---

# 11. Phase 9 — Refresh System

## Objective

Keep the monitoring dashboard updated.

### Manual Refresh

* [ ] Add Refresh button
* [ ] Display loading state
* [ ] Fetch latest data
* [ ] Update cards
* [ ] Update phase counts

### Automatic Refresh

Initial interval:

```text
30 seconds
```

### Tasks

* [ ] Implement polling
* [ ] Prevent overlapping requests
* [ ] Preserve active filter
* [ ] Update card data
* [ ] Update counts
* [ ] Update last refreshed time

### Display

```text
Last updated:
10:42:31 AM

[ Refresh ]
```

### Deliverable

The dashboard continuously monitors fulfillment changes.

---

# 12. Phase 10 — Error Handling

## Objective

Make the dashboard resilient to integration problems.

### Handle

* [ ] WooCommerce unavailable
* [ ] Authentication failure
* [ ] Invalid API response
* [ ] Timeout
* [ ] Empty order list
* [ ] Missing customer
* [ ] Missing order fields
* [ ] Frappe backend failure
* [ ] Permission errors

### Example Messages

```text
Unable to connect to WooCommerce.
Please try again later.
```

```text
WooCommerce authentication failed.
Please check the integration settings.
```

```text
No orders found.
```

```text
Customer information unavailable.
```

### Deliverable

The dashboard fails gracefully without breaking the entire page.

---

# 13. Phase 11 — UI/UX Improvements

## Objective

Make the dashboard usable for warehouse/operations staff.

### Tasks

* [ ] Improve card styling
* [ ] Add phase visual indicators
* [ ] Improve typography
* [ ] Improve spacing
* [ ] Add card hover state
* [ ] Improve sidebar navigation
* [ ] Add active filter indicator
* [ ] Add loading indicator
* [ ] Add empty state
* [ ] Add error state
* [ ] Add last updated indicator
* [ ] Verify responsive behavior

### Optional

* [ ] Full-screen mode
* [ ] Dark mode
* [ ] Sound notification
* [ ] New order animation

---

# 14. Phase 12 — Testing

## Backend Testing

* [ ] Settings can be saved
* [ ] Credentials are stored securely
* [ ] WooCommerce connection works
* [ ] All orders can be retrieved
* [ ] Specific order can be retrieved
* [ ] API errors are handled
* [ ] Invalid credentials are handled
* [ ] Customer lookup works
* [ ] Missing customers are handled

## Frontend Testing

* [ ] Dashboard loads
* [ ] Orders render
* [ ] Cards display correctly
* [ ] 6-column grid works
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

## Responsive Testing

* [ ] Desktop
* [ ] Laptop
* [ ] Tablet
* [ ] Mobile

---

# 15. Phase 13 — Deployment

## Tasks

* [ ] Commit changes
* [ ] Run Frappe migrations
* [ ] Build assets
* [ ] Clear cache
* [ ] Restart required services
* [ ] Configure production settings
* [ ] Configure WooCommerce credentials
* [ ] Verify API connectivity
* [ ] Verify dashboard
* [ ] Verify permissions
* [ ] Verify automatic refresh

### Suggested Commands

```bash
bench migrate
bench build --app qgc_erp
bench clear-cache
```

Use the appropriate deployment/restart commands for the production environment.

---

# 16. Definition of Done

The feature is considered complete when:

* [ ] Configuration DocType works
* [ ] WooCommerce API integration works
* [ ] ERPNext customer mapping works
* [ ] Dashboard is accessible from Frappe Desk
* [ ] Sidebar works
* [ ] Phase filtering works
* [ ] Orders display as cards
* [ ] Desktop uses 6 columns
* [ ] Customer is displayed
* [ ] Order ID is displayed
* [ ] Current phase is displayed
* [ ] Created date is displayed
* [ ] Manual refresh works
* [ ] Automatic refresh works
* [ ] Error handling works
* [ ] Permissions are verified
* [ ] Production deployment succeeds

---

# 17. Future Scope

The following features are intentionally outside the MVP:

* Historical order storage
* Fulfillment history
* Order phase duration
* Analytics
* Performance reports
* Delayed order alerts
* WebSocket real-time updates
* Advanced search
* Warehouse filtering
* Date filtering
* Order detail modal
* Audit trail
* Notifications

These should only be implemented after the core monitoring dashboard is stable.
