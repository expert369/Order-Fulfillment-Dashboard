from urllib.parse import urlparse

import frappe
from frappe import _
from frappe.model.document import Document


class OrderFulfillmentSettings(Document):
	def validate(self):
		if not self.enabled:
			return

		self.validate_woocommerce_url()
		self.validate_api_path()
		self.validate_credentials()

	def validate_woocommerce_url(self):
		if not self.woocommerce_url:
			frappe.throw(_("WooCommerce URL is required when the integration is enabled."))

		parsed = urlparse(self.woocommerce_url.strip())
		if parsed.scheme not in ("http", "https") or not parsed.netloc:
			frappe.throw(_("WooCommerce URL must be a valid URL starting with http:// or https://."))

	def validate_api_path(self):
		if not self.api_path:
			frappe.throw(_("API Path is required when the integration is enabled."))

		api_path = self.api_path.strip()
		if not api_path.startswith("/"):
			frappe.throw(_("API Path must start with a forward slash (/)"))

	def validate_credentials(self):
		if not self.consumer_key:
			frappe.throw(_("Consumer Key is required when the integration is enabled."))

		if not self.consumer_secret:
			frappe.throw(_("Consumer Secret is required when the integration is enabled."))
