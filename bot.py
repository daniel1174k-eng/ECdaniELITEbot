import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token (Note: It's not recommended to hardcode tokens in production)
BOT_TOKEN = "8361000818:AAEytI5UkFTp0y1rPlXCe9ITtYlqHuTrc6w"

# Your social media links
CHANNEL_URL = "https://t.me/MagnetReach_Digital"
GROUP_URL = "https://t.me/hMagnetReach_Digital"
TWITTER_URL = "https://x.com/Agboolabamise17"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message on /start"""
    user = update.effective_user
    welcome_message = (
        f"Hello {user.first_name}! 👋\n\n"
        "Welcome to the *ECdaniELITE Airdrop Bot*!\n\n"
        "To qualify for our airdrop, you need to complete a few simple tasks:\n\n"
        "1. Join our Telegram channel\n"
        "2. Join our Telegram group\n"
        "3. Follow our Twitter account\n"
        "4. Submit your Solana wallet address\n\n"
        "Click the button below to get started! 🚀"
    )
    
    keyboard = [[InlineKeyboardButton("Start Tasks 🎯", callback_data="start_tasks")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_tasks":
        # First task: Join channel
        keyboard = [[
            InlineKeyboardButton("Join Channel", url=CHANNEL_URL),
            InlineKeyboardButton("I've Joined ✅", callback_data="joined_channel")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Task 1/4: Join Our Telegram Channel*\n\n"
            "Please join our official channel.\n\n"
            "After joining, click the button below to continue.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    elif query.data == "joined_channel":
        # Second task: Join group
        keyboard = [[
            InlineKeyboardButton("Join Group", url=GROUP_URL),
            InlineKeyboardButton("I've Joined ✅", callback_data="joined_group")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Task 2/4: Join Our Telegram Group*\n\n"
            "Please join our official group.\n\n"
            "After joining, click the button below to continue.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    elif query.data == "joined_group":
        # Third task: Follow Twitter
        keyboard = [[
            InlineKeyboardButton("Follow Twitter", url=TWITTER_URL),
            InlineKeyboardButton("I'm Following ✅", callback_data="followed_twitter")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Task 3/4: Follow Our Twitter*\n\n"
            "Please follow our Twitter account.\n\n"
            "After following, click the button below to continue.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    
    elif query.data == "followed_twitter":
        # Fourth task: Submit wallet
        await query.edit_message_text(
            "*Task 4/4: Submit Your Solana Wallet*\n\n"
            "Please enter your Solana wallet address now.\n\n"
            "Example: `8xTsFpPEVW6gXgLJ9Qj1kK3mK4wLWbPfVZ5JxR7sL8qy`",
            parse_mode="Markdown"
        )
        # Set state to wait for wallet address
        context.user_data['state'] = 'awaiting_wallet'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle all messages"""
    # Check if we're waiting for a wallet address
    if context.user_data.get('state') == 'awaiting_wallet':
        wallet_address = update.message.text.strip()
        
        # Simple validation for Solana wallet (basic format check)
        if len(wallet_address) < 32 or len(wallet_address) > 44:
            await update.message.reply_text(
                "That doesn't look like a valid Solana wallet address. "
                "Please check and try again.\n\n"
                "Example: `8xTsFpPEVW6gXgLJ9Qj1kK3mK4wLWbPfVZ5JxR7sL8qy`",
                parse_mode="Markdown"
            )
            return
        
        # Success message
        await update.message.reply_text(
            f"🎉 *Congratulations!* 🎉\n\n"
            f"You've successfully qualified for the ECdaniELITE airdrop!\n\n"
            f"*Wallet submitted:* `{wallet_address}`\n\n"
            "100 SOL will be sent to your wallet after the airdrop period ends.\n"
            "Well done, hope you didn't cheat the system! 😉\n\n"
            "Thank you for participating!",
            parse_mode="Markdown"
        )
        
        # Reset state
        context.user_data['state'] = None
    else:
        # If not waiting for wallet, just respond with start message
        await start(update, context)

def main() -> None:
    """Start the bot"""
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()
