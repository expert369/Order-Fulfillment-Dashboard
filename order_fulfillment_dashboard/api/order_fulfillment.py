import frappe
from frappe import _
from frappe.utils import cstr

from order_fulfillment_dashboard.services.order_fulfillment import customer_lookup, woo_client

PHASE_FIELDS = ("enqueueing", "picking", "sorting", "checking", "loading")


@frappe.whitelist(allow_guest=True)
def get_orders():
	_check_permission()

	try:
		orders = woo_client.get_orders()
	except Exception as error:
		return _handle_error(error)

	customer_map = customer_lookup.resolve_customers([order.get("order_id") for order in orders])

	normalized_orders = []
	for order in orders:
		normalized = _normalize_order(order)
		normalized["customer"] = customer_map.get(cstr(order.get("order_id")))
		normalized_orders.append(normalized)
  
	return {
		"success": True,
		"total": len(normalized_orders),
		"count": len(normalized_orders),
		"orders": normalized_orders,
	}


@frappe.whitelist(allow_guest=True)
def get_order(order_id):
	_check_permission()

	if not order_id:
		return _error("INVALID_REQUEST", _("An order ID is required."))

	try:
		order = woo_client.get_order(order_id)
	except Exception as error:
		return _handle_error(error)

	normalized = _normalize_order(order) if order else None
	if normalized:
		normalized["customer"] = customer_lookup.resolve_customer(order_id)

	return {"success": True, "order": normalized}


def _check_permission():
	if frappe.session.user == "Guest":
		frappe.throw(
			_("Authentication is required to access order fulfillment data."), frappe.PermissionError
		)


def _handle_error(error):
	if isinstance(error, woo_client.IntegrationDisabledError):
		return _error("INTEGRATION_DISABLED", _("WooCommerce integration is disabled."))

	if isinstance(error, woo_client.IntegrationNotConfiguredError):
		return _error("INTEGRATION_NOT_CONFIGURED", _("WooCommerce integration is not fully configured."))

	if isinstance(error, woo_client.WooCommerceConnectionError):
		return _error(
			"WOOCOMMERCE_CONNECTION_ERROR",
			_("Unable to connect to WooCommerce. Please try again later."),
		)

	if isinstance(error, woo_client.WooCommerceAuthenticationError):
		return _error(
			"WOOCOMMERCE_AUTHENTICATION_ERROR",
			_("WooCommerce authentication failed. Please check the integration settings."),
		)

	if isinstance(error, woo_client.WooCommerceAPIError):
		return _error("WOOCOMMERCE_API_ERROR", _("WooCommerce returned an error. Please try again later."))

	if isinstance(error, woo_client.WooCommerceInvalidResponseError):
		return _error(
			"WOOCOMMERCE_INVALID_RESPONSE",
			_("WooCommerce returned an unexpected response. Please try again later."),
		)

	frappe.log_error(f"Order Fulfillment API: {error}", "Order Fulfillment API")
	return _error("INTERNAL_ERROR", _("An unexpected error occurred. Please try again later."))


def _normalize_order(order):
	return {
		"id": order.get("id"),
		"order_id": order.get("order_id"),
		"current_phase": order.get("current_phase"),
		"created_at": order.get("created_at"),
		"customer": None,
		"phases": {
			phase: {
				"start": order.get(f"{phase}_start"),
				"end": order.get(f"{phase}_end"),
				"elapsed": order.get(f"{phase}_elapsed"),
			}
			for phase in PHASE_FIELDS
		},
	}


def _error(code, message):
	return {"success": False, "error": {"code": code, "message": message}}
