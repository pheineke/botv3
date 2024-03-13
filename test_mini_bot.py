import discord

intents = discord.Intents.all()
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    # Replace 'CHANNEL_ID' with the ID of the channel where you want to check reactions
    channel = client.get_channel(1217200712576929945)
    if channel:
        async for message in channel.history(limit=2):
            if message.author == client.user:
                continue
            previous_message = message
            break

        if previous_message:
            await channel.send(f"Checking reactions on previous message: {previous_message.content}")
            # You can now check for reactions on previous_message

@client.event
async def on_reaction_add(reaction, user):
    print(f"{user} reacted with {reaction.emoji} to the message.")

# Replace 'TOKEN' with your bot's token
client.run('DISCORD_TOKEN')
