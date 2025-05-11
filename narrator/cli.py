import argparse
import time
from narrator import logger, db, summarizer, llm
import re

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
        start = time.ctime(s["start"])
        end = time.ctime(s["end"])
        message = s.get("message", "(no tag)")
        duration = round((s["end"] - s["start"]) / 60, 1)  # in minutes

        summary = s.get("summary", "").strip()
        summary = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL).strip()

        print(f"\n🕒 {start} — {end}  ⏱ {duration} min  🏷 {message}\n{summary}\n")

def query_analysis(query_prompt: str, session_data: list) -> str:
    if not session_data:
        return "No past session data available."

    formatted_sessions = []
    for session in session_data:
        message = session.get("message", "")
        duration = round(session.get("duration", 0) / 3600, 2)
        summary = session.get("summary", "")
        formatted_sessions.append(f"- {message} | {duration} hours\n  {summary}")

    prompt = f"""
    Here's a list of my dev sessions with task name, time spent, and summaries:

    {chr(10).join(formatted_sessions)}

    Based on the above, please answer the following:
    {query_prompt}
    """

    raw_response = llm.run_llm(prompt)
    cleaned = re.sub(r"<think>.*?</think>", "", raw_response, flags=re.DOTALL)
    cleaned = re.sub(r"[#*`>_]", "", cleaned)  # strip markdown chars
    return cleaned.strip()

def query_sessions(args):
    print(f"🧠 Analyzing session history with query: {args.message}")
    data = db.get_estimation_data()
    result = query_analysis(args.message, data)
    print(f"\n🤖 {result}\n")



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

    estimate = subparsers.add_parser("estimate", help="Estimate time for a new task")
    estimate.add_argument("-m", "--message", type=str, required=True, help="Task description to estimate")
    estimate.set_defaults(func=estimate_task)

    query = subparsers.add_parser("query", help="Ask high-level questions about your session history")
    query.add_argument("-m", "--message", type=str, required=True, help="Query prompt for the LLM")
    query.set_defaults(func=query_sessions)



    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()