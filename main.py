#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import time

if len(sys.argv) < 2:
    print("No shell command provided")
    exit(1)

aerospace_path = shutil.which('aerospace')
if aerospace_path is None:
    print("Cannot find the 'aerospace' binary in PATH")
    exit(1)

ps_path = shutil.which('ps')
if ps_path is None:
    print("Cannot find the 'ps' binary in PATH")
    exit(1)

def launch_shell_command(command):
    # NOT the shell because only the first argument would be command (for some reason)
    # see - https://docs.python.org/3/library/subprocess.html
    sub = subprocess.Popen(command, shell=False)

    return sub

def capture_command_output(command):
    completed_process = subprocess.run(
        command,
        shell=False,
        capture_output=True,
        text=True
    )
    return completed_process.stdout


def get_pid_to_window_id_mapping():
    output = capture_command_output([aerospace_path, 'list-windows', '--all', '--format', '%{window-id}-%{app-pid}'])
    mapping = {}
    for window_id, pid in [line.split('-') for line in output.split('\n') if len(line.strip()) > 1]:
        mapping[int(pid)] = int(window_id)
    return mapping

def get_window_id_to_workspace_mapping():
    output = capture_command_output([aerospace_path, 'list-windows', '--all', '--format', '%{window-id}-%{workspace}'])
    mapping = {}
    for window_id, workspace in [line.split('-') for line in output.split('\n') if len(line.strip()) > 1]:
        mapping[int(window_id)] = workspace
    return mapping

def try_get_two_ps_fields(ps_line):
    first_word = ''
    second_word = None
    for c in ps_line:
        if (c == ' '):
            if (len(first_word) > 0) and (second_word is None):
                second_word = ''
        elif second_word is None:
            first_word += c
        else:
            second_word += c
    if (second_word is not None) and len(second_word) > 0:
        return (first_word, second_word)
    return None

def get_pid_to_parent_pid_mapping():
    output = capture_command_output([ps_path, '-eo', 'pid,ppid'])
    mapping = {}
    for pid_and_ppid in [try_get_two_ps_fields(line) for line in output.split('\n')[1:]]:
        if pid_and_ppid is not None:
            pid, ppid = pid_and_ppid
            mapping[int(pid)] = int(ppid)
    return mapping

def try_get_window_id(pid):
    pid_to_wid = get_pid_to_window_id_mapping()
    pid_to_ppid = get_pid_to_parent_pid_mapping()
    if pid in pid_to_wid:
        return pid_to_wid[pid]
    if not (pid in pid_to_ppid):
        return None
    return try_get_window_id(pid_to_ppid[pid])

def focus_on(window_id):
    capture_command_output([aerospace_path, 'focus', '--window-id', str(window_id)])

def move_to_workspace(name):
    capture_command_output([aerospace_path, 'move-node-to-workspace', name])

def get_workspace_of(window_id):
    return get_window_id_to_workspace_mapping()[window_id]


script_pid = os.getpid()
script_window_id = try_get_window_id(script_pid)
if script_window_id is None:
    print("Cannot find window id of current proccess - is it really launched through GUI?")
    exit(1)
# print("Script's own process ID:", script_pid)
# print("Script's own window ID is:", script_window_id)

sub = launch_shell_command(sys.argv[1:])

workspace = get_workspace_of(script_window_id)
focus_on(script_window_id)
move_to_workspace('scratchpad') # TODO: parametrize?

# TODO: if need be, wait for subchildren too? Or untill there are no window ids rooting from this pid? For now it works fine as is
sub.wait()

focus_on(script_window_id)
move_to_workspace(workspace)
focus_on(script_window_id)
