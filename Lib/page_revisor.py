"""Для отримання та обробки даних Get-a"""


def remove_page(query_string):
    qstring = query_string.split('&')
    qstring = [s for s in qstring if not s.startswith('page')]
    return '&'.join(qstring)
