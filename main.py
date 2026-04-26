import discord
import os
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_PUNISHMENTS = 1497364541024112720

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

DIV = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

def build_payload() -> dict:
    return {
        "flags": 1 << 15,
        "components": [
            {
                "type": 17,
                "components": [
                    # ── Portada ──────────────────────────
                    {
                        "type": 10,
                        "content": (
                            "```ansi\n"
                            "\u001b[1;31mP U N I S H M E N T S\u001b[0m\n"
                            "```"
                            f"-# {discord.utils.escape_markdown('Consequence Framework')}  ·  Celestials Dragons\n"
                            f"```\n{DIV}\n```"
                        )
                    },
                    # ── I. WARNING ───────────────────────
                    {
                        "type": 10,
                        "content": (
                            "```ansi\n"
                            "\u001b[2;31m▸  I.  WARNING\u001b[0m\n"
                            "```"
                            "A formal written warning issued by staff. "
                            "Warnings are logged and __accumulate__ — "
                            "**three warnings** escalate automatically to a mute."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── II. MUTE ─────────────────────────
                    {
                        "type": 10,
                        "content": (
                            "```ansi\n"
                            "\u001b[2;31m▸  II.  MUTE\u001b[0m\n"
                            "```"
                            "Temporary removal of communication privileges. "
                            "Duration is determined by staff based on __severity__ "
                            "and prior history of the offender."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── III. TEMPORARY BAN ───────────────
                    {
                        "type": 10,
                        "content": (
                            "```ansi\n"
                            "\u001b[2;31m▸  III.  TEMPORARY BAN\u001b[0m\n"
                            "```"
                            "Temporary removal from the server. Applied when a mute has proven "
                            "__insufficient__ or the offense is of **considerable severity**."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── IV. PERMANENT BAN ────────────────
                    {
                        "type": 10,
                        "content": (
                            "```ansi\n"
                            "\u001b[2;31m▸  IV.  PERMANENT BAN\u001b[0m\n"
                            "```"
                            "Permanent removal from the server with __no appeal__. "
                            "Reserved for **severe violations** or repeated offenses "
                            "after all prior sanctions have been exhausted."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── Footer ───────────────────────────
                    {
                        "type": 10,
                        "content": f"-# ◈  *Ignorance of the rules is not an excuse.*  ◈"
                    }
                ],
                "accent_color": 0x0d0d0d
            }
        ]
    }

async def send_punishments():
    url = f"https://discord.com/api/v10/channels/{CHANNEL_PUNISHMENTS}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=build_payload(), headers=headers) as resp:
            if resp.status not in (200, 201):
                text = await resp.text()
                print(f"[ERROR] {resp.status}: {text}")
            else:
                print("[OK] Punishments enviado")

@client.event
async def on_ready():
    print(f"[ONLINE] {client.user} listo")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content.strip() == ">setuppunishments":
        if not message.author.guild_permissions.administrator:
            return
        await message.delete()
        await send_punishments()

client.run(TOKEN)
