frappe.ready(() => {
	$('#stock-report').empty();
	this.form = new frappe.ui.FieldGroup({
		fields: [
			{
				fieldtype: 'Section Break'
			},
			{
				label: __('Brand'),
				fieldname: 'brand',
				fieldtype: 'Autocomplete',
				options: [],
				reqd: 1,
				change: () => this.get_brand_items(),
			},
			{
				fieldtype: 'Column Break'
			},
			{
				label: __('Item'),
				fieldname: 'item_name',
				fieldtype: 'Autocomplete',
				reqd: 1,
				change: () => this.get_stock_details(),
			},
			{
				fieldtype: 'Column Break'
			},
			{
				label: __('Item Name'),
				fieldname: 'item',
				fieldtype: 'Data',
				read_only: 1,
				default: ' '
			},
			{
				fieldtype: 'Column Break'
			},
			{
				label: __('Required Qty'),
				fieldname: 'required_qty',
				fieldtype: 'Int',
				reqd: 1,
				change: () => this.get_stock_details(),
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'HTML',
				fieldname: 'preview'
			}
		],
		body: $('#stock-report')
	});
	this.form.make();

	this.get_brands = function() {
		let me = this;
		frappe.call({
			method: 'mobility.mobility.api.get_brands',
			callback: function(r) {
				me.form.fields_dict.brand.set_data(r.message);
			}
		});
	}

	this.get_brand_items = function() {
		let me = this;
		me.form.fields_dict.item_name.set_value('');
		me.form.fields_dict.required_qty.set_value('');
		$('#datatable').empty();

		frappe.call({
			method: 'mobility.mobility.api.get_brand_items',
			args: {
				brand: me.form.fields_dict.brand.$input.val()
			},
			callback: function(r) {
				me.form.fields_dict.item_name.set_data(r.message);
			}
		});
	}

	this.get_stock_details = function() {
		let me = this;
		let brand = me.form.fields_dict.brand.$input.val();
		let item = me.form.fields_dict.item_name.$input.val();
		let qty = me.form.fields_dict.required_qty.$input.val();

		if (item) {
			frappe.call({
				method: 'mobility.mobility.api.get_item_name',
				args: {
					'item': item
				},
				callback: function(r) {
					me.form.fields_dict.item.set_value(r.message);
				}
			});
		}

		if (brand && item && qty) {
			frappe.call({
				method: 'mobility.mobility.api.get_stock_details',
				args: {
					'brand': brand,
					'item': item,
					'qty': qty 
				},
				callback: function(r) {
					$('#datatable').html(r.message);
				}
			});
		}
	}
	this.get_brands();
});
