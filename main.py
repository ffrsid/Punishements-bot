import discord
import os
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_PUNISHMENTS = 1497364541024112720

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def build_payload() -> dict:
    return {
        "flags": 1 << 15,
        "components": [
            {
                "type": 17,
                "components": [
                    # ── Header ───────────────────────────
                    {
                        "type": 10,
                        "content": (
                            "## 𝗣 𝗨 𝗡 𝗜 𝗦 𝗛 𝗠 𝗘 𝗡 𝗧 𝗦\n"
                            "-# *Every action has a consequence. No exceptions.*\n"
                            "-# ◈ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ◈"
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── I. WARNING ───────────────────────
                    {
                        "type": 10,
                        "content": (
                            "**𝐈.  𝗪𝗔𝗥𝗡𝗜𝗡𝗚**\n\n"
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
                            "**𝐈𝐈.  𝗠𝗨𝗧𝗘**\n\n"
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
                            "**𝐈𝐈𝐈.  𝗧𝗘𝗠𝗣𝗢𝗥𝗔𝗥𝗬 𝗕𝗔𝗡**\n\n"
                            "Temporary removal from the server. Applied when a mute "
                            "has proven __insufficient__ or the offense is of **considerable severity**."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── IV. PERMANENT BAN ────────────────
                    {
                        "type": 10,
                        "content": (
                            "**𝐈𝐕.  𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡**\n\n"
                            "Permanent removal from the server with __no appeal__. "
                            "Reserved for **severe violations** or repeated offenses "
                            "after all prior sanctions have been exhausted."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    # ── Footer ───────────────────────────
                    {
                        "type": 10,
                        "content": (
                            "-# ◈ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ◈\n"
                            "-# Celestials Dragons  ·  Punishments"
                        )
                    }
                ]
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
