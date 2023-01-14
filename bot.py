import os
import asyncio
from pathlib import Path
from dotenv import dotenv_values
import telebot
from revChatGPT.ChatGPT import Chatbot

# get config
parent_dir = Path(__file__).resolve().parent
config = dotenv_values(f"{parent_dir}/.env")

# init telegram bot
BOT_TOKEN = config["BOT_TOKEN"]
bot = telebot.TeleBot(BOT_TOKEN)

# init chatbot
chatbot = Chatbot(
    {"session_token": config["SESSION_TOKEN"]}, conversation_id=None, parent_id=None
)
print("Chatbot & TeleBot initialized ")

# define a message handler to send a message when the command /start is issued


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you doing? \nHere are some options to help you with your job hunt! \n1. Generate a resume template\n2. Generate a personal professional resume\n3. Discover your strengths by listing out your activities\n4. Explore career options and alternatives\n5. Practice responding to interview questions")

# option1


@bot.message_handler(commands=["1"])
def send_message_1(message):
    sent_msg = bot.send_message(
        message.chat.id, "Key in the job you are applying for (ex. marketing manager/financial analyst/software engineer)")
    bot.register_next_step_handler(sent_msg, send_gpt_1handler)

# generate chatgpt response for option 1


def send_gpt_1handler(message):
    interest = message.text
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask(interest + "resume template")
    bot.reply_to(message, response["message"])

# option 2


@bot.message_handler(commands=["2"])
def send_message_2(message):
    sent_msg = bot.send_message(
        message.chat.id, "Key in the job you are applying for and your details as much as possible to generate a personalized professional resume")
    bot.register_next_step_handler(sent_msg, send_gpt_2handler)

# generate chatgpt response for option 2


def send_gpt_2handler(message):
    details = message.text
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask("Generate a resume " + details)
    bot.reply_to(message, response["message"])

# option 3


@bot.message_handler(commands=["3"])
def send_message_3(message):
    sent_msg = bot.send_message(
        message.chat.id, "List your activities or your experiences (ex. minecraft/hackathon)")
    bot.register_next_step_handler(sent_msg, send_gpt_3handler)

# generate chatgpt response for option 3


def send_gpt_3handler(message):
    details = message.text
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask("What skills do I gain from " +
                           details + "that could be useful in the workplace?")
    bot.reply_to(message, response["message"])

# option 4


@bot.message_handler(commands=["4"])
def send_message_4(message):
    sent_msg = bot.send_message(
        message.chat.id, "Key in the job you want to search alternative options")
    bot.register_next_step_handler(sent_msg, send_gpt_4handler)

# generate chatgpt response for option 4


def send_gpt_4handler(message):
    interest = message.text
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask(
        "Write a list with descriptions of 10 careers that are similar to " + interest)
    bot.reply_to(message, response["message"])

# option 4


@bot.message_handler(commands=["4"])
def send_message_5(message):
    sent_msg = bot.send_message(
        message.chat.id, "Key in the job you want to apply for")
    bot.register_next_step_handler(sent_msg, send_gpt_5handler)

# generate chatgpt response for option 5


def send_gpt_5handler(message):
    interest = message.text
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask(
        "Generate a list of common interview questions for " + interest)
    bot.reply_to(message, response["message"])

# define a message handler to send a message when the command /gpt is issued


@ bot.message_handler(commands=["gpt"])
def send_gpt(message):
    print("Working with chatgpt")
    bot.send_message(message.chat.id, "Working with chatgpt. Gimme a sec...")
    response = chatbot.ask(message.text.replace("/gpt", ""))
    bot.reply_to(message, response["message"])


# run the bot
# asyncio.run(bot.polling())
bot.infinity_polling()
