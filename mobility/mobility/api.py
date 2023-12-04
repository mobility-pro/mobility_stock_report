from werkzeug.wrappers import Response

import frappe
from frappe import _

@frappe.whitelist()
def get_brands():
	brands = frappe.db.get_all('Brand', pluck='name')
	return brands

@frappe.whitelist()
def get_brand_items(brand):
	r = frappe.db.sql('''SELECT DISTINCT i.item_code AS item_code, i.item_name AS item_name FROM ((`tabItem` i
		INNER JOIN `tabBin` b ON i.item_code = b.item_code
		AND i.brand = '{0}')
		INNER JOIN `tabWarehouse` w ON b.warehouse = w.name
		AND w.show_on_portal = 1)'''.format(brand), as_dict=True)
	items = []
	for d in r:
		items.append({
			'label': d.item_code,
			'value': d.item_code
		})

	return items

@frappe.whitelist()
def get_item_name(item):
	return frappe.db.get_value('Item', item, 'item_name')

@frappe.whitelist()
def get_stock_details(brand, item, qty):
	frappe.get_doc({
		'doctype': 'Stock Report Log',
		'brand': brand,
		'item': item,
		'qty': qty,
		'user': frappe.session.user
	}).insert(ignore_permissions=True)

	warehouse = frappe.db.get_all('Warehouse', filters={'show_on_portal': 1}, pluck='name')
	bins = frappe.db.get_all('Bin', filters={'item_code': item, 'warehouse': ['in', warehouse]}, fields=['item_code', 'actual_qty', 'warehouse'])

	if len(bins) == 1:
		if bins[0].actual_qty == frappe.utils.flt(0):
			return ''

	response = '''<table class="table table-striped">
		<thead>
			<tr>
			<th scope="col">Sr No.</th>
			<th scope="col">{0}</th>
			<th scope="col">{1}</th>
			</tr>
		</thead>
		<tbody>'''.format(_('Warehouse'), _('Required Stock Status'))

	for idx,row in enumerate(bins):
		stock_status = ''
		if row.actual_qty >= frappe.utils.flt(qty):
			stock_status = _('Available')
		elif row.actual_qty == frappe.utils.flt(0):
			stock_status = _('Not Available')
		else:
			stock_status = _('Not Enough ( {0} Units )').format(row.actual_qty)
		response += '''<tr>
			<th scope="row">{0}</th>
			<td>{1}</td>
			<td>{2}</td>
			</tr>'''.format(idx+1, row.warehouse, stock_status)
	response += '''</tbody>
		</table>'''
	return response