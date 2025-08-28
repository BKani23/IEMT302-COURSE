
import os
import json
import re
from collections import defaultdict
import spacy
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Load environment variables (expects TELEGRAM_TOKEN in .env)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

STORE_PATH = os.getenv("TASK_STORE", "tasks_store.json")

# Load SpaCy English model (download with: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def load_store():
    if os.path.exists(STORE_PATH):
        try:
            with open(STORE_PATH,'r',encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_store(store):
    tmp = STORE_PATH + ".tmp"
    with open(tmp,'w',encoding='utf-8') as f:
        json.dump(store,f,ensure_ascii=False, indent=2)
    os.replace(tmp, STORE_PATH)

STORE = load_store()

def get_user_tasks(user_id):
    uid = str(user_id)
    return STORE.setdefault(uid, [])

def simple_clean(text: str) -> str:
    text = re.sub(r"^\s*(please|pls)\s+", "", text, flags=re.I)
    text = re.sub(r"^\s*(remind me to|remind me|remember to|i need to|i have to)\s+", "", text, flags=re.I)
    return text.strip()

def parse_task(text):
    doc = nlp(text)
    due = None
    for ent in doc.ents:
        if ent.label_ in ("DATE","TIME"):
            due = ent.text
            break

    # Try to capture a verb phrase around the root verb
    root_verbs = [t for t in doc if t.head == t and t.pos_ == "VERB"]
    description = None
    if root_verbs:
        root = root_verbs[0]
        left_i = min(t.i for t in root.subtree)
        right_i = max(t.i for t in root.subtree)
        description = doc[left_i:right_i+1].text

    if not description:
        # Fallback: all tokens that are not DATE/TIME entities or punctuation
        desc_tokens = [t.text for t in doc if not (t.ent_type_ in ("DATE","TIME") or t.is_punct)]
        description = " ".join(desc_tokens)

    description = simple_clean(description)
    if not description:
        description = text.strip()

    return description, due

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I'm Quick Task Bot 🗒️\n"
        "Tell me things like: 'remind me to finish the report by Friday 5pm'.\n"
        "Commands:\n"
        "/list – show your tasks\n"
        "/done <number> – mark as done\n"
        "/clear – remove all tasks\n"
        "/help – show help"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_user_tasks(update.effective_user.id)
    if not tasks:
        await update.message.reply_text("Your list is empty. Tell me a task to add one.")
        return
    lines = []
    for idx, t in enumerate(tasks, start=1):
        due = f" (due: {t['due']})" if t.get("due") else ""
        lines.append(f"{idx}. {t['desc']}{due}")
    await update.message.reply_text("Here are your tasks:\n" + "\n".join(lines))

async def done_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = get_user_tasks(update.effective_user.id)
    if not tasks:
        await update.message.reply_text("No tasks to complete.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /done <number>")
        return
    try:
        idx = int(context.args[0])
        if idx < 1 or idx > len(tasks):
            raise ValueError
    except ValueError:
        await update.message.reply_text("Please provide a valid task number, e.g., /done 1")
        return
    removed = tasks.pop(idx-1)
    save_store(STORE)
    await update.message.reply_text(f"Done! ✅ Removed: {removed['desc']}")

async def clear_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    STORE[uid] = []
    save_store(STORE)
    await update.message.reply_text("Cleared your task list.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    desc, due = parse_task(text)
    tasks = get_user_tasks(update.effective_user.id)
    tasks.append({"desc": desc, "due": due})
    save_store(STORE)
    due_part = f" (due: {due})" if due else ""
    await update.message.reply_text(f"Added: {desc}{due_part}\nUse /list to see all tasks or /done <number> to complete one.")

def main():
    token = TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_TOKEN is missing. Create a .env file with TELEGRAM_TOKEN=<your token>.")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("done", done_cmd))
    app.add_handler(CommandHandler("clear", clear_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
