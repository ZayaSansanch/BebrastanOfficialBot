TOKEN = "5978727436:AAEWhUBMuvSHsS4u8YAaR5L2bRkVwxhbwbY"

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from datetime import datetime
import os

getSong = False

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Started /help")
    logs = open("texts/logs.txt", "a")
    logs.write(str(datetime.now()) + " - ")
    logs.write("Started /help" + "\n")

    helpFile = open("texts/help.txt", "r")
    lines = helpFile.readlines()
    for line in lines:
        await update.message.reply_text(line.strip())

async def listOfSongs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Started /listOfSongs")
    logs = open("texts/logs.txt", "a")
    logs.write(str(datetime.now()) + " - ")
    logs.write("Started /listOfSongs" + "\n")
    
    songs = os.listdir("texts/songs")
    for song in songs:
        await update.message.reply_text(song)

async def toSong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Started /toSong")
    logs = open("texts/logs.txt", "a")
    logs.write(str(datetime.now()) + " - ")
    logs.write("Started /toSong" + "\n")
    global getSong
    getSong = True
    await update.message.reply_text("Please type song name, /songs for see songs")

async def textMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Started textMessage, with: " + update.message.text)
    global getSong
    songs = os.listdir("texts/songs")

    logs = open("texts/logs.txt", "a")
    logs.write(str(datetime.now()) + " - ")
    logs.write(str(update.message) + "\n")
    
    if getSong == True:
        getSong = False
        getting = False
        for song in songs:
            if update.message.text == song:
                getting = True
        
        if getting:
            song = open("texts/songs/" + update.message.text, "r")
            lines = song.readlines()
            for line in lines:
                await update.message.reply_text(line.strip())
        else:
            await update.message.reply_text("Song can't be fond, you can see songs by /songs")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", help))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("songs", listOfSongs))
    app.add_handler(CommandHandler("song", toSong))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), textMessage))
    app.run_polling()

if __name__ == "__main__":
    main()