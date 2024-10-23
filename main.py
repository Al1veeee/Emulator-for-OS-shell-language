import tarfile
import sys
import argparse
import csv
from datetime import datetime
import calendar
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

local_path = ""

def delete_symbol(path):
    for letter in path:
        if letter == "/":
            path = path[1:]
        else:
            break
    return path


def log_action(logfile, action, full_command):
    # Если файл не существует или пуст, добавляем заголовки
    if not os.path.exists(logfile) or os.stat(logfile).st_size == 0:
        with open(logfile, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Command'])

    # Запись действия
    with open(logfile, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"{action} {full_command}"])


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

    return sorted(items)


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
        return "No file specified"

    if "root:" in extension_path:
        path = extension_path[len("root:"):]
    else:
        path += extension_path
    path = delete_symbol(path)

    try:
        with tarfile.open(tar_file) as files:
            file = files.extractfile(path)
            if file:
                return file.read().decode('utf8').strip()
            else:
                raise KeyError
    except (KeyError, IndexError):
        return "Can't open this file"


def date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def echo(text):
    return text


def cal():
    return calendar.month(datetime.now().year, datetime.now().month)


def execute_command(command, args, all_files, output_area=None):
    global local_path
    result = ""
    if command[0] == "pwd":
        result = "root:" + ("/" if not local_path else local_path)
        log_action(args.log, 'pwd', '')
    elif command[0] == "ls":
        items = ls(local_path, all_files, command[1] if len(command) > 1 else None)
        result = "\n".join(items)
        log_action(args.log, 'ls', command[1] if len(command) > 1 else '')
    elif command[0] == "cd":
        if cd(local_path, command[1], all_files):
            result = "Changed directory to " + command[1]
            log_action(args.log, 'cd', command[1])
        else:
            result = "The path does not exist"
    elif command[0] == "cat":
        result = cat(local_path, command[1], args.tarfile)
        log_action(args.log, 'cat', command[1])
    elif command[0] == "date":
        result = date()
        log_action(args.log, 'date', '')
    elif command[0] == "echo":
        result = echo(' '.join(command[1:]))
        log_action(args.log, 'echo', ' '.join(command[1:]))
    elif command[0] == "cal":
        result = cal()
        log_action(args.log, 'cal', '')
    elif command[0] == "exit":
        log_action(args.log, 'exit', '')
        sys.exit(0)
    else:
        result = "Unknown command"

    if output_area:
        output_area.config(state=tk.NORMAL)
        output_area.insert(tk.END, f"$ {' '.join(command)}\n{result}\n", 'green')
        output_area.config(state=tk.DISABLED)

    return result


def gui_main(all_files, args):
    def execute_gui_command():
        command = entry.get().strip().split()
        if command:
            execute_command(command, args, all_files, output_area)
            entry.delete(0, tk.END)

    def execute_script_commands(script):
        try:
            with open(script, 'r') as script_file:
                for line in script_file:
                    command = line.strip().split()
                    if command:
                        execute_command(command, args, all_files, output_area)
        except IOError as e:
            messagebox.showerror("Error", f"Error reading script: {str(e)}")

    # GUI setup
    window = tk.Tk()
    window.title("Shell Emulator")
    window.configure(bg='black')

    frame = tk.Frame(window, bg='black')
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    output_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, bg='black', fg='green', insertbackground='green',
                                            height=20)
    output_area.pack(fill=tk.BOTH, expand=True, pady=10)
    output_area.tag_configure('green', foreground='green')
    output_area.config(state=tk.DISABLED)  # Disable editing

    entry = tk.Entry(frame, bg='black', fg='green', insertbackground='green')
    entry.pack(fill=tk.X, pady=5)

    execute_button = tk.Button(frame, text="Execute", command=execute_gui_command, bg='black', fg='green')
    execute_button.pack(pady=5)

    # Bind Enter key to execute command
    window.bind('<Return>', lambda event: execute_gui_command())

    # Resizing behavior
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Execute script if provided
    if args.script:
        execute_script_commands(args.script)

    window.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tarfile', type=str, help='The TAR file to work with')
    parser.add_argument('--log', type=str, help='The log file to save actions', required=True)
    parser.add_argument('--script', type=str, help='Read commands from a file and execute them')

    args = parser.parse_args()

    local_path = ""

    with tarfile.open(args.tarfile) as tar:
        all_files = tar.getmembers()

        # Start GUI
        gui_main(all_files, args)
