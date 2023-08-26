# -*- coding: utf-8 -*-

import os, argparse
from functools import reduce

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_directory_structure(rootdir, show_sys_files=False, blacklist=[]):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    Modified by: David Cheng
    Orginal by: Andrew Clark (http://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/)
    """
    dir, rootdir, start = {}, rootdir.rstrip(os.sep), rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        if not show_sys_files:
            files, dirs[:] = [f for f in files if f[0] != '.' and f not in blacklist], [d for d in dirs if d[0] != '.' and d not in blacklist]

        folders, subdir = path[start:].split(os.sep), dict.fromkeys(files)
        parent, parent[folders[-1]] = reduce(dict.get, folders[:-1], dir), subdir
    return dir


def create_tree(current_dict, top_dir, prefix="", sort_alpha=True):
    if not current_dict:
        return ""
    keys = list(current_dict.keys())
    output = ""
    if sort_alpha:
        keys.sort(key=lambda x: x[0].lower())

    for i, item in enumerate(keys):
        last = True if i == len(keys) - 1 and item != top_dir else False; connector = '' if item == top_dir else '└── ' if last else '├── '; nextPrefix = prefix + ('' if item == top_dir else '│   ' if not last else '    '); new_row = create_tree(current_dict[item], top_dir, prefix=nextPrefix, sort_alpha=sort_alpha)
    
        output += prefix + connector + item + '\n' + new_row
    return output

def add_comment(output):
    new_output = ""
    output_split, padding = output.split('\n')[:-1], max([len(x) for x in output_split]) + 10
    for x in output_split:
        new_output += x + (padding - len(x)) * " " + "#\n"
    return new_output

def main():
    argument_specs = [
        ('-f', 'file', str, ".", 1, 'Root directory. Default: .'),
        ('-t', 'text_file_name', str, "README_FILE_STRUCTURE.txt", 1, 'Text file save name. Default: README_FILE_STRUCTURE.txt'),
        ('-b', 'blacklist', str, [], '+', "Names of files/directories to blacklist. Default: []"),
        ('-s', 'include_system_files', str2bool, False, 1, "Include system files (.) Default: False"),
        ('-a', 'sort_alpha', str2bool, True, 1, "Sort files alphabetically. If set to False, will order in natural progression."),
        ('-c', 'comment_fields', str2bool, True, 1, "Add comment fields for each file")
    ]
    parser = argparse.ArgumentParser(description='Creates easy to read file structure text file.')
    for arg_spec in argument_specs:
        flag, dest, type_, default, nargs, help_text = arg_spec
        parser.add_argument(flag, dest=dest, type=type_, default=default, nargs=nargs, help=help_text)
    args = parser.parse_args()
    file_dict, output = get_directory_structure(args.file[0], show_sys_files=args.include_system_files[0], blacklist=args.blacklist), create_tree(file_dict, list(file_dict.keys())[0], sort_alpha=args.sort_alpha[0])
    if args.comment_fields[0]:
        output = add_comment(output)
    path = args.file[0] + '/' + args.text_file_name[0]
    with open(path, "w") as text_file:
        text_file.write(output)
    print("Saved to " + path)

if __name__ == "__main__":
    main()
