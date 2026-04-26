import discord
import os
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]

CHANNEL_PUNISHMENTS = 1497364541024112720

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

PUNISHMENTS_PAYLOAD = {
    "embeds": [
        {
            "description": "## 𝗣𝗨𝗡𝗜𝗦𝗛𝗠𝗘𝗡𝗧𝗦\n-# 𝘊𝘰𝘯𝘴𝘦𝘲𝘶𝘦𝘯𝘤𝘦 𝘍𝘳𝘢𝘮𝘦𝘸𝘰𝘳𝘬\n```\n🔴  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━  🔴\n```",
            "color": 10038562
        },
        {
            "description": "**𝐈.  𝗪𝗔𝗥𝗡𝗜𝗡𝗚**\n\n> A formal written warning issued by staff.\n> Warnings are logged and accumulate.\n> Three warnings escalate automatically to a mute.\n\n-# ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─",
            "color": 10038562
        },
        {
            "description": "**𝐈𝐈.  𝗠𝗨𝗧𝗘**\n\n> Temporary removal of communication privileges.\n> Duration is determined by staff based on severity\n> and prior history of the offender.\n\n-# ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─",
            "color": 10038562
        },
        {
            "description": "**𝐈𝐈𝐈.  𝗧𝗘𝗠𝗣𝗢𝗥𝗔𝗥𝗬 𝗕𝗔𝗡**\n\n> Temporary removal from the server.\n> Applied when a mute has proven insufficient\n> or the offense is of considerable severity.\n\n-# ─  ─  ─  ─  ─  ─  ─  ─  ─  ─  ─",
            "color": 10038562
        },
        {
            "description": "**𝐈𝐕.  𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡**\n\n> Permanent removal from the server.\n> Reserved for severe violations or repeated offenses\n> after prior sanctions have been exhausted.\n\n```\n🔴  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━  🔴\n```\n-# Celestials Dragons  ·  Punishments",
            "color": 10038562
        }
    ]
}

async def send_embeds(channel_id: int):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=PUNISHMENTS_PAYLOAD, headers=headers) as resp:
            if resp.status not in (200, 201):
                text = await resp.text()
                print(f"[ERROR] {resp.status}: {text}")
            else:
                print(f"[OK] Punishments enviado")

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
        await send_embeds(CHANNEL_PUNISHMENTS)

client.run(TOKEN)
