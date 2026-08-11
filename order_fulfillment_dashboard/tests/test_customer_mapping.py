import unittest
from unittest.mock import patch

import frappe

from order_fulfillment_dashboard.services.order_fulfillment import customer_lookup


def sample_so_row(woo_id, name="SO-00001", customer="CUST-00001", customer_name="ABC Construction"):
	return {
		"woo_id": woo_id,
		"name": name,
		"customer": customer,
		"customer_name": customer_name,
	}


class TestResolveCustomer(unittest.TestCase):
	@patch.object(frappe.db, "has_column", return_value=True)
	def test_resolves_via_primary_field(self, mock_has_column):
		with patch.object(
			frappe.db,
			"sql",
			return_value=[sample_so_row("47375")],
		):
			result = customer_lookup.resolve_customer(47375)

		self.assertEqual(result, {"id": "CUST-00001", "name": "ABC Construction"})

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_falls_back_to_order_number(self, mock_has_column):
		with patch.object(
			frappe.db,
			"sql",
			side_effect=[[], [sample_so_row("JO#102", name="SO-00002")]],
		):
			result = customer_lookup.resolve_customer("JO#102")

		self.assertEqual(result, {"id": "CUST-00001", "name": "ABC Construction"})

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_not_found_returns_none(self, mock_has_column):
		with patch.object(frappe.db, "sql", return_value=[]):
			self.assertIsNone(customer_lookup.resolve_customer("999999"))

	def test_none_order_id_returns_none(self):
		self.assertIsNone(customer_lookup.resolve_customer(None))

	def test_empty_order_id_returns_none(self):
		self.assertIsNone(customer_lookup.resolve_customer(""))


class TestResolveCustomers(unittest.TestCase):
	@patch.object(frappe.db, "has_column", return_value=True)
	def test_batch_mapping_keyed_by_string_order_id(self, mock_has_column):
		rows = [
			sample_so_row("47375"),
			sample_so_row("47376", name="SO-00003", customer="CUST-00002", customer_name="XYZ Corp"),
		]
		with patch.object(frappe.db, "sql", return_value=rows):
			result = customer_lookup.resolve_customers([47375, 47376])

		self.assertEqual(
			result,
			{
				"47375": {"id": "CUST-00001", "name": "ABC Construction"},
				"47376": {"id": "CUST-00002", "name": "XYZ Corp"},
			},
		)

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_skips_empty_and_none_ids(self, mock_has_column):
		with patch.object(frappe.db, "sql", return_value=[]) as mock_sql:
			result = customer_lookup.resolve_customers([None, "", "  ", 47375])

		self.assertEqual(result, {})
		self.assertEqual(mock_sql.call_count, 2)

	def test_no_ids_returns_empty_without_query(self):
		with patch.object(frappe.db, "sql", return_value=[]) as mock_sql:
			self.assertEqual(customer_lookup.resolve_customers([]), {})
			mock_sql.assert_not_called()

	@patch.object(frappe.db, "has_column", return_value=False)
	def test_missing_column_returns_empty(self, mock_has_column):
		with patch.object(frappe.db, "sql", return_value=[]) as mock_sql:
			result = customer_lookup.resolve_customers([47375])

		self.assertEqual(result, {})
		mock_sql.assert_not_called()

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_query_failure_logged_and_returns_empty(self, mock_has_column):
		with patch.object(frappe.db, "sql", side_effect=frappe.DataError("column does not exist")):
			with patch.object(customer_lookup.frappe, "log_error") as mock_log:
				result = customer_lookup.resolve_customers([47375])

		self.assertEqual(result, {})
		mock_log.assert_called_once()

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_primary_hits_skip_fallback_query(self, mock_has_column):
		rows = [sample_so_row("47375")]
		with patch.object(frappe.db, "sql", return_value=rows) as mock_sql:
			result = customer_lookup.resolve_customers([47375])

		self.assertEqual(len(result), 1)
		self.assertEqual(mock_sql.call_count, 1)

	@patch.object(frappe.db, "has_column", return_value=True)
	def test_queries_are_chunked(self, mock_has_column):
		ids = [str(index) for index in range(1, 502)]
		rows = [sample_so_row(order_id) for order_id in ids]
		with patch.object(frappe.db, "sql", return_value=rows) as mock_sql:
			customer_lookup.resolve_customers(ids)

		self.assertEqual(mock_sql.call_count, 2)
		first_chunk = mock_sql.call_args_list[0][0][1][0]
		second_chunk = mock_sql.call_args_list[1][0][1][0]
		self.assertEqual(len(first_chunk), 500)
		self.assertEqual(len(second_chunk), 1)


if __name__ == "__main__":
	unittest.main()
