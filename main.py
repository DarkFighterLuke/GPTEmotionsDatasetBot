import csv
import logging
import os

import telebot
from dotenv import load_dotenv

dataset_file = "supervision.csv"
filtered_ids_file = "filtered_ids"
allowed_ids_file = "allowed_ids"

load_dotenv()
bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))
logger = logging.getLogger("[GPTEmotionsDatasetBot]")
logging.basicConfig(level=logging.INFO)


def create_filtered_csv(input_file_path, output_file_path):
    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
        reader = csv.reader(input_file, delimiter="|", lineterminator="\n")
        writer = csv.writer(output_file, delimiter="|", lineterminator="\n")
        for row in reader:
            if not row[1] in load_text_file_lines(filtered_ids_file):
                writer.writerow(row[5:])


def load_text_file_lines(file_path):
    lines = set()
    with open(file_path, "r") as f:
        for line in f.readlines():
            lines.add(line.strip())

    return lines


@bot.message_handler(commands=["get"])
def send_file(message):
    temp_file = "dataset.csv"
    if str(message.from_user.id) in load_text_file_lines(allowed_ids_file):
        logger.info(
            f"Authorized user {message.from_user.id}|{message.from_user.username}|{message.from_user.first_name} {message.from_user.last_name} sent /get command")
        create_filtered_csv(dataset_file, temp_file)
        bot.send_document(message.from_user.id, open(temp_file, "r"))
        os.remove(temp_file)
    else:
        logger.info(
            f"Unauthorized user {message.from_user.id}|{message.from_user.username}|{message.from_user.first_name} {message.from_user.last_name} sent /get command")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    logger.info(
        f"User {message.from_user.id}|{message.from_user.username}|{message.from_user.first_name} {message.from_user.last_name} sent /get command")
    bot.reply_to(message, "Benvenuto su GPTEmotionsDatasetBot!\nInvia il comando /get per ottenere uno snapshot "
                          "aggiornato del dataset di @GPTSentimentsBot")


bot.infinity_polling()
