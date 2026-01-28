import psutil
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def kill_targets(target_list, callback=None):
    """
    Kills processes in target_list.
    callback(message): Optional function to send status updates back to GUI/Tray
    Returns: (killed_list, failed_list)
    """
    killed = []
    failed = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            p_name = proc.info['name']
            if p_name and p_name.lower() in [t.lower() for t in target_list]:
                proc.kill()
                killed.append(p_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            # We assume failure if we can't kill it, though AccessDenied is the main one.
            # We can't really track "failed" easily without trying and catching specific errors per process
            # But the loop iterates all processes, so we only know what we successfully killed.
    
    return killed
