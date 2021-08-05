from telethon import Button, custom

OWNER_NAME = user.first_name
OWNER_ID = user.id


async def setit(event, name, value):
    try:
        cdB.set(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    button = [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
    return button
