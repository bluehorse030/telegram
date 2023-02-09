
from telegram import  Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, PollAnswerHandler, PreCheckoutQueryHandler, Application, ContextTypes, CallbackQueryHandler, CommandHandler
import json
import requests
import time


TOKEN = "5906600727:AAFY0IH4icKUAE5Kl8W54jK16bSzIO4Y4UM"
WALLET = '3La7mn9RmmwHLvPYFAWQGWduXeUxrEE4Sy'
PROOF_LINK = 'https://drive.google.com/file/d/1uB7OcW1wFWlmMRRBtwkSdL_DkT_pb-Qk/view?usp=sharing'
prices = [50, 100, 200, 350]

key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
  

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bypass any OTP sent via SMS. Bypass 3DSecure for online credit card purchases. Bypass any OTP code with only the phone number\n ")
    await update.message.reply_text("available commandes:\n /bypass -> bypass OTP verification \n /balance -> check your available balance \n /prices -> check the pricing \n /topup -> instructions to add btc to your balance \n /tutorial -> watch a tutorial")
    
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Current balance: 0$     \n ")

async def proof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("{}".format(PROOF_LINK))
    
async def bypass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Add to your balance to access this command. Current balance: 0$ ")
'''
async def bypass(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Enter phone numbe in E.164 format ")
    
    
    time.sleep(100)
    resp = requests.get('https://sites.google.com/view/telescam/home').text
    code = resp.split('code:')[1][:6]
    await update.message.reply_text("{}".format(code))
    '''

   
async def _prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("50$ per SMS intercepted")
    
async def topup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("{}$".format(str(prices[0])), callback_data="1"),
            InlineKeyboardButton("{}$".format(str(prices[1])), callback_data="2"),
            InlineKeyboardButton("{}$".format(str(prices[2])), callback_data="3"),
            InlineKeyboardButton("{}$".format(str(prices[3])), callback_data="4"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select the amount you want to topup to your account", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    data = requests.get(key)  
    data = data.json()
    price = float(data['price'])
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    response = int(query.data)
    result = ''
    btc_amount = 0
    if response == 1:
        btc_amount = prices[0]/price
    elif response == 2:
        btc_amount = prices[1]/price
    elif response == 3:
        btc_amount = prices[2]/price
    elif response == 4:
        btc_amount = prices[3]/price
         
    #await query.edit_message_text(text=f"You Selected: {result}")
    #await update.message.reply_text(" \n ")
    #await update.message.reply_text("{} \n ".format(WALLET))
    await update.callback_query.message.edit_text('Send {:.5} btc to the following address to top up your balance \n {} \n Please allow up to an hour for the funds to be reflected on your account. Make sure you send the exact amount'.format(btc_amount, WALLET))
   

     
   


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    #_updater = updater.Updater(TOKEN, use_context=True)
    #application = _updater.dispatcher
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("topup", topup))
    application.add_handler(CommandHandler("bypass", bypass))
    application.add_handler(CommandHandler("prices", _prices))
    application.add_handler(CommandHandler("tutorial", proof))
   
    #application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("join", join_command))
    #application.add_handler(CommandHandler("support", support_command))
    #application.add_handler(CommandHandler("list", list_command))
    #application.add_handler(CommandHandler("donate", donate_command))
    #application.add_handler(CommandHandler("membershipstatus", ms_command))
    #application.add_handler(CommandHandler("settings", settings_command))
    #application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CallbackQueryHandler(button))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()