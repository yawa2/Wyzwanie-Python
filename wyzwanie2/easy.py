import sys
import os

MAX_BAR_LENGTH = 50


def get_files_extensions_dict(path_to_directory, files_extensions_dict):

    directory_contents = os.scandir(path_to_directory)
    for entry in directory_contents:
        if entry.is_dir() is True:
            get_files_extensions_dict(entry.path, files_extensions_dict)
        else:
            update_extensions_info(entry, files_extensions_dict)


def update_extensions_info(entry, files_extensions_dict):
    extension = check_entry_extension(entry)
    if extension in files_extensions_dict:
        files_extensions_dict[extension][0] += 1
        files_extensions_dict[extension][1] += entry.stat().st_size
    else:
        files_extensions_dict[extension] = [1, entry.stat().st_size]


def check_entry_extension(entry):
    return entry.name.split(".")[-1]


def sum_files_count(files_extensions_dict):
    files_sum = 0
    for entry in files_extensions_dict:
        files_sum += files_extensions_dict.get(entry)[0]
    return files_sum


def write_histogram_to_file(files_extensions_dict, file_name):
    file = open(file_name, mode="w+")
    draw_histogram(files_extensions_dict, file)
    file.close()


def draw_histogram(files_extensions_dict, file):
    files_count = sum_files_count(files_extensions_dict)
    for entry in files_extensions_dict:

        percentage = files_extensions_dict.get(entry)[0]/files_count
        bar_length = round(percentage * MAX_BAR_LENGTH)
        bar = "#" * bar_length

        file.write("{0: >5}{1: >14}B{2: >60}\n".format(entry, files_extensions_dict.get(entry)[1], bar))


files = {}
get_files_extensions_dict(sys.argv[1], files)
write_histogram_to_file(files, sys.argv[2])

