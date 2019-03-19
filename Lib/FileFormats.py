"""valid file formats"""
from Lib import FFD
from django.utils.translation import ugettext as _

formats_files = {

    FFD.IMAGE: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'],
    FFD.VIDEO: ['mp4', 'ogv'],
    FFD.AUDIO: ['mp3', 'ogg', 'wav'],
    FFD.FILES: ['txt', 'doc', 'docx'],
}

MAX_FILES_SIZE = 10 ** 8
MAX_FILES_COUNT = 10


def check_file_formats(fname, ftype=None):
    """Проверяет валидность формата файла"""
    correct_ext = False
    ext = fname.split('.')[-1]
    if ftype:
        if ext in formats_files[ftype]:
            correct_ext = True
    else:
        for key in formats_files.keys():
            if ext in formats_files[key]:
                correct_ext = True
    return correct_ext


def check_file_size(file):
    if file.size > MAX_FILES_SIZE:
        return False
    return True


def handle_uploaded_file(files_dict):
    errors_file_type = []

    for elem in FFD.FILE_TYPE:
        files = files_dict.getlist(elem[1], None)
        if len(files) > MAX_FILES_COUNT:
            errors_file_type.append(_("To many files"))
        else:
            for file in files:
                if not check_file_formats(file.name, elem[0]):
                    errors_file_type.append(_("don`t support this file extension for image file"))

    return errors_file_type
