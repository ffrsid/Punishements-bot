import discord
import os
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_PUNISHMENTS = 1497364541024112720

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Color rojo oscuro elegante
RED = 0xC0392B

EMBEDS = [
    # ── Portada ──────────────────────────────────────────────
    {
        "description": (
            "```ansi\n"
            "\u001b[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "\u001b[1;31m        P U N I S H M E N T S\u001b[0m\n"
            "\u001b[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "```"
            "\n-# *Every action has a consequence. No exceptions.*"
        ),
        "color": RED
    },
    # ── I. WARNING ───────────────────────────────────────────
    {
        "description": (
            "```ansi\n"
            "\u001b[1;31m  ▸  I.  W A R N I N G\u001b[0m\n"
            "```"
            "\nA formal written warning issued by staff.\n"
            "Warnings are **logged and accumulate** — three warnings\n"
            "escalate automatically to a temporary mute.\n\n"
            "-# ◈ ──────────────────────────── ◈"
        ),
        "color": RED
    },
    # ── II. MUTE ─────────────────────────────────────────────
    {
        "description": (
            "```ansi\n"
            "\u001b[1;31m  ▸  II.  M U T E\u001b[0m\n"
            "```"
            "\nTemporary removal of communication privileges.\n"
            "Duration is determined by staff based on **severity**\n"
            "and prior history of the offender.\n\n"
            "-# ◈ ──────────────────────────── ◈"
        ),
        "color": RED
    },
    # ── III. TEMPORARY BAN ───────────────────────────────────
    {
        "description": (
            "```ansi\n"
            "\u001b[1;31m  ▸  III.  T E M P O R A R Y   B A N\u001b[0m\n"
            "```"
            "\nTemporary removal from the server.\n"
            "Applied when prior sanctions have proven **insufficient**\n"
            "or the offense is of considerable severity.\n\n"
            "-# ◈ ──────────────────────────── ◈"
        ),
        "color": RED
    },
    # ── IV. PERMANENT BAN ────────────────────────────────────
    {
        "description": (
            "```ansi\n"
            "\u001b[1;31m  ▸  IV.  P E R M A N E N T   B A N\u001b[0m\n"
            "```"
            "\nPermanent removal from the server with **no appeal**.\n"
            "Reserved for severe violations or repeated offenses\n"
            "after all prior sanctions have been exhausted.\n\n"
            "```ansi\n"
            "\u001b[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "```"
            "\n-# Celestials Dragons  ·  Punishments"
        ),
        "color": RED
    },
]

async def send_punishments():
    url = f"https://discord.com/api/v10/channels/{CHANNEL_PUNISHMENTS}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"embeds": EMBEDS}, headers=headers) as resp:
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
