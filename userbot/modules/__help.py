from telethon.errors.rpcerrorlist import BotInlineDisabledError as dis
from telethon.errors.rpcerrorlist import BotMethodInvalidError
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as rep

from userbot import CMD_HELP
from userbot.events import register

from ..core import HELP, LIST, ALLMODULES
from ..utils import edit_delete, edit_or_reply
from . import *


@register(outgoing=True, pattern=r"^\.help")
async def _help(cyb):
    module = cyb.pattern_match.group(1)
    if module:
        try:
            if module in HELP:
                output = f"**Modules** - `{module}`\n"
                for i in HELP[module]:
                    output += i
                output += "\n© @TeamCyber"
                await edit_or_reply(edit_or_reply, output)
            elif modules in CMD_HELP:
                kk = f"Modules Name-{modules}\n\n✘ Commands Available -\n\n"
                kk += str(CMD_HELP[module])
                await edit_or_reply(cyb, kk)
            else:
                try:
                    x = f"Modules Name-{module}\n\n✘ Commands Available -\n\n"
                    for d in LIST[module]:
                        x += HNDLR + d
                        x += "\n"
                    x += "\n© @TeamCyber"
                    await edit_or_reply(cyb, x)
                except BaseException:
                    await edit_delete(cyb, get_string("help_1").format(plug), time=5)
        except BaseException:
            await edit_or_reply(cyb, "Error 🤔 occured.")
    else:
        tgbot = asst.me.username
        try:
            results = await cyb.client.inline_query(tgbot, "cyber")
        except BotMethodInvalidError:
            z = []
            for x in LIST.values():
                for y in x:
                    z.append(y)
            cmd = len(z) + 10
            return await cyb.client.send_message(
                cyb.chat_id,
                get_string("inline_4").format(
                    OWNER_NAME,
                    len(MODULES) - 5,
                    cmd,
                ),
                buttons=[
                    [
                        Button.inline("• Pʟᴜɢɪɴs", data="hrrrr"),
                    ],
                    [
                        Button.inline("Oᴡɴᴇʀ•ᴛᴏᴏʟꜱ", data="ownr"),
                        Button.inline("Iɴʟɪɴᴇ•Pʟᴜɢɪɴs", data="inlone"),
                    ],
                    [
                        Button.url(
                            "⚙️Sᴇᴛᴛɪɴɢs⚙️", url=f"https://t.me/{tgbot}?start=set"
                        ),
                    ],
                    [Button.inline("••Cʟᴏꜱᴇ••", data="close")],
                ],
            )
        except rep:
            return await edit_or_reply(
                cyb,
                get_string("help_2").format(HNDLR),
            )
        except dis:
            return await edit_or_reply(cyb, get_string("help_3"))
        await results[0].click(cyb.chat_id, reply_to=cyb.reply_to_msg_id, hide_via=True)
        await cyb.delete()
