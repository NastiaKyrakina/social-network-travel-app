"""Функции для коректного преобразования типов"""


def from_srt_to_int(value, only_positive=False, max_value=None):
    try:
        value = int(value)
    except ValueError:
        return 'invalid value'

    if only_positive and value <= 0:
        return 'invalid value'

    if max_value and value > max_value:
        return 'invalid value'

    return value


def from_srt_to_float(value, only_positive=False, max_value=None):
    try:
        value = float(value)
    except ValueError:
        return 'invalid value'

    if only_positive and value <= 0:
        return 'invalid value'

    if max_value and value > max_value:
        return 'invalid value'

    return value


def from_dict_to_list(dict_val):
    """из словаря в список кортежей"""
    new_list = []
    for key in dict_val:
        kortege = (key, dict_val[key][0])
        new_list.append(kortege)
    return new_list
