from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from itertools import zip_longest
import re
import glob
import os
import sys
import xml.etree.ElementTree as ET
import math
from datetime import datetime
import shutil
from taf.sbts.oam.coam.admin import admin
import functools
from retrying import retry
from taf.transport.ssh.exceptions import ConnectFailedError
import time
from pathlib import Path
from heapq import nlargest
import ExcelLib
import pprint as pp

admin = admin()


def gnb_admin_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            admin.connect_to()
            return func(*args, **kwargs)
        finally:
            admin.teardown()
    return wrapper


def add_list_entries(list):
    """
    This method takes the list as an input which is a list of list.
    Adds the entries w.r.t its position and returns the sum.
    """
    int_nested = [[int(item) for item in sublist] for sublist in list]
    res = [sum((i)) for i in zip_longest(*int_nested, fillvalue=0)]
    print(res)
    return res


def merge_dictionaries(dict1, dict2):
    """
    This method merges both the input dictionaries which are passed.
    The resultant is also a dictionary
    """
    dict1.update(dict2)
    print(dict1)
    return dict1


def sum_of_list_entries(list):
    """
    This method takes the list as an input which is a list.
    Adds the entries w.r.t its position and returns the sum.
    """
    total = sum(list)
    print(total)
    return total


def cell_kpi_data(counter_list, counter_value_list):
    result = [list(col) for col in zip_longest(*counter_value_list, fillvalue=0)]
    cell_list = []
    for index in result:
        nums = [int(x) for x in index]
        first = sum(nums[:87])
        sec = sum((nums[87:]))
        if first == 0:
            a = "NA"
        else:
            a = round(((100 * (first - sec)) / first), 2)
        cell_list.append(a)
    return cell_list


GNB_KPI = ['NR_592a', 'NR_5094a', 'NR_5095a', 'NR_2193c']
CELL_KPI = [
    'NR_1400c', 'NR_1401b', 'NR_1402c', 'NR_1403d', 'NR_2153d',
    'NR_5054a', 'NR_5054b', 'NR_5056b', 'NR_5056d', 'NR_5128c',
    'NR_5504b', 'NR_5513', 'NR_5513b', 'NR_5054d']
custom_pet_kpi = ['NR_592a']


def map_to_cell_or_gnb(pm_file, overall_kpi_data):
    kpi_data = []
    cell_len = 0
    cell_kpi_status = False
    gnb_kpi_status = False
    for kpi, value in overall_kpi_data.items():
        per_kpi = {}
        per_kpi['PM_FILE'] = pm_file
        per_kpi['KPI_TYPE'] = kpi
        if kpi in GNB_KPI:
            per_kpi['MRBTS'] = value[0]
        if kpi in CELL_KPI:
            for i in range(len(value)):
                per_kpi['CELL-' + str(i + 1)] = value[i]
        kpi_data.append(per_kpi)
    # print(kpi_data)
    return kpi_data


def map_bler_data(bler_list, kpi):
    cell_info = ''
    avg_bler = round(sum(bler_list)/len(bler_list), 2)
    for i in range(0, len(bler_list)):
        if float(bler_list[i]) > 0.5:
            cell_info = cell_info+'CELL-'+str(i+1)+', '
    return (avg_bler, cell_info)


def process_all_kpi(kpi_details, kpi_list, pm_file, duration, exec_dir):
    overall_kpi_data = {}
    missing_counter_dict = {}
    missing_counters = []
    for kpi_data, counter_list in kpi_details.items():
        pattern = r"NR_[a-zA-Z0-9]+"
        match = re.search(pattern, kpi_data)
        if match:
            kpi = match.group(0)
            if kpi in kpi_list:
                if kpi in custom_pet_kpi:
                    kpi = 'PET_'+kpi
                counter_data, missing_counters = fetch_counters_from_PM_file(pm_file, counter_list)
                # pp.pprint(counter_data)
                mapped_values_comprehension = {
                    counter_list: counter_data
                    for counter_list, counter_data in zip(counter_list, counter_data)
                }
                # pp.pprint(mapped_values_comprehension)
                if kpi in sys.modules[__name__].__dict__ and callable(sys.modules[__name__].__dict__[kpi]):
                    func = sys.modules[__name__].__dict__[kpi]
                    overall_kpi_data[kpi] = func(counter_data, counter_list, duration)
                else:
                    print(f"Warning: No callable function found for KPI: {kpi}")
    missing_counter_dict['PM_FILE'] = pm_file
    missing_counter_dict['Missing_counters'] = missing_counters
    kpi_data = map_to_cell_or_gnb(pm_file, overall_kpi_data)

    return_data = {}
    return_data['PM_file'] = pm_file
    for kpi, values in overall_kpi_data.items():
        if kpi in CELL_KPI:
            value_str = ''
            for i in range(len(values)):
                value_str = value_str + 'CEll-' + str(i + 1) + ' : ' + str(values[i]) + ' '
            return_data[kpi] = value_str
        else:
            return_data[kpi] = 'MRBTS : '+str(values[0])
    excel = ExcelLib.ExcelLib()
    excel.create_exl_add_data(kpi_data, missing_counter_dict, exec_dir)
    print(return_data)
    return return_data


def fetch_counters_from_PM_file(pm_file, counter_list):
    '''input being a PM file, the function fetches the counter values
    from the PM file and also returns a list of missing counters
    these missing counters are appended with empty values'''
    counter_data = []
    missing_counters = []
    with open(pm_file, 'r', encoding='utf-8') as file:
        file_content = file.read()
    for counter in counter_list:
        pattern = r'<' + counter + r'>(\d+)</' + counter + r'>'
        counter_values = re.findall(pattern, file_content)
        if len(counter_values) == 0:
            counter_data.append(['not_found'])
            missing_counters.append(counter)
        else:
            counter_data.append(counter_values)
    max_len = max(len(sub) for sub in counter_data)
    final_list = append_with_zero(counter_data, max_len)
    return final_list, missing_counters


def append_with_zero(counter_data, max_len):
    '''appends the list of missing counetrs with zeros'''
    final_list = []
    for entry in counter_data:
        if 'not_found' in entry:
            final_list.append([0] * max_len)
        else:
            final_list.append(entry)
    return final_list


def NR_5054b(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5054b
    Date Modified: 10/02/2026
    BY: Anjana
    """
    cell_kpi = cell_kpi_data(counter_list, counter_value_list)
    # print(cell_kpi)
    return cell_kpi


def NR_5056d(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5056b
    Date Modified: 10/02/2026
    BY: Anjana
    """
    cell_kpi = cell_kpi_data(counter_list, counter_value_list)
    # print(cell_kpi)
    return cell_kpi


def sum_group(counter_group, sum_dict, range_index):
    """
    Author: anjana.kulkarni@nokia.com
    Date Modified: 20/03/2025

    Sums up values from a dictionary for keys generated using a list of prefixes
    and a range of suffixes.

    Args:
        counter_group (list): A list of string prefixes to generate keys.
        sum_dict (dict): A dictionary containing keys and their respective values.
        range_index (int): The range of suffixes to append to prefixes (from 0 to range_index - 1).

    Returns:
        int: The total sum of values corresponding to the generated keys.

    Example:
        counter_group = ["M55302C"]
        sum_dict = {"M55302C00": 10, "M55302C01": 20, "M55302C02": 30}
        range_index = 3

        total = sum_group(counter_group, sum_dict, range_index)
        print(total)  # Output: 60
    """
    group_total = 0
    for prefix in counter_group:
        for suffix in range(range_index):
            sum = f"{prefix}{suffix:02}"  # Generate key with prefix and two-digit suffixif sum in sum_dict
            if sum in sum_dict:
                group_total += sum_dict[sum]  # Add value from dictionaryelse:
            else:
                print(f"Key not found: {sum}")  # Print missing key for debuggingreturn group_total
    return group_total


def NR_5056b(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5056b
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(summed_data, 'M55302C000', 29)
    sum_group_B = sum_of_specific_index(summed_data, 'M55302C060', 28)
    sum_group_C = sum_of_specific_index(summed_data, 'M55302C110', 28)
    sum_group_D = sum_of_specific_index(summed_data, 'M55302C040', 29)
    sum_group_E = sum_of_specific_index(summed_data, 'M55302C080', 28)
    sum_group_F = sum_of_specific_index(summed_data, 'M55302C130', 28)
    # print(sum_group_A, sum_group_B, sum_group_C, sum_group_D)
    group_A = [a + b + c for a, b, c in zip(sum_group_A, sum_group_B, sum_group_C)]
    group_B = [a + b + c for a, b, c in zip(sum_group_D, sum_group_E, sum_group_F)]
    result = []
    for i in range(0, len(group_A)):
        if group_A[i] == 0:
            result.append('NA')
        else:
            result.append(round(100*(group_A[i]-group_B[i])/group_A[i], 2))
    return result


def NR_5054d(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5054d
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(summed_data, 'M55300C000', 29)
    sum_group_B = sum_of_specific_index(summed_data, 'M55300C040', 28)
    sum_group_C = sum_of_specific_index(summed_data, 'M55366C010', 29)
    sum_group_D = sum_of_specific_index(summed_data, 'M55401C000', 29, 1)
    sum_group_E = sum_of_specific_index(summed_data, 'M55300C010', 29)
    sum_group_F = sum_of_specific_index(summed_data, 'M55300C050', 28)
    sum_group_G = sum_of_specific_index(summed_data, 'M55366C020', 29)
    sum_group_H = sum_of_specific_index(summed_data, 'M55401C000', 55, 28)
    group_A = [a + b + c + d for a, b, c, d in zip(sum_group_A, sum_group_B, sum_group_C, sum_group_D)]
    group_B = [a + b + c + d for a, b, c, d in zip(sum_group_E, sum_group_F, sum_group_G, sum_group_H)]
    result = []
    avg_bler = 0
    for i in range(0, len(group_A)):
        if group_A[i] == 0:
            result.append('NA')
        else:
            result.append(round((100*(group_A[i] - group_B[i])/group_A[i]), 2))
    return result


def NR_5094a(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5094a
    BY: Rahul
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(summed_data, 'M55319C120', 21, 1)
    result = []
    sum_group_B = summed_data["M55319C00001"]
    for i in range(len(sum_group_A)):
        if int(sum_group_B[i]) == 0:
            result.append('NA')
        else:
            result.append(round((8 * sum_group_A[i])/(1000 * int(sum_group_B[i])), 2))
    # print(result)
    return result


def NR_5095a(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5095a
    BY: Rahul
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(summed_data, 'M55319C160', 21, 1)
    result = []
    sum_group_B = summed_data["M55319C00001"]
    for i in range(len(sum_group_A)):
        if int(sum_group_B[i]) == 0:
            result.append('NA')
        else:
            result.append(round((8 * sum_group_A[i])/(1000 * int(sum_group_B[i])), 2))
    # print(result)
    return result


def NR_5128c(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5128c
    Date Modified: 30/04/2025
    BY: Rahul
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    data = summed_data["M55138C00008"]
    result = []
    for i in range(len(data)):
        result.append(round(int(data[i])/(duration*60), 2))
    # print(result)
    return result


def get_specific_entries(d: dict, keys_to_get: list) -> dict:
    """
    Returns a new dictionary containing only the key-value pairs
    for the specified keys.
    """
    result = {}
    for key in keys_to_get:
        if key in d:
            result[key] = d[key]
    return result


def sum_of_specific_index(summed_data, counter, index, x=0):
    selected_keys = []
    sum_group = []
    for i in range(x, index):  # M55300C00000 to M55300C00028
        # print(f"in is {i}")
        key = counter+f'{i:02d}'
        selected_keys.append(key)
    dict_to_sum = get_specific_entries(summed_data, selected_keys)
    sum_group = sum_of_list(dict_to_sum)
    # print(sum_group)
    return sum_group


def NR_5054a(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5054a
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    # print(summed_data)
    sum_group_A = sum_of_specific_index(summed_data, 'M55300C000', 29)
    sum_group_B = sum_of_specific_index(summed_data, 'M55300C040', 28)
    sum_group_C = sum_of_specific_index(summed_data, 'M55300C010', 29)
    sum_group_D = sum_of_specific_index(summed_data, 'M55300C050', 28)
    # print(sum_group_A, sum_group_B, sum_group_C, sum_group_D)
    group_A = [a + b for a, b in zip(sum_group_A, sum_group_B)]
    group_B = [a + b for a, b in zip(sum_group_C, sum_group_D)]
    result = []
    for i in range(0, len(group_A)):
        if group_A[i] == 0:
            result.append('NA')
        else:
            result.append(round(100 * (group_A[i]-group_B[i])/group_A[i], 2))
    return result


def NR_2193c(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_2193c
    Date Modified: 25/03/2025
    BY: Anjana
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    result = []
    final_sum_list = sum_of_list(summed_data)
    result.append(round((sum(final_sum_list))/(int(duration) * 60), 2))
    # print(result)
    return result


def NR_2153d(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_2153d
    Date Modified: 25/03/2025
    BY: Anjana
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    result = []
    final_sum_list = sum_of_list(summed_data)
    for index_entries in final_sum_list:
        result.append(round(int(index_entries)/(int(duration) * 60), 2))
    # print(result)
    return result


def sum_of_list(summed_data):
    list_length = len(next(iter(summed_data.values())))
    # print(list_length)
    final_sum_list = [0] * list_length
    fill_value = '0'
    for key, current_list in summed_data.items():
        if len(current_list) < list_length:
            num_zeros_to_add = list_length - len(current_list)
            current_list.extend([fill_value] * num_zeros_to_add)
            summed_data[key] = current_list

    for item_list in summed_data.values():
        for i in range(list_length):
            final_sum_list[i] += int(item_list[i])
    return final_sum_list


def NR_1400c(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_1400c
    Date Modified: 25/03/2025
    BY: Anjana
    """
    result = []
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    final_sum_list = sum_of_list(summed_data)
    for i in final_sum_list:
        result.append(round(i/(int(duration)*60), 2))
    return result


def NR_1401b(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_1401b
    Date Modified: 25/03/2025
    BY: Anjana
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    result = []
    for kpi, values in summed_data.items():
        for index_entries in values:
            result.append(round(int(index_entries)/(int(duration) * 60), 2))
    # print(result)
    return result


def NR_1402c(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_1402c
    Date Modified: 25/03/2025
    BY: Anjana
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    result = []
    final_sum_list = sum_of_list(summed_data)
    for index_entries in final_sum_list:
        result.append(round(int(index_entries)/(int(duration) * 60), 2))
    # print(result)
    return result


def NR_1403d(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_1403d
    Date Modified: 25/03/2025
    BY: Anjana
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    result = []
    final_sum_list = sum_of_list(summed_data)
    for index_entries in final_sum_list:
        result.append(round(int(index_entries)/(int(duration) * 60), 2))
    # print(result)
    return result


def PET_NR_592a(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_592a
    Date Modified: 25/03/2025
    BY: Anjana
    this KPI is a customised ask from
    PET team to divide by the period * 60
    to make it per sec
    """
    custom_output = []
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    output = (summed_data["M55119C01501"])
    for i in output:
        custom_output.append(int(i)/(int(duration)*60))
    return custom_output


def convert_lists_to_dictionary(counter_list, counter_value_list):
    new_dict = dict(zip(counter_list, counter_value_list))
    # print(new_dict)
    # summed_data = {key: sum(values) for key, values in new_dict.items()}
    # return summed_data
    return new_dict


def get_nr_tput(cell_stats_nr, dir="DL"):
    """
    Parses NR throughput (DL or UL) per cell from stats text.
    dir: 'dl' for Downlink, 'ul' for Uplink
    Returns a dict: {cell_id: tput_kbps}
    """
    result = {}
    for line in cell_stats_nr.splitlines():
        match = re.match(r'^\s*(\d+)\s+[\d.]+\s+kbps\s+([\d.]+)\s+kbps\s+([\d.]+)\s+kbps\s+([\d.]+)\s+kbps', line)
        if match:
            cid = int(match.group(1))
            if dir == "UL":
                tput_kbps = float(match.group(2))
            elif dir == "DL":
                tput_kbps = float(match.group(4))
            else:
                raise ValueError("Invalid throughput direction: use 'DL' or 'UL'")
            result[cid] = tput_kbps
    return result


def NR_5513(counter_value_list, counter_list, duration):
    """
    Pairing Ration Calculation
    By : Anjana
    """
    result = []
    sd = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(sd, 'M55308C340', 12, 1)

    for i in range(len(sum_group_A)):
        sum_group_B = (
            sum_group_A[i]
            + int(sd['M55308C34016'][i])
            + int(sd['M55308C34017'][i])
            + int(sd['M55308C34018'][i])
            + int(sd['M55308C34019'][i])
            + int(sd['M55308C34020'][i])
            + int(sd['M55308C34021'][i])
            + int(sd['M55308C34022'][i])
            + int(sd['M55308C34023'][i])
        )

        if math.isclose(sum_group_B, 0.0, abs_tol=1e-6):
            result.append('NA')
        else:
            result.append(
                round((
                    1 * int(sd['M55308C34001'][i]) +
                    2 * (int(sd['M55308C34002'][i]) + int(sd['M55308C34005'][i])) +
                    3 * (int(sd['M55308C34003'][i]) + int(sd['M55308C34006'][i])) +
                    4 * (int(sd['M55308C34004'][i]) + int(sd['M55308C34007'][i])) +
                    5 * int(sd['M55308C34008'][i]) + 6 * int(sd['M55308C34009'][i]) +
                    7 * int(sd['M55308C34010'][i]) + 8 * int(sd['M55308C34011'][i]) +
                    9 * int(sd['M55308C34016'][i]) + 10 * int(sd['M55308C34017'][i]) +
                    11 * int(sd['M55308C34018'][i]) + 12 * int(sd['M55308C34019'][i]) +
                    13 * int(sd['M55308C34020'][i]) + 14 * int(sd['M55308C34021'][i]) +
                    15 * int(sd['M55308C34022'][i]) + 16 * int(sd['M55308C34023'][i])) /
                    sum_group_B, 2)
                )
    return result


def calculate_formula(exp, a, b):
    """
    Expression calculation. Where exp is the expression passed, a and b are the args that are to be
    calculated
    By : Anjana
    """
    formatted_expression = exp.format(a=a, b=b)
    # print(formatted_expression)
    result = eval(formatted_expression)
    print(result)
    return result


def find_string_between_multiple_files(folder_path, filename_pattern, start_str, end_str):
    """
    Find the detach string from multiple egate_console files
    By : Anjana
    """
    folder = Path(folder_path)
    files = list(folder.glob(filename_pattern))
    target_file = "final_egate_console.log"
    target_file = Path(folder_path) / target_file
    if not files:
        raise Exception("No matching files found!")
    matching_files = [p for p in files if p.is_file()]
    latest_files = sorted(matching_files, key=lambda p: p.stat().st_ctime)
    with open(target_file, "wb") as out_f:
        for f in latest_files:
            with open(f, "rb") as in_f:
                shutil.copyfileobj(in_f, out_f)
    found = False
    start_token = 'entry=' + start_str
    with open(target_file, 'r') as f:
        content = f.read()

    entry_idx = content.find(start_token)
    if entry_idx == -1:
        return False  # Skip if entry point not found

        # Slice content from entry point onward
    sliced_content = content[entry_idx + len(start_token):]

    # Search for target string only in sliced content
    target_idx = sliced_content.find(end_str)
    if target_idx != -1:
        found = True
    print(found)
    return found


def find_in_same_file(folder_path, end_str):
    file_name = 'egate_console.log'
    final_file = os.path.join(folder_path, file_name)
    with open(final_file, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if end_str in line:
                return True
    return False


def download_update_and_upload_vendor_file_to_gnb(vendor_filepath='/home/ute'):
    """
    Downloads, Modifies and uploads the vendor file
    By : Anjana
    """
    original_vendor_filepath = os.path.join(vendor_filepath, 'vendor_original.xml')
    modified_vendor_filepath = os.path.join(vendor_filepath, 'vendor_modified.xml')
    print('downloading the vendor file')
    get_vendor_file(original_vendor_filepath)
    print('updating the vendor file')
    shutil.copyfile(original_vendor_filepath, modified_vendor_filepath)
    update_vendor_file(modified_vendor_filepath,
                       {'xEc': '14'})
    upload_vendor_file(modified_vendor_filepath)


@gnb_admin_connection
def get_vendor_file(download_filepath):
    """
    Gets the vendor file via TAF call
    By : Anjana
    """
    vendor_download_response = admin.download_vendor_file(download_filepath)
    print("vendor_download_response:", vendor_download_response)


@gnb_admin_connection
def update_vendor_file(file_path, param_updates):
    """
    Parses the vendor file and modifies the required param
    By : Anjana
    """
    # Parse the XML file
    ns = "raml21.xsd"
    ET.register_namespace('', ns)
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Find and update the parameters
    path = "{ns}cmData//{ns}managedObject[@class='NRBTS']//{ns}p[@name='{name}']"
    for param in param_updates.keys():
        param_list = tree.find(path.format(ns="{" + ns + "}", name=param))
        print("Before update the value at the xml file for {} : {}".format(param, param_list.text))
        param_list.text = param_updates[param]
        print("New value updated at the xml file for {} : {}".format(param, param_list.text))
    # Write the updated XML back to the file
    tree.write(file_path)


@gnb_admin_connection
def upload_vendor_file(modified_vendor_filepath, scf_path="/home/ute/", scf_timeout=60):
    """
    Uploads the vendor file, post modification to gNB
    By : Anjana
    """
    build_id = os.environ.get("BUILD_NUMBER", "0")
    scf_file_name = f"scf_{build_id}.xml"
    scf_dir_path = admin.get_current_scf_file(local_dir_path=scf_path,
                                              file_name=scf_file_name,
                                              timeout=scf_timeout)
    for _ in range(10):
        try:
            print('uploading the vendor file')
            vendor_output = admin.set_vendor_file(modified_vendor_filepath)
            print(f"Vendor file upload output: {vendor_output}")
            time.sleep(180)
            commision_output = admin.perform_commissioning(scf_file=scf_dir_path,
                                                           skip_parameter_relation_errors=True,
                                                           should_activate=True, timeout=300)
            print(f"Full commissioning output {commision_output}")
            return
        except Exception as e:
            print(f"ADMIN API Commissioning failed due to {repr(e)}")
            time.sleep(60)
    raise CommisioningFailure("Commisioning Failed")


def NR_5504b(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5056d
    BY: kushal.j
    """
    summed_data = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(summed_data, 'M55308C350', 5, 1)
    result = []
    for i in range(0, len(sum_group_A)):
        sum_group_B = (
            int(sum_group_A[i])
            + int(summed_data['M55308C36009'][i])
            + int(summed_data['M55308C36010'][i])
            + int(summed_data['M55308C36011'][i])
            + int(summed_data['M55308C36012'][i])
        )
        if math.isclose(sum_group_B, 0.0, abs_tol=1e-6):
            result.append('NA')
        else:
            result.append(
                round((
                    1 * int(summed_data['M55308C35001'][i]) +
                    2 * int(summed_data['M55308C35002'][i]) + int(summed_data['M55308C35003'][i]) +
                    3 * int(summed_data['M55308C35004'][i]) +
                    4 * int(summed_data['M55308C35005'][i]) +
                    5 * int(summed_data['M55308C36009'][i]) +
                    6 * int(summed_data['M55308C36010'][i]) +
                    7 * int(summed_data['M55308C36011'][i]) +
                    8 * int(summed_data['M55308C36012'][i])) /
                    sum_group_B, 2)
                )
    # print(result)
    return result


def NR_5513b(counter_value_list, counter_list, duration):
    """
    KPI Calculation for NR_5503b
    BY: kushal.j
    """
    result = []
    sd = convert_lists_to_dictionary(counter_list, counter_value_list)
    sum_group_A = sum_of_specific_index(sd, 'M55308C340', 12, 1)
    for i in range(len(sum_group_A)):
        sum_group_B = (
            sum_group_A[i]
            + int(sd['M55308C34016'][i])
            + int(sd['M55308C34017'][i])
            + int(sd['M55308C34018'][i])
            + int(sd['M55308C34019'][i])
            + int(sd['M55308C34020'][i])
            + int(sd['M55308C34021'][i])
            + int(sd['M55308C34022'][i])
            + int(sd['M55308C34023'][i])
        )
        if math.isclose(sum_group_B, 0.0, abs_tol=1e-6):
            result.append('NA')
        else:
            result.append(
                round((
                    1 * int(sd['M55308C34001'][i]) +
                    2 * (int(sd['M55308C34002'][i]) + int(sd['M55308C34005'][i])) +
                    3 * (int(sd['M55308C34003'][i]) + int(sd['M55308C34006'][i])) +
                    4 * (int(sd['M55308C34004'][i]) + int(sd['M55308C34007'][i])) +
                    5 * int(sd['M55308C34008'][i]) + 6 * int(sd['M55308C34009'][i]) +
                    7 * int(sd['M55308C34010'][i]) + 8 * int(sd['M55308C34011'][i]) +
                    9 * int(sd['M55308C34016'][i]) + 10 * int(sd['M55308C34017'][i]) +
                    11 * int(sd['M55308C34018'][i]) + 12 * int(sd['M55308C34019'][i]) +
                    13 * int(sd['M55308C34020'][i]) + 14 * int(sd['M55308C34021'][i]) +
                    15 * int(sd['M55308C34022'][i]) + 16 * int(sd['M55308C34023'][i])) /
                    sum_group_B, 2)
            )
    return result
