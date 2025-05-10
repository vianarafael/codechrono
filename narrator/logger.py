import os
import subprocess
import time
import threading

LOG_DIR = "logs"
TERMINAL_LOG = os.path.join(LOG_DIR, "terminal.log")
WINDOW_LOG = os.path.join(LOG_DIR, "active_window.log")

_window_logger_thread = None
_stop_window_logger = threading.Event()


def clear_logs():
    os.makedirs(LOG_DIR, exist_ok=True)
    open(TERMINAL_LOG, "w").close()
    open(WINDOW_LOG, "w").close()


def start_window_logger():
    def log_windows():
        while not _stop_window_logger.is_set():
            try:
                window = subprocess.check_output(
                    ["xdotool", "getactivewindow", "getwindowname"]
                ).decode().strip()
                with open(WINDOW_LOG, "a") as f:
                    f.write(f"{int(time.time())} ::: {window}\n")
            except Exception:
                pass
            time.sleep(5)

    global _window_logger_thread
    _stop_window_logger.clear()
    _window_logger_thread = threading.Thread(target=log_windows, daemon=True)
    _window_logger_thread.start()


def stop_window_logger():
    _stop_window_logger.set()
    if _window_logger_thread:
        _window_logger_thread.join()


def get_terminal_logs(start_ts, end_ts):
    if not os.path.exists(TERMINAL_LOG):
        return []
    results = []
    with open(TERMINAL_LOG, "r") as f:
        for line in f:
            try:
                ts_str, cmd = line.strip().split(" ::: ", 1)
                ts = int(ts_str)
                if start_ts <= ts <= end_ts:
                    results.append(cmd)
            except ValueError:
                continue
    return results


def get_window_logs(start_ts, end_ts):
    if not os.path.exists(WINDOW_LOG):
        return []
    timeline = []
    with open(WINDOW_LOG, "r") as f:
        for line in f:
            try:
                ts_str, window = line.strip().split(" ::: ", 1)
                ts = int(ts_str)
                if start_ts <= ts <= end_ts:
                    timeline.append(window)
            except ValueError:
                continue
    return timeline


def get_git_diff():
    try:
        diff = subprocess.check_output(["git", "diff"]).decode()
        return diff
    except Exception:
        return "No diff available"
