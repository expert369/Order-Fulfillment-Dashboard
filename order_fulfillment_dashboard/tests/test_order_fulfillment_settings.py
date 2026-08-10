import unittest

import frappe


class TestOrderFulfillmentSettings(unittest.TestCase):
	def setUp(self):
		self.settings = frappe.get_doc("Order Fulfillment Settings")
		self.settings.flags.ignore_permissions = True
		self.reset()

	def tearDown(self):
		frappe.db.rollback()

	def reset(self):
		self.settings.enabled = 0
		self.settings.woocommerce_url = ""
		self.settings.consumer_key = ""
		self.settings.consumer_secret = ""
		self.settings.api_path = ""

	def test_disabled_settings_may_be_empty(self):
		self.settings.save()
		self.assertFalse(self.settings.enabled)

	def test_enabled_requires_all_fields(self):
		self.settings.enabled = 1
		with self.assertRaises(frappe.ValidationError):
			self.settings.save()

	def test_enabled_requires_consumer_key(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		self.settings.consumer_secret = "secret"
		with self.assertRaises(frappe.ValidationError):
			self.settings.save()

	def test_enabled_requires_consumer_secret(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		self.settings.consumer_key = "key"
		with self.assertRaises(frappe.ValidationError):
			self.settings.save()

	def test_invalid_url_rejected(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "htp://not-a-url"
		self.settings.consumer_key = "key"
		self.settings.consumer_secret = "secret"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		with self.assertRaises(frappe.ValidationError):
			self.settings.save()

	def test_api_path_must_start_with_slash(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.consumer_key = "key"
		self.settings.consumer_secret = "secret"
		self.settings.api_path = "wp-json/qgc-erp/v1/order-fulfillment"
		with self.assertRaises(frappe.ValidationError):
			self.settings.save()

	def test_valid_configuration_saves(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.consumer_key = "ck_test"
		self.settings.consumer_secret = "cs_test"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		self.settings.save()
		self.assertTrue(self.settings.enabled)

	def test_passwords_are_stored_encrypted(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.consumer_key = "ck_test"
		self.settings.consumer_secret = "cs_test"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		self.settings.save()

		public_value = frappe.db.get_value(
			"Order Fulfillment Settings", "Order Fulfillment Settings", "consumer_key"
		)
		self.assertEqual(public_value, "*******")

		decrypted = frappe.utils.password.get_decrypted_password(
			"Order Fulfillment Settings", "Order Fulfillment Settings", "consumer_key"
		)
		self.assertEqual(decrypted, "ck_test")

	def test_passwords_round_trip_via_get_password(self):
		self.settings.enabled = 1
		self.settings.woocommerce_url = "https://cms-staging.buildmaster.ph"
		self.settings.consumer_key = "ck_test"
		self.settings.consumer_secret = "cs_test"
		self.settings.api_path = "/wp-json/qgc-erp/v1/order-fulfillment"
		self.settings.save()

		doc = frappe.get_doc("Order Fulfillment Settings")
		self.assertEqual(doc.get_password("consumer_key"), "ck_test")
		self.assertEqual(doc.get_password("consumer_secret"), "cs_test")


if __name__ == "__main__":
	unittest.main()
