from __future__ import unicode_literals
import frappe
from frappe import _

sitemap = 1

def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw(_("Log in to access this page."), frappe.Redirect)

	return context
