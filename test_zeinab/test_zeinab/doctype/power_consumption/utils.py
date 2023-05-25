import calendar
import datetime
import itertools
import operator
from typing import Dict

import frappe
from frappe import _
from frappe.utils import flt


def is_number(num):
    return isinstance(num, int) or isinstance(num, float)


def calculate_average(key: str, data):
    return sum(flt(it[key]) for it in data) / len(data)


def get_month_and_year_names(date_time: datetime):
    month_number = date_time.month
    month_name = calendar.month_name[month_number]
    year = date_time.year

    return month_name, year


def group_data_by_month_and_year(data):
    output_list = []
    if data:
        for i, g in itertools.groupby(data, key=operator.itemgetter("month", str("year"))):
            output_list.append(list(g))
    return output_list


def validate_link_values(links_dict: Dict):
    for key, value in links_dict.items():
        if not frappe.db.exists(key, value):
            frappe.throw(title=_("Not Found"), msg=_("{} {} doesn't exist".format(key, value)))
