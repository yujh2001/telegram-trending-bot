import os
import requests
from telegram.ext import CommandHandler, Updater

TOKEN = os.environ.get("7861369219:AAHDnmBJ1eUlK3tT5K6AaanSjKRzuT_ulxU")
USER_ID = os.environ.get("5073865182")
HELIUS_API_KEY = "f96f1101-345f-4e60-8f34-d2f5a8526a0d"

def get_sol_trending():
    url = f"https://api.helius.xyz/v0/token-metadata?api-key={HELIUS_API_KEY}"
    payload = {
        "limit": 10,
        "sortBy": "transactionCount"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        tokens = data.get("tokens", [])
        if not tokens:
            return "솔라나 체인에서 트렌딩 토큰이 없습니다."
        
        report_lines = ["솔라나 체인 트렌딩 토큰:"]
        for token in tokens:
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "")
            tx_count = token.get("transactionCount", 0)
            report_lines.append(f"{name} ({symbol}) - 거래 수: {tx_count}")
        return "\n".join(report_lines)
    except Exception as e:
        return f"데이터를 가져오는 중 오류가 발생했습니다: {e}"

def report(update, context):
    chat_id = update.effective_chat.id
    if str(chat_id) != USER_ID:
        context.bot.send_message(chat_id=chat_id, text="권한이 없습니다.")
        return

    report_message = get_sol_trending()
    context.bot.send_message(chat_id=chat_id, text=report_message)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("report", report))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
