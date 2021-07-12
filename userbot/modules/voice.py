# Copyright (C) 2021 TeamUltroid
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import ALIVE_NAME, CMD_HELP
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, groups_only=True, pattern=r"^\.startvc$")
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await c.edit(f"`Sorry {ALIVE_NAME} you are not admin`")
        return
    try:
        await c.client(startvc(c.chat_id))
        await c.edit("`✅ Voice Chat Started...`")
    except Exception as ex:
        await c.edit(f"`Sorry an error occurred:` `{ex}`")


@register(outgoing=True, groups_only=True, pattern=r"^\.stopvc$")
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await c.edit(f"`Sorry {ALIVE_NAME} you are not admin`")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await c.edit("`✅ Voice Chat Stopped...`")
    except Exception as ex:
        await c.edit(f"`Sorry an error occurred:` `{ex}`")


@register(outgoing=True, groups_only=True, pattern=r"^\.vcinvite")
async def _(c):
    await c.edit("`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 6))
    for p in botman:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await c.edit(f"`{z}` `✅ Successfully invite to voice`")

@register(outgoing=True, groups_only=True, pattern=r"^\.vcinvite")
async def _(c):
    await c.edit("`Inviting Members to Voice Chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 200))
    for p in hmm:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 200
        except BaseException:
            pass
    await c.edit(f"`✅ Successfully invite {z} to voice`")


CMD_HELP.update(
    {
       "voice": ">`.startvc`"
       "\nUsage: Start Group Call in a group."
       "\n\n>`.stopvc`"
       "\nUsage: Stop Group Call in a group."
       "\n\n>`.vcinvite`"
       "\nUsage: Invite all members of group in Group Call (You must be joined)."
    }
)
