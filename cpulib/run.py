import subprocess
import datetime


def run(ca, shell):
    try:
        res = subprocess.check_output(ca, shell=shell, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return str(ca) + '\n' + e.output.decode("utf-8")
    return res


def run_nowait(ca, shell):
    return subprocess.Popen(ca, shell=shell)


def format_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def append_file(fname, st):
    with open(fname, 'a+', encoding='utf-8') as f:
        f.write(st + '\n')


def append_debug_log(st):
    st2 = '[' + format_current_datetime() + '] ' + str(st)
    append_file('logs/debug.log', st2)

def append_ping_log(st):
    st2 = '[' + format_current_datetime() + '] ' + str(st)
    append_file('logs/ping.log', st2)

