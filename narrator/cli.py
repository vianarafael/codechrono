import argparse
import time
from narrator import logger, db, summarizer

SESSION_STATE = {"start_time": None}


def start_session(args):
    print(f"🔵 Starting session: {args.message}")
    SESSION_STATE["start_time"] = int(time.time())
    
    logger.clear_logs()
    logger.start_window_logger()

    db.init_db()
    db.create_session(args.message, SESSION_STATE["start_time"])

    print("⏳ Session running. Use 'stop' to end.")


def stop_session(args):
    end_time = int(time.time())
    start_time = SESSION_STATE.get("start_time")

    start_time = db.get_last_unfinished_session()
    if not start_time:
        print("⚠️ No active session found in DB.")
        return

    print("🛑 Stopping session...")
    logger.stop_window_logger()

    commands = logger.get_terminal_logs(start_time, end_time)
    windows = logger.get_window_logs(start_time, end_time)
    git_diff = logger.get_git_diff()

    summary = summarizer.summarize_session(commands, git_diff, windows)
    db.finalize_session(start_time, end_time, summary)

    print("✅ Summary:")
    print(summary)

def estimate_task(args):
    print(f"📐 Estimating time for: {args.message}")
    past_sessions = db.get_estimation_data()
    estimate = summarizer.estimate_time(args.message, past_sessions)
    print(f"\n🧮 Estimated Time: {estimate}\n")
    

def report_sessions(args):
    print("📄 Recent Sessions:")
    sessions = db.get_recent_summaries()
    for s in sessions:
        print(f"\n🕒 {time.ctime(s['start'])} — {time.ctime(s['end'])}\n{ s['summary'] }\n")


def main():
    parser = argparse.ArgumentParser(prog="code_narrator", description="Track and summarize dev sessions.")
    subparsers = parser.add_subparsers(dest="command")

    start = subparsers.add_parser("start", help="Start a coding session")
    start.add_argument("-m", "--message", type=str, required=True, help="Tag or description of the session")
    start.set_defaults(func=start_session)

    stop = subparsers.add_parser("stop", help="Stop the current session")
    stop.set_defaults(func=stop_session)

    report = subparsers.add_parser("report", help="Show past session summaries")
    report.set_defaults(func=report_sessions)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()