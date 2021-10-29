import psutil
import subprocess
import threading

def start(process_name):
    t = threading.Thread(
        target = subprocess.Popen,
        args = ['start ' + process_name],
        kwargs = {'shell':True, 'stdout':subprocess.PIPE}
    )
    t.start()


def kill(pid):
    proc = psutil.Process(pid)
    proc.kill()


def get_running_processes():
    procs = []
    for proc in psutil.process_iter():
        with proc.oneshot():
            info = {}
            info['name'] = proc.name()
            info['pid'] = proc.pid
            info['num_threads'] = proc.num_threads()
            procs.append(info)
    return procs
    

def get_running_applications():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Id'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    pids = []
    for line in proc.stdout:
        try:
            pids.append(int(line.decode().rstrip()))
        except ValueError:
            pass
    apps = []
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                info = {}
                info['name'] = proc.name()
                info['pid'] = proc.pid
                info['num_threads'] = proc.num_threads()
                apps.append(info)
        except psutil.NoSuchProcess:
            pass
    return apps
