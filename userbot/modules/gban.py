# Copyright © 2021 Cyber
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# Cyber by @StayWithMe69
# Ported from Catuserbot



import asyncio
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import Channel, ChatBannedRights

import userbot.modules.sql_helper.gban_sql_helper as gban_sql
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot import CMD_HELP

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


@register(outgoing=True, pattern=r"^\.gban(?: |$)(.*)")
async def global_ban(event):
    if event.fwd_from:
        return
    await event.edit("Gbanned....")
    start = datetime.now()
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        return await event.edit("`Why would you gban yourself?`")
    if gban_sql.is_gbanned(user.id):
        await event.edit(
            f"the [user](tg://user?id={user.id}) is already in gbanned list any way checking again"
        )
    else:
        gban_sql.catgban(user.id, reason)

    count = 0
    groups_admin = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            groups_admin.append(dialog.id)

    if len(groups_admin) == 0:
        return await event.edit(
            "`You need to be at least admin in 1 group to gban someone!`"
        )
    await event.edit(
        f"Global Ban to [{user.first_name}](tg://user?id={user.id}) in `{len(groups_admin)}` groups"
    )
    for i in range(len(groups_admin)):
        try:
            await event.client(EditBannedRequest(groups_admin[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"You don't have required permission in :\nCHAT: {event.chat.title}(`{event.chat_id}`)\nFor banning here",
            )
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await event.edit(
            "`I dont have message deleting rights here! But still he was gbanned!`"
        )
    time_taken = (datetime.now() - start).seconds
    if reason:
        await event.edit(
            f"[{user.first_name}](tg://user?id={user.id}) was gbanned in `{count}` groups in `{time_taken}` seconds!\nReason: `{reason}`"
        )
    else:
        await event.edit(
            f"[{user.first_name}](tg://user?id={user.id}) was gbanned in `{count}` groups in `{time_taken}` seconds!"
        )

    if BOTLOG and count != 0:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#GBAN\nGlobal BAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: `{user.id}`\
                                                \nReason: `{reason}`\nBanned in `{count}` groups\nTime taken = `{time_taken}` seconds",
        )


@register(outgoing=True, pattern=r"^\.ungban(?: |$)(.*)")
async def unglobal_ban(event):
    if event.fwd_from:
        return
    await event.edit("ungbaning.....")
    start = datetime.now()
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await event.edit(
            f"the [user](tg://user?id={user.id}) is not in your gbanned list"
        )
        return

    count = 0
    groups_admin = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            groups_admin.append(dialog.id)

    if len(groups_admin) == 0:
        return await event.edit(
            "`You need to be at least admin in 1 group to gban someone!`"
        )
    await event.edit(
        f"initiating ungban of the [{user.first_name}](tg://user?id={user.id}) in `{len(groups_admin)}` groups"
    )
    for i in range(len(groups_admin)):
        try:
            await event.client(EditBannedRequest(groups_admin[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"You don't have required permission in :\nCHAT: {event.chat.title}(`{event.chat_id}`)\nFor unbaning here",
            )
    time_taken = (datetime.now() - start).seconds
    if reason:
        await event.edit(
            f"[{user.first_name}](tg://user?id={user.id}) was ungbanned in `{count}` groups in `{time_taken}` seconds!\nReason: `{reason}`"
        )
    else:
        await event.edit(
            f"[{user.first_name}](tg://user?id={user.id}) was ungbanned in `{count}` groups in `{time_taken}` seconds!"
        )

    if BOTLOG and count != 0:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UNGBAN\nGlobal UNBAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: {user.id}\
                                                \nReason: `{reason}`\nUnbanned in `{count}` groups\nTime taken = `{time_taken}` seconds",
        )


@register(outgoing=True, pattern=r"^\.listgban$")
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
                )
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    if len(GBANNED_LIST) > 4095:
        with io.BytesIO(str.encode(GBANNED_LIST)) as out_file:
            out_file.name = "Gbannedusers.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Current Gbanned Users",
                reply_to=event,
            )
            await event.delete()
    else:
        await event.edit(GBANNED_LIST)

CMD_HELP.update(
    {
        "gban": ">`.gban <id/username> <reason>`"
        "\nUsage: Globally bans user from your account."
        "\nYou can reply to the user whom you want to gban or manually pass the username/id."
        "\n\n`>.ungban <id/username> <reason>`"
        "\nUsage: Same as gban but unbans the user"
        "\n\n>`.listgban`"
        "\nUsage: Lists all account who got gbanned by specified id."
    }
)
