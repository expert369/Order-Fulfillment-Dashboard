import unittest
from types import SimpleNamespace
from unittest.mock import patch

import frappe

from order_fulfillment_dashboard.services.order_fulfillment import woo_client


def fake_settings(enabled=True, url="https://cms-staging.buildmaster.ph", key="ck", secret="cs"):
	settings = SimpleNamespace(
		enabled=enabled,
		woocommerce_url=url,
		api_path="/wp-json/qgc-erp/v1/order-fulfillment",
		consumer_key=key,
		consumer_secret=secret,
	)
	settings.get_password = lambda fieldname: key if fieldname == "consumer_key" else secret
	return settings


class TestWooClient(unittest.TestCase):
	def setUp(self):
		self.settings = fake_settings()
		self.patcher = patch.object(woo_client, "get_settings", return_value=self.settings)
		self.mock_settings = self.patcher.start()

	def tearDown(self):
		self.patcher.stop()

	def _fake_response(self, status_code=200, payload=None, raw=None):
		response = SimpleNamespace(status_code=status_code, json=lambda: payload)
		return response

	def test_get_orders_returns_list(self):
		with patch("requests.request", return_value=self._fake_response(payload=[{"order_id": 1}])) as mock:
			orders = woo_client.get_orders()
		self.assertEqual(orders, [{"order_id": 1}])
		_, kwargs = mock.call_args
		self.assertEqual(kwargs["auth"], ("ck", "cs"))
		self.assertEqual(kwargs["params"], None)

	def test_uses_settings_url_and_path(self):
		with patch("requests.request", return_value=self._fake_response(payload=[])) as mock:
			woo_client.get_orders()
		url = mock.call_args[0][1]
		self.assertEqual(url, "https://cms-staging.buildmaster.ph/wp-json/qgc-erp/v1/order-fulfillment")

	def test_get_order_passes_order_id(self):
		with patch(
			"requests.request", return_value=self._fake_response(payload=[{"order_id": 47375}])
		) as mock:
			order = woo_client.get_order(47375)
		self.assertEqual(order, {"order_id": 47375})
		self.assertEqual(mock.call_args[1]["params"], {"order_id": 47375})

	def test_get_order_empty_result_returns_none(self):
		with patch("requests.request", return_value=self._fake_response(payload=[])):
			self.assertIsNone(woo_client.get_order(999))

	def test_accepts_orders_key(self):
		with patch(
			"requests.request", return_value=self._fake_response(payload={"orders": [{"order_id": 1}]})
		):
			self.assertEqual(woo_client.get_orders(), [{"order_id": 1}])

	def test_accepts_data_key(self):
		with patch("requests.request", return_value=self._fake_response(payload={"data": [{"order_id": 1}]})):
			self.assertEqual(woo_client.get_orders(), [{"order_id": 1}])

	def test_accepts_results_key(self):
		with patch(
			"requests.request", return_value=self._fake_response(payload={"results": [{"order_id": 1}]})
		):
			self.assertEqual(woo_client.get_orders(), [{"order_id": 1}])

	def test_unexpected_structure_raises(self):
		with patch("requests.request", return_value=self._fake_response(payload={"foo": "bar"})):
			with self.assertRaises(woo_client.WooCommerceInvalidResponseError):
				woo_client.get_orders()

	def test_scalar_response_raises(self):
		with patch("requests.request", return_value=self._fake_response(payload="nope")):
			with self.assertRaises(woo_client.WooCommerceInvalidResponseError):
				woo_client.get_orders()

	def test_invalid_json_raises(self):
		with patch("requests.request", return_value=self._fake_response(raw="not json")) as mock:
			response = SimpleNamespace(status_code=200)
			response.json = lambda: (_ for _ in ()).throw(ValueError("No JSON"))
			mock.return_value = response
			with self.assertRaises(woo_client.WooCommerceInvalidResponseError):
				woo_client.get_orders()

	def test_unauthorized_raises_auth_error(self):
		with patch("requests.request", return_value=self._fake_response(status_code=401)):
			with self.assertRaises(woo_client.WooCommerceAuthenticationError):
				woo_client.get_orders()

	def test_forbidden_raises_auth_error(self):
		with patch("requests.request", return_value=self._fake_response(status_code=403)):
			with self.assertRaises(woo_client.WooCommerceAuthenticationError):
				woo_client.get_orders()

	def test_server_error_raises_api_error(self):
		with patch("requests.request", return_value=self._fake_response(status_code=502)):
			with self.assertRaises(woo_client.WooCommerceAPIError):
				woo_client.get_orders()

	def test_not_found_raises_api_error(self):
		with patch("requests.request", return_value=self._fake_response(status_code=404)):
			with self.assertRaises(woo_client.WooCommerceAPIError):
				woo_client.get_orders()

	def test_timeout_raises_connection_error(self):
		with patch("requests.request", side_effect=requests_exception("Timeout")):
			with self.assertRaises(woo_client.WooCommerceConnectionError):
				woo_client.get_orders()

	def test_connection_failure_raises_connection_error(self):
		with patch("requests.request", side_effect=requests_exception("ConnectionError")):
			with self.assertRaises(woo_client.WooCommerceConnectionError):
				woo_client.get_orders()

	def test_authentication_uses_credentials_not_url(self):
		with patch("requests.request", return_value=self._fake_response(payload=[])) as mock:
			woo_client.get_orders()
		url = mock.call_args[0][1]
		self.assertNotIn("ck", url)
		self.assertNotIn("cs", url)


def requests_exception(name):
	import requests

	if name == "Timeout":
		return requests.exceptions.Timeout("timed out")
	return requests.exceptions.ConnectionError("connection refused")


class TestGetSettings(unittest.TestCase):
	def setUp(self):
		settings = frappe.get_doc("Order Fulfillment Settings")
		settings.flags.ignore_permissions = True
		settings.enabled = 0
		settings.woocommerce_url = ""
		settings.consumer_key = ""
		settings.consumer_secret = ""
		settings.api_path = ""
		settings.save()

	def tearDown(self):
		frappe.db.rollback()

	def test_disabled_integration_raises(self):
		with self.assertRaises(woo_client.IntegrationDisabledError):
			woo_client.get_settings()

	def test_configured_integration_returns_settings(self):
		settings = frappe.get_doc("Order Fulfillment Settings")
		settings.flags.ignore_permissions = True
		settings.enabled = 1
		settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		settings.consumer_key = "ck_live"
		settings.consumer_secret = "cs_live"
		settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		settings.save()

		result = woo_client.get_settings()
		self.assertEqual(result.name, "Order Fulfillment Settings")
		self.assertTrue(result.enabled)
		self.assertEqual(result.get_password("consumer_key"), "ck_live")


if __name__ == "__main__":
	unittest.main()
