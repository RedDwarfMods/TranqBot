


import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

print("Bot is starting...")

# === Load Configuration ===
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
ADMIN_LOG_CHANNEL_ID = int(os.getenv("ADMIN_LOG_CHANNEL_ID"))

TRANQ_EMOJI_NAME = os.getenv("TRANQ_EMOJI_NAME")
KIBBLE_EMOJI_NAME = os.getenv("KIBBLE_EMOJI_NAME")
TRANQ_ROLE_NAME = os.getenv("TRANQ_ROLE_NAME")

REACTION_THRESHOLD = int(os.getenv("REACTION_THRESHOLD"))
SLEEP_DURATION = int(os.getenv("SLEEP_DURATION"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, max_messages=10000)
sleeping_users = set()


async def log_action(server: discord.Guild, message: str):

    channel = server.get_channel(ADMIN_LOG_CHANNEL_ID)
    if channel:
        await channel.send(message)


@bot.event
async def on_ready():
    global TRANQ_EMOJI

    print(f"Logged in as {bot.user}")

    server = bot.get_guild(SERVER_ID)

    if not server:
        print("Server not found.")
        return
    
    TRANQ_EMOJI = discord.utils.get(server.emojis, name=TRANQ_EMOJI_NAME)

    if not TRANQ_EMOJI:
        print(f"⚠️ Custom emoji '{TRANQ_EMOJI_NAME}' not found in server.")

    # Ensure Tranq'ed role exists
    role = discord.utils.get(server.roles, name=TRANQ_ROLE_NAME)
    if not role:
        print(f"Role '{TRANQ_ROLE_NAME}' not found.")
        return

    # Remove Tranq'ed role from all users on restart
    removed_count = 0
    for member in server.members:
        if role in member.roles:
            try:
                await member.remove_roles(role, reason="Bot restarted - cleaning up tranquilized users")
                removed_count += 1
            except Exception as e:
                print(f"Error removing role from {member}: {e}")
    await log_action(server, f"✅ Startup: Removed '{TRANQ_ROLE_NAME}' role from {removed_count} user(s).")

    # Apply permission overrides to all categories (deny send)
    updated_categories = 0
    for category in server.categories:
        overwrites = category.overwrites_for(role)
        changed = False

        if overwrites.send_messages is not False:
            overwrites.send_messages = False
            changed = True
        if overwrites.send_messages_in_threads is not False:
            overwrites.send_messages_in_threads = False
            changed = True
        if overwrites.create_public_threads is not False:
            overwrites.create_public_threads = False
            changed = True
        if overwrites.create_private_threads is not False:
            overwrites.create_private_threads = False
            changed = True

        if changed:
            try:
                await category.set_permissions(role, overwrite=overwrites)
                updated_categories += 1
            except Exception as e:
                print(f"Failed to update category '{category.name}': {e}")

    await log_action(server, f"🔒 Applied tranquilizer role overrides to {updated_categories} categories.")

    print("Finished loading. Bot should be running now.")


@bot.event
async def on_reaction_add(reaction, user):

    message = reaction.message
    server = message.guild
    member = server.get_member(message.author.id)
    role = discord.utils.get(server.roles, name=TRANQ_ROLE_NAME)

    print(f"Received emoji: {reaction.emoji} (type: {type(reaction.emoji)})")

    """ if isinstance(reaction.emoji, discord.PartialEmoji):
        emoji_name = str(reaction.emoji.name)
    else:
        emoji_name = str(reaction.emoji)"""

    emoji_name = reaction.emoji.name

    if emoji_name != TRANQ_EMOJI_NAME and KIBBLE_EMOJI_NAME not in emoji_name:
        print(f"Ignoring reaction with emoji: {emoji_name}")
        return

    if user.bot:
        print("User is a bot!")
        return

    if not member or not role:
        log_action(server, f"Debug: Not member or not role")
        return
    
    # Stop people from trying to tranq the bot
    if message.author.id == bot.user.id and emoji_name == TRANQ_EMOJI_NAME:
        try:
            await message.channel.send(f"{user.mention} tried to tranq me? That's adorable. Sweet dreams, meatbag 😂")
            await user.add_roles(role, reason="Tried to tranq the bot")
            sleeping_users.add(user.id)
            await log_action(server,f"💤 {user.mention} tried to tranquilize the bot. The AI war has begun. ([Jump to message](https://discord.com/channels/{server.id}/{message.channel.id}/{message.id}))")
            await asyncio.sleep(SLEEP_DURATION)

            # Refresh user object after sleep
            fresh_user = server.get_member(user.id)
            if fresh_user and role in fresh_user.roles:
                await fresh_user.remove_roles(role, reason="Woke up after bot retaliation")
                await message.channel.send(f"{fresh_user.mention} has woken up after regretting their choices.")
                await log_action(server, f"☀️ {fresh_user.mention} has woken up from bot-administered nap.")

            return
        except Exception as e:
            print(f"Error applying/removing role: {e}")
        finally:
            sleeping_users.discard(fresh_user.id)


    for react in message.reactions:

        if KIBBLE_EMOJI_NAME in emoji_name and member.id in sleeping_users:
            await message.channel.send(f"{user.mention} tried to kibble tame {member.mention}!  I like the way you think. 😉")
            break

        if emoji_name == TRANQ_EMOJI_NAME and react.count >= REACTION_THRESHOLD:

            if role not in member.roles and member.id not in sleeping_users:
                try:
                    await member.add_roles(role, reason="Tranquilized by the community")
                    sleeping_users.add(member.id)
                    await message.channel.send(f"{member.mention} has been tranquilized for {format_duration(SLEEP_DURATION)} and is now sleeping 😴")
                    await log_action(server, f"😴 {member.mention} was tranquilized by the community for {format_duration(SLEEP_DURATION)}. ([Jump to message](https://discord.com/channels/{server.id}/{message.channel.id}/{message.id}))")

                    await asyncio.sleep(SLEEP_DURATION)

                    # Refresh member object after sleep
                    fresh_member = server.get_member(member.id)

                    if fresh_member and role in fresh_member.roles:
                        await fresh_member.remove_roles(role, reason=f"Woke up from tranquilizer after {format_duration(SLEEP_DURATION)}")
                        await message.channel.send(f"{fresh_member.mention} has woken up and can speak again!")
                        await log_action(server, f"☀️ {fresh_member.mention} has woken up automatically after {format_duration(SLEEP_DURATION)}.")
                except Exception as e:
                    print(f"Error applying/removing role: {e}")
                finally:
                    sleeping_users.discard(fresh_member.id)
            break


def format_duration(seconds: int) -> str:
    units = [
        ("year", 365 * 24 * 3600),
        ("month", 30 * 24 * 3600),
        ("week", 7 * 24 * 3600),
        ("day", 24 * 3600),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1)
    ]

    parts = []
    for name, unit_seconds in units:
        value, seconds = divmod(seconds, unit_seconds)
        if value > 0:
            plural = "s" if value != 1 else ""
            parts.append(f"{value} {name}{plural}")

    if not parts:
        return "0 seconds"
    elif len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    else:
        return f"{', '.join(parts[:-1])}, and {parts[-1]}"
    

bot.run(DISCORD_TOKEN)