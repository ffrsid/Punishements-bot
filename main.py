import discord
import os
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]
APPLICATION_ID = int(os.environ.get("APPLICATION_ID", "0"))
CHANNEL_PUNISHMENTS = 1497364541024112720

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ─────────────────────────────────────────────
#  C O N T E N T
# ─────────────────────────────────────────────

PUNISHMENTS_CONTENT = {
    "en": (
        "**𝐈.  𝗪𝗔𝗥𝗡𝗜𝗡𝗚**\n\n"
        "A formal written warning issued by staff. "
        "Warnings are logged and __accumulate__ — "
        "**three warnings** escalate automatically to a mute.\n\n"
        "**𝐈𝐈.  𝗠𝗨𝗧𝗘**\n\n"
        "Temporary removal of communication privileges. "
        "Duration is determined by staff based on __severity__ "
        "and prior history of the offender.\n\n"
        "**𝐈𝐈𝐈.  𝗧𝗘𝗠𝗣𝗢𝗥𝗔𝗥𝗬 𝗕𝗔𝗡**\n\n"
        "Temporary removal from the server. Applied when a mute "
        "has proven __insufficient__ or the offense is of **considerable severity**.\n\n"
        "**𝐈𝐕.  𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧 𝗕𝗔𝗡**\n\n"
        "Permanent removal from the server with __no appeal__. "
        "Reserved for **severe violations** or repeated offenses "
        "after all prior sanctions have been exhausted.\n\n"
        "-# Celestials Dragons  ·  Punishments"
    ),
    "es": (
        "**𝐈.  𝗔𝗗𝗩𝗘𝗥𝗧𝗘𝗡𝗖𝗜𝗔**\n\n"
        "Una advertencia formal emitida por el staff. "
        "Las advertencias se registran y __acumulan__ — "
        "**tres advertencias** escalan automáticamente a un mute.\n\n"
        "**𝐈𝐈.  𝗠𝗨𝗧𝗘**\n\n"
        "Eliminación temporal de privilegios de comunicación. "
        "La duración es determinada por el staff según la __gravedad__ "
        "e historial previo del infractor.\n\n"
        "**𝐈𝐈𝐈.  𝗕𝗔𝗡 𝗧𝗘𝗠𝗣𝗢𝗥𝗔𝗟**\n\n"
        "Expulsión temporal del servidor. Se aplica cuando el mute ha sido "
        "__insuficiente__ o la infracción es de **gravedad considerable**.\n\n"
        "**𝐈𝐕.  𝗕𝗔𝗡 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗘**\n\n"
        "Expulsión permanente del servidor __sin apelación__. "
        "Reservado para **violaciones graves** o infracciones repetidas "
        "tras haberse agotado todas las sanciones previas.\n\n"
        "-# Celestials Dragons  ·  Punishments"
    ),
    "pt": (
        "**𝐈.  𝗔𝗩𝗜𝗦𝗢**\n\n"
        "Um aviso formal emitido pela staff. "
        "Os avisos são registrados e __acumulam__ — "
        "**três avisos** escalam automaticamente para um mute.\n\n"
        "**𝐈𝐈.  𝗠𝗨𝗧𝗘**\n\n"
        "Remoção temporária dos privilégios de comunicação. "
        "A duração é determinada pela staff com base na __gravidade__ "
        "e no histórico anterior do infrator.\n\n"
        "**𝐈𝐈𝐈.  𝗕𝗔𝗡 𝗧𝗘𝗠𝗣𝗢𝗥𝗔𝗥𝗜𝗢**\n\n"
        "Remoção temporária do servidor. Aplicado quando o mute foi "
        "__insuficiente__ ou a infração é de **gravidade considerável**.\n\n"
        "**𝐈𝐕.  𝗕𝗔𝗡 𝗣𝗘𝗥𝗠𝗔𝗡𝗘𝗡𝗧𝗘**\n\n"
        "Remoção permanente do servidor sem __apelação__. "
        "Reservado para **violações graves** ou infrações repetidas "
        "após o esgotamento de todas as sanções anteriores.\n\n"
        "-# Celestials Dragons  ·  Punishments"
    ),
}

# ─────────────────────────────────────────────
#  P A Y L O A D S
# ─────────────────────────────────────────────

def build_accept_payload() -> dict:
    return {
        "flags": 1 << 15,
        "components": [
            {
                "type": 17,
                "accent_color": 0x2ECC71,  # verde
                "components": [
                    {
                        "type": 10,
                        "content": (
                            "By accepting, you acknowledge that you have read and understood "
                            "the punishment system of **Celestials Dragons**. "
                            "Violations will result in the sanctions described — "
                            "ignorance is __not__ an excuse."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    {
                        "type": 9,
                        "components": [
                            {
                                "type": 10,
                                "content": "-# Tap to confirm you understand."
                            }
                        ],
                        "accessory": {
                            "type": 2,
                            "style": 3,
                            "label": "Accepted",
                            "custom_id": "accept_punishments",
                            "emoji": {"id": "1497991468584014025", "name": "emoji_2"}
                        }
                    }
                ]
            }
        ]
    }

def build_lang_select_payload() -> dict:
    return {
        "flags": 1 << 15,
        "components": [
            {
                "type": 17,
                "accent_color": 0xFFFFFF,  # blanco
                "components": [
                    {
                        "type": 10,
                        "content": (
                            "Choose your language to view the punishment system.\n"
                            "-# The content will be sent to you privately."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    {
                        "type": 9,
                        "components": [
                            {
                                "type": 10,
                                "content": "-# Select your language below."
                            }
                        ],
                        "accessory": {
                            "type": 2,
                            "style": 3,
                            "label": "Accepted",
                            "custom_id": "accept_done",
                            "emoji": {"id": "1497991468584014025", "name": "emoji_2"},
                            "disabled": True
                        }
                    }
                ]
            },
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 2,
                        "label": "🇬🇧  English",
                        "custom_id": "punish_lang_en"
                    },
                    {
                        "type": 2,
                        "style": 2,
                        "label": "🇦🇷  Español",
                        "custom_id": "punish_lang_es"
                    },
                    {
                        "type": 2,
                        "style": 2,
                        "label": "🇧🇷  Português",
                        "custom_id": "punish_lang_pt"
                    }
                ]
            }
        ]
    }

def build_ephemeral_content(lang: str) -> dict:
    return {
        "flags": 64,
        "content": PUNISHMENTS_CONTENT[lang]
    }

# ─────────────────────────────────────────────
#  A P I   H E L P E R S
# ─────────────────────────────────────────────

async def send_v2(channel_id: int, payload: dict):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status not in (200, 201):
                text = await resp.text()
                print(f"[ERROR send] {resp.status}: {text}")
            else:
                print("[OK] Mensaje enviado")

async def update_interaction(interaction_id: str, token: str, payload: dict):
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback"
    body = {"type": 7, "data": payload}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers={"Content-Type": "application/json"}) as resp:
            if resp.status not in (200, 201, 204):
                text = await resp.text()
                print(f"[ERROR update] {resp.status}: {text}")

async def respond_ephemeral(interaction_id: str, token: str, payload: dict):
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback"
    body = {"type": 4, "data": payload}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers={"Content-Type": "application/json"}) as resp:
            if resp.status not in (200, 201, 204):
                text = await resp.text()
                print(f"[ERROR ephemeral] {resp.status}: {text}")

# ─────────────────────────────────────────────
#  B O T
# ─────────────────────────────────────────────

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
        await send_v2(CHANNEL_PUNISHMENTS, build_accept_payload())

@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id", "")

    if custom_id == "accept_punishments":
        await update_interaction(
            str(interaction.id),
            interaction.token,
            build_lang_select_payload()
        )

    elif custom_id in ("punish_lang_en", "punish_lang_es", "punish_lang_pt"):
        lang = custom_id.replace("punish_lang_", "")
        await respond_ephemeral(
            str(interaction.id),
            interaction.token,
            build_ephemeral_content(lang)
        )

client.run(TOKEN)
