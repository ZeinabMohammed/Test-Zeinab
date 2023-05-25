// Copyright (c) 2023, Zeinab Mohammed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Power Consumption', {
	upload_entries: function (frm, cdt, cdn) {
		new frappe.ui.FileUploader({
			as_dataurl: true,
			allow_multiple: false,
			on_success(file) {
				frappe.call({
                    url: "/api/method/test_zeinab.test_zeinab.doctype.power_consumption.power_consumption.get_file_data",
                    args:{'file':file},
                    callback: (response) => {
                        let response_data = response.message;
                        console.log(response.message)
                        update_form_fields(frm, response_data)
			        }

		        });
	        },


        });
    }
});

function update_form_fields(frm, response_data){
    frm.doc.customer = response_data.customer;
    frm.doc.project = response_data.project;
    frm.doc.phone = response_data.phone;
    frm.doc.average_kw = response_data.kw_avg;
    frm.doc.average_kwh = response_data.kwh_avg;
    frm.clear_table("power_consumption");
    response_data.consumption_data.forEach(function (element) {
        var row = frm.add_child("power_consumption");
        row.datetime = element.datetime;
        row.kw = element.kw;
        row.kwh = element.kwh;
    });
    response_data.periodic_data.forEach(function (item) {
        let child = frm.add_child("periodic_power_consumption_details");
        child.month = item.month;
        child.year = item.year;
        child.low_traffic = item.low_traffic;
        child.high_traffic = item.high_traffic;
    });
    frm.refresh_fields();
}