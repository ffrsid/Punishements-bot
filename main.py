import discord
import os
import asyncio
import aiohttp

TOKEN = os.environ["DISCORD_TOKEN"]
APPLICATION_ID = int(os.environ.get("APPLICATION_ID", "0"))
CHANNEL_PUNISHMENTS = 1497364541024112720
REQUIRED_ROLE_ID = 1497010109824499923

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
#  L A N G   O P T I O N S  (custom emojis)
# ─────────────────────────────────────────────

LANG_OPTIONS = [
    {
        "label": "English",
        "value": "en",
        "emoji": {"id": "1499826848035766454", "name": "emoji_3"}
    },
    {
        "label": "Español",
        "value": "es",
        "emoji": {"id": "1499826873226629241", "name": "emoji_5"}
    },
    {
        "label": "Português",
        "value": "pt",
        "emoji": {"id": "1499826860794708069", "name": "emoji_4"}
    }
]

# ─────────────────────────────────────────────
#  P A Y L O A D S
# ─────────────────────────────────────────────

def build_accept_payload() -> dict:
    """Mensaje inicial en el canal con el botón Accepted (sin color)."""
    return {
        "flags": 1 << 15,
        "components": [
            {
                "type": 17,
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


def build_ephemeral_accepted() -> dict:
    """Ephemeral: Punishments Accepted + select de idiomas."""
    return {
        "content": (
            "**Punishments Accepted** — You have acknowledged the punishment system "
            "of **Celestials Dragons**.\n\n"
            "Select your language below to view the punishments."
        ),
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "punish_lang_select",
                        "placeholder": "Select your language...",
                        "options": LANG_OPTIONS
                    }
                ]
            }
        ]
    }


def build_ephemeral_lang_select() -> dict:
    """Ephemeral: select de idiomas (después de Back)."""
    return {
        "content": "Select your language below to view the punishments.",
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "punish_lang_select",
                        "placeholder": "Select your language...",
                        "options": LANG_OPTIONS
                    }
                ]
            }
        ]
    }


def build_ephemeral_punishment(lang: str) -> dict:
    """Ephemeral: contenido de punishments + botón Back azul."""
    return {
        "content": PUNISHMENTS_CONTENT[lang],
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 1,
                        "label": "Back",
                        "custom_id": "back_to_langs"
                    }
                ]
            }
        ]
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


async def defer_ephemeral(interaction_id: str, token: str):
    """Type 5: respuesta ephemeral diferida (muestra 'thinking...' / cargando)."""
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback"
    body = {"type": 5, "data": {"flags": 64}}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers={"Content-Type": "application/json"}) as resp:
            if resp.status not in (200, 201, 204):
                text = await resp.text()
                print(f"[ERROR defer] {resp.status}: {text}")


async def edit_deferred(token: str, payload: dict):
    """Edita la respuesta diferida via webhook."""
    url = f"https://discord.com/api/v10/webhooks/{APPLICATION_ID}/{token}/messages/@original"
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, headers={"Content-Type": "application/json"}) as resp:
            if resp.status not in (200, 201, 204):
                text = await resp.text()
                print(f"[ERROR edit_deferred] {resp.status}: {text}")


async def update_interaction(interaction_id: str, token: str, payload: dict):
    """Type 7: actualiza el mensaje al que pertenece el componente."""
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{token}/callback"
    body = {"type": 7, "data": payload}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers={"Content-Type": "application/json"}) as resp:
            if resp.status not in (200, 201, 204):
                text = await resp.text()
                print(f"[ERROR update] {resp.status}: {text}")

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

    # ── Accepted: verificar rol ──
    if custom_id == "accept_punishments":
        await defer_ephemeral(str(interaction.id), interaction.token)
        await asyncio.sleep(1)

        has_role = any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles)

        if has_role:
            await edit_deferred(interaction.token, build_ephemeral_accepted())
        else:
            await edit_deferred(interaction.token, {
                "content": (
                    "**Rejected** — You do not have the required role "
                    "to access the punishment system."
                )
            })

    # ── Select de idioma → muestra punishments ──
    elif custom_id == "punish_lang_select":
        lang = interaction.data.get("values", ["en"])[0]
        await update_interaction(
            str(interaction.id),
            interaction.token,
            build_ephemeral_punishment(lang)
        )

    # ── Back → regresa a la selección de idiomas ──
    elif custom_id == "back_to_langs":
        await update_interaction(
            str(interaction.id),
            interaction.token,
            build_ephemeral_lang_select()
        )


client.run(TOKEN)
