"""Temporary Phase 5 live smoke test — removed after execution."""

import frappe

from order_fulfillment_dashboard.services.order_fulfillment import customer_lookup

CUSTOMER = "T-Smoke-P5-Customer"
SO_NAME = "SO-T-Smoke-P5"
WOO_ID = "77331"
FIELDS = (
	{
		"dt": "Sales Order",
		"fieldname": "custom_woo_job_order_id",
		"fieldtype": "Data",
		"label": "Woo Job Order ID",
		"unique": 1,
		"search_index": 1,
		"read_only": 1,
	},
	{
		"dt": "Sales Order",
		"fieldname": "custom_woo_job_order_no",
		"fieldtype": "Data",
		"label": "Woo Job Order No",
	},
)


def _cleanup_sales_orders():
	names = frappe.db.sql_list(
		"SELECT name FROM `tabSales Order` WHERE name LIKE %s OR customer = %s",
		(f"{SO_NAME}%", CUSTOMER),
	)
	for name in names:
		frappe.delete_doc("Sales Order", name, force=True, ignore_permissions=True)


def debug_fields():
	rows = frappe.db.sql(
		"SELECT name, dt, fieldname FROM `tabCustom Field` WHERE fieldname LIKE 'custom_woo_job_order%%'",
		as_dict=True,
	)
	exists_results = [
		frappe.db.exists("Custom Field", {"dt": "Sales Order", "fieldname": "custom_woo_job_order_id"}),
		frappe.db.exists("Custom Field", {"dt": "Sales Order", "fieldname": "custom_woo_job_order_no"}),
	]
	print(frappe.as_json({"rows": rows, "exists_results": exists_results}))


def delete_fields():
	for field in FIELDS:
		existing = frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]})
		print("EXISTS", existing)
		if existing:
			frappe.delete_doc("Custom Field", existing, force=True, ignore_permissions=True)
	frappe.db.commit()
	print("DELETE_FIELDS_DONE")
	print(
		frappe.as_json(
			{
				"id_column_exists": frappe.db.has_column("Sales Order", "custom_woo_job_order_id"),
				"no_column_exists": frappe.db.has_column("Sales Order", "custom_woo_job_order_no"),
				"rows_after": frappe.db.sql(
					"SELECT name, fieldname FROM `tabCustom Field` WHERE fieldname LIKE 'custom_woo_job_order%%'"
				),
				"error_logs": frappe.db.sql(
					"SELECT name, title, LEFT(error, 300) FROM `tabError Log` WHERE creation > DATE_SUB(NOW(), INTERVAL 10 MINUTE) ORDER BY creation DESC LIMIT 5"
				),
			}
		)
	)


def verify_clean():
	so_rows = frappe.db.sql_list(
		"SELECT name FROM `tabSales Order` WHERE name LIKE %s OR customer = %s",
		(f"{SO_NAME}%", CUSTOMER),
	)
	print(
		frappe.as_json(
			{
				"orphan_sales_orders": so_rows,
				"customer_exists": bool(frappe.db.exists("Customer", CUSTOMER)),
				"id_column_exists": frappe.db.has_column("Sales Order", "custom_woo_job_order_id"),
				"no_column_exists": frappe.db.has_column("Sales Order", "custom_woo_job_order_no"),
			}
		)
	)


def cleanup():
	_cleanup_sales_orders()
	if frappe.db.exists("Customer", CUSTOMER):
		frappe.delete_doc("Customer", CUSTOMER, force=True, ignore_permissions=True)
	for field in FIELDS:
		existing = frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]})
		if existing:
			frappe.delete_doc("Custom Field", existing, force=True, ignore_permissions=True)
	frappe.db.commit()
	print("PHASE5_SMOKE_CLEANUP_DONE")


def run():
	results = {}
	created_so_name = None
	try:
		results["before_columns"] = {
			"has_id_column": frappe.db.has_column("Sales Order", "custom_woo_job_order_id"),
			"has_no_column": frappe.db.has_column("Sales Order", "custom_woo_job_order_no"),
		}

		for field in FIELDS:
			if not frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]}):
				frappe.get_doc({"doctype": "Custom Field", **field}).insert(ignore_permissions=True)
		results["after_columns"] = {
			"has_id_column": frappe.db.has_column("Sales Order", "custom_woo_job_order_id"),
		}

		if not frappe.db.exists("Customer", CUSTOMER):
			frappe.get_doc(
				{
					"doctype": "Customer",
					"customer_name": CUSTOMER,
					"customer_group": "Individual",
					"territory": "All Territories",
				}
			).insert(ignore_permissions=True)

		company = frappe.defaults.get_global_default("company")
		warehouse = frappe.db.get_value("Warehouse", {"company": company, "is_group": 0}, "name")

		so_doc = frappe.get_doc(
			{
				"doctype": "Sales Order",
				"customer": CUSTOMER,
				"company": company,
				"transaction_date": frappe.utils.today(),
				"delivery_date": frappe.utils.today(),
				"items": [
					{
						"item_code": "_Test Item",
						"qty": 1,
						"rate": 100,
						"warehouse": warehouse,
					}
				],
				"custom_woo_job_order_id": WOO_ID,
				"custom_woo_job_order_no": f"JO#{WOO_ID}",
			}
		).insert(ignore_permissions=True)
		created_so_name = so_doc.name
		frappe.db.commit()
		results["created_so"] = created_so_name

		results["resolve_customer_hit"] = customer_lookup.resolve_customer(int(WOO_ID))
		results["resolve_customer_join_no"] = customer_lookup.resolve_customer(f"JO#{WOO_ID}")
		results["resolve_customer_miss"] = customer_lookup.resolve_customer(99999)
		results["resolve_customers_batch"] = customer_lookup.resolve_customers([int(WOO_ID), 99999, None, ""])

		so = frappe.get_doc("Sales Order", created_so_name)
		results["so_customer_matches"] = {"so_customer": so.customer, "so_customer_name": so.customer_name}
	finally:
		cleanup()

	frappe.log_error(title="Phase 5 Smoke Results", message=frappe.as_json(results))
	print("PHASE5_SMOKE", frappe.as_json(results))
	return results