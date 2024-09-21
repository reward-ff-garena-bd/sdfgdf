from telegram.ext import Updater, CommandHandler
import random
import time

# Your bot token from BotFather
BOT_TOKEN = 'your-telegram-bot-token'

# In-memory user data (in production, use a database like MySQL, MongoDB)
user_data = {}

# Start command: Registers a user and sends a welcome message
def start(update, context):
    user_id = update.message.chat_id
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0, 'referred_by': None, 'referrals': []}
    context.bot.send_message(chat_id=user_id, text="Welcome to the Mining Bot! Use /mine to start mining tokens.")

# Mine command: Simulates mining and rewards random tokens (1-20 tokens)
def mine(update, context):
    user_id = update.message.chat_id
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0, 'referred_by': None, 'referrals': []}

    # Mining logic: Reward random tokens between 1 and 20
    mined_tokens = random.randint(1, 20)
    user_data[user_id]['balance'] += mined_tokens

    # Simulate a delay for mining (optional)
    time.sleep(2)

    context.bot.send_message(chat_id=user_id, text=f"You mined {mined_tokens} tokens! Total balance: {user_data[user_id]['balance']} tokens.")

# Balance command: Shows the current balance of the user
def balance(update, context):
    user_id = update.message.chat_id
    balance = user_data.get(user_id, {}).get('balance', 0)
    context.bot.send_message(chat_id=user_id, text=f"Your current balance is: {balance} tokens.")

# Referral system: User can refer others by sharing their user_id
def refer(update, context):
    referrer_id = update.message.chat_id
    if len(context.args) > 0:
        referred_by = int(context.args[0])
        if referred_by in user_data:
            if referrer_id not in user_data[referred_by]['referrals']:
                user_data[referred_by]['referrals'].append(referrer_id)
                context.bot.send_message(chat_id=referrer_id, text=f"You have been referred by {referred_by}.")
                # Optional: Add referral bonuses here
                user_data[referred_by]['balance'] += 10  # Example: 10 token bonus for referral
                context.bot.send_message(chat_id=referred_by, text="You received 10 bonus tokens for referring a user!")
            else:
                context.bot.send_message(chat_id=referrer_id, text="You have already been referred by this user.")
        else:
            context.bot.send_message(chat_id=referrer_id, text="Invalid referral code.")
    else:
        context.bot.send_message(chat_id=referrer_id, text="Please provide a referral code.")

# Referrals command: Displays users referred by the current user
def referrals(update, context):
    user_id = update.message.chat_id
    referrals_list = user_data.get(user_id, {}).get('referrals', [])
    if referrals_list:
        context.bot.send_message(chat_id=user_id, text=f"You referred: {', '.join(map(str, referrals_list))} users.")
    else:
        context.bot.send_message(chat_id=user_id, text="You haven't referred anyone yet.")

# Leaderboard command (optional): Shows top users by balance
def leaderboard(update, context):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['balance'], reverse=True)
    leaderboard_text = "Leaderboard:\n"
    rank = 1
    for user, data in sorted_users[:10]:  # Show top 10 users
        leaderboard_text += f"{rank}. User {user}: {data['balance']} tokens\n"
        rank += 1
    context.bot.send_message(chat_id=update.message.chat_id, text=leaderboard_text)

# Main function to start the bot
def main():
    # Set up the updater and dispatcher
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('mine', mine))
    dispatcher.add_handler(CommandHandler('balance', balance))
    dispatcher.add_handler(CommandHandler('refer', refer, pass_args=True))
    dispatcher.add_handler(CommandHandler('referrals', referrals))
    dispatcher.add_handler(CommandHandler('leaderboard', leaderboard))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
