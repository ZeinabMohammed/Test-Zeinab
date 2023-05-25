# Copyright (c) 2023, Zeinab Mohammed and contributors
# For license information, please see license.txt
import base64
import io
import json
import mimetypes
from datetime import datetime

import pandas as pd

import frappe
from frappe import _
from frappe.model.document import Document
from test_zeinab.test_zeinab.doctype.power_consumption.utils import calculate_average, get_month_and_year_names, \
    group_data_by_month_and_year, is_number


class PowerConsumption(Document):
    pass


@frappe.whitelist()
def get_file_data(file):
    file_json = json.loads(file)
    data_url = file_json.get("dataurl")
    if "," not in data_url:
        frappe.throw(title=_("Unsupported"), msg=_("Unsupported file format"))

    data = data_url.split(",")
    file_object = file_json.get("name")
    if not valid_excel_type(file_object):
        frappe.throw(_("File should be valid '.xlsx' extension"))  # TODO: Translate error msgs
    _file = read_file(data[1])
    result = extract_data_from_file(_file)
    return result


def valid_excel_type(file_name):
    mimetype = mimetypes.guess_type(file_name)
    file_extension = mimetypes.guess_extension(mimetype[0], strict=False)
    return file_extension in [".xlsx"]


def read_file(data):
    content = base64.b64decode(data)
    readable = io.BytesIO()
    readable.write(content)
    readable.seek(0)  # reset the pointer
    return readable


def extract_data_from_file(file):
    df1 = pd.read_excel(file, engine='openpyxl')

    customer = df1.iloc[0, 1] if not pd.isnull(df1.iloc[0, 1]) else None  # B2
    phone = df1.iloc[1, 1] if not pd.isnull(df1.iloc[1, 1]) else None  # B3
    project = df1.iloc[2, 1] if not pd.isnull(df1.iloc[2, 1]) else None  # B4
    # validate_link_values({"Customer": customer, "Project": project}) TODO: Reactivate after making fields type link

    data_frame = pd.read_excel(file, skiprows=6, engine='openpyxl')  # Skip all rows before dataframe cells
    consumption_data = data_frame.T[:3].to_dict().values()  # records frame starting from row8: A8, B8 and C8
    validate_data_types(consumption_data)

    kw_avg = calculate_average(key='kw', data=consumption_data)
    kwh_avg = calculate_average(key='kwh', data=consumption_data)
    periodic_data = get_periodic_data(consumption_data)

    return {"customer": customer, "phone": phone, "project": project, "consumption_data": consumption_data,
            "kw_avg": kw_avg, "kwh_avg": kwh_avg, "periodic_data": periodic_data}


def validate_data_types(data):
    for element in data:
        if not pd.isnull(element):
            date_time = element['datetime']
            kw = element['kw']
            kwh = element['kwh']
            if not is_number(kw) and kw != '-':
                frappe.throw(_("Invalid data type for  kw {}".format(kw)))
            elif not is_number(kwh) and kwh != '-':
                frappe.throw(_("Invalid data type for  kwh {}".format(kwh)))

            elif not isinstance(date_time, datetime):
                frappe.throw(_("Invalid data type for  datetime {}".format(date_time)))


def get_periodic_data(consumption_data):
    for item in consumption_data:
        item['month'], item['year'] = get_month_and_year_names(item['datetime'])
        item['traffic_type'] = 'low' if (6 > item['datetime'].hour >= 0 or 23 == item['datetime'].hour) else 'high'

    grouped_data_list = group_data_by_month_and_year(consumption_data)
    return get_periodic_details(grouped_data_list)


def get_periodic_details(grouped_data_list):
    periodic_data = []
    for element in grouped_data_list:
        low_traffic_items = [it for it in element if it['traffic_type'] == 'low']
        high_traffic_items = [it for it in element if it['traffic_type'] == 'high']
        low_traffic_kwh_avg = calculate_average('kwh', low_traffic_items)
        high_traffic_kwh_avg = calculate_average('kwh', high_traffic_items)
        total_month_low_traffic = 0.1 * low_traffic_kwh_avg
        total_month_high_traffic = 0.3 * high_traffic_kwh_avg
        periodic_data.append(
            {"month": element[0]['month'], "year": element[0]['year'], "low_traffic": total_month_low_traffic,
             "high_traffic": total_month_high_traffic})
    return periodic_data
