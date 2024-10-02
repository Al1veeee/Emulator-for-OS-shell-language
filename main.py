import tarfile
import sys
import argparse
import csv
from datetime import datetime
import calendar

def delete_symbol(path):
    for letter in path:
        if letter == "/":
            path = path[1:]
        else:
            break
    return path

def log_action(logfile, action, result):
    with open(logfile, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action, result])

def ls(path, files, folder=None):
    path = delete_symbol(path)
    items = set()

    for file in files:
        if folder:
            if folder in file.name:
                file_names = file.name[len(folder):].split("/")
            else:
                continue
        else:
            if path in file.name:
                file_names = file.name[len(path):].split("/")
            else:
                continue

        file_names = list(filter(None, file_names))
        if len(file_names) > 1 or not file_names:
            continue
        items.add(file_names[0])

    for item in sorted(items):
        print("\033[33m{}\033[0m".format(item))

def cd(path, extension_path, files):
    global local_path
    flag = False
    for file in files:
        if file.name.startswith(local_path + extension_path):
            flag = True
            break
    if "root:" in extension_path:
        path = extension_path[len("root:"):]
    else:
        if extension_path == "~":
            path = ""
        else:
            path += extension_path + "/"
    path = delete_symbol(path)

    if path == "":
        local_path = ""
        return True

    if ".." in path:
        tmp = local_path.split("/")[:-1]
        if len(tmp) == 1 and "/".join(tmp) == tmp[0]:
            local_path = ""
        else:
            local_path = "/".join(tmp)
        return True
    if not flag:
        return False

    for file in files:
        if path in file.name:
            local_path = path
            return True
    return False

def cat(path, extension_path, tar_file):

    if not extension_path:
        print("\033[31m{}\033[0m".format("No file specified"))
        return

    if "root:" in extension_path:
        path = extension_path[len("root:"):]
    else:
        path += extension_path
    path = delete_symbol(path)

    try:
        with tarfile.open(tar_file) as files:
            file = files.extractfile(path)
            if file:
                print(file.read().decode('utf8').strip())
            else:
                raise KeyError
    except (KeyError, IndexError):
        print("\033[31m{}\033[0m".format("Can't open this file"))

def date():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def echo(text):
    print(text)

def cal():
    print(calendar.month(datetime.now().year, datetime.now().month))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tarfile', type=str, help='The TAR file to work with')
    parser.add_argument('--log', type=str, help='The log file to save actions', required=True)
    parser.add_argument('--script', type=str, help='Read commands from a file and execute them')

    args = parser.parse_args()

    ROOT_PATH = "root:"
    local_path = ""

    with tarfile.open(args.tarfile) as tar:
        all_files = tar.getmembers()

        if args.script:
            try:
                with open(args.script, 'r') as script_file:
                    for command in script_file:
                        command = command.strip().split(" ")
                        if command[0] == "pwd":
                            print("\033[32m{}\033[0m".format("  " + ROOT_PATH + ("/" if not local_path else local_path)))
                            log_action(args.log, 'pwd', local_path)
                        elif command[0] == "ls":
                            if len(command) == 1:
                                ls(local_path, all_files)
                            elif len(command) == 2:
                                ls(local_path, all_files, command[1])
                            log_action(args.log, 'ls', command[1] if len(command) > 1 else "")
                        elif command[0] == "cd":
                            if cd(local_path, command[1], all_files):
                                log_action(args.log, 'cd', command[1])
                            else:
                                print("\033[31m{}\033[0m".format("The path does not exist"))
                        elif command[0] == "cat":
                            if len(command) < 2:
                                print("\033[31m{}\033[0m".format("No file specified"))
                            else:
                                cat(local_path, command[1], args.tarfile)
                                log_action(args.log, 'cat', command[1])
                        elif command[0] == "date":
                            date()
                            log_action(args.log, 'date', '')
                        elif command[0] == "echo":
                            echo(' '.join(command[1:]))
                            log_action(args.log, 'echo', ' '.join(command[1:]))
                        elif command[0] == "cal":
                            cal()
                            log_action(args.log, 'cal', '')
                        elif command[0] == "exit":
                            log_action(args.log, 'exit', '')
                            exit(0)
                        else:
                            print("\033[31m{}\033[0m".format("Unknown command"))
            except IOError as e:
                print(f"Error reading script: " + str(e))
