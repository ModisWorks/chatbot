import logging

from modis import main
from modis.tools import data
from . import _data, api_mitsuku

logger = logging.getLogger(__name__)


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # Simplify message info
    guild = message.guild
    author = message.author
    channel = message.channel
    content = message.content

    # Only reply to guild messages and don't reply to myself
    if guild is not None and author != main.client.user:
        # Only reply to mentions
        if main.client.user in message.mentions:

            logger.info("Bot was mentioned, summoning Mitsuku")
            await channel.trigger_typing()

            # Get new botcust2 from Mitsuku if does not exist for channel in database
            if channel.id not in data.get(guild.id, "chatbot", ["channels"]):
                data.edit(guild.id, "chatbot", str(channel.id), ["channels"])
                data.edit(guild.id, "chatbot", api_mitsuku.get_botcust2(), ["channels", str(channel.id)])

            # Get botcust2 from database
            botcust2 = data.get(guild.id, "chatbot", ["channels", str(channel.id)])

            # Remove mention from message content so Mitsuku doesn't see it
            content = content.replace("<@{}>".format(str(main.client.user.id)), ' ')
            content = content.replace("<@!{}>".format(str(main.client.user.id)), ' ')

            # Send Mitsuku's reply
            if botcust2:
                response = api_mitsuku.query(botcust2, content)
                if response:
                    await channel.send(response)
                else:
                    await channel.send("```Couldn't get readable response from Mitsuku.```")
            else:
                await channel.send("```Couldn't initialise with Mitsuku.```")
