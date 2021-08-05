from telethon import Button, custom
from userbot import ALIVE_NAME

OWNER_NAME = ALIVE_NAME
OWNER_ID = "950149480"


async def setit(event, name, value):
    try:
        cdB.set(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    button = [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
    return button
