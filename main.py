import discord
import random
import asyncio
import json
from discord.utils import get
from discord.ext import commands
client = commands.Bot(command_prefix="<")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed=discord.Embed(description="Uh, You have used wrong command. Please try again or if you don't know you can simply type '$help'",
    color=0xdd3030)
        await ctx.send(embed=embed)

@client.event
async def on_ready():
   await client.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching,name="You at Kazy's World | Prefix - $"))
   print("Bot is ready")

snipe_ctx_content = None
snipe_ctx_author = None

@client.event
async def on_ctx_delete(ctx, member: discord.Member = None):

    global snipe_ctx_content
    global snipe_ctx_author
    # Variables outside a function have to be declared as global in order to be changed

    snipe_ctx_content = ctx.content
    snipe_ctx_author = ctx.author.id
    await asyncio.sleep(60)
    snipe_ctx_author = None
    snipe_ctx_content = None
    

@client.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@client.command()
async def userinfo(ctx, member: discord.Member):

    role = [role for role in member.roles]

    roles = []
    for role in member.roles:
        roles.append(role)

    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at , inline=False)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id , inline=False)
    embed.add_field(name="Nickname:", value=member.display_name , inline=False)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

    embed.add_field(name=f"Role ({len(roles)})", value=" ".join([role.mention for role in roles]) , inline=False)
    embed.add_field(name="Top Role:", value=member.top_role.mention , inline=False)

    embed.add_field(name="Bot?", value=member.bot , inline=False)

    await ctx.send(embed=embed)

@client.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round (client.latency* 1000)}ms')

@client.command(aliases=['8ball' , 'test'])
async def _8ball(ctx, *,question):
  responses = ['It is certain.',
               'It is decidedly so.',
               'Without a doubt.',
               'Yes - definitely.',
               'You may rely on it.',
               'As I see it, yes.',
               'Most likely.',
               'Outlook good.',
               'Yes.',
               'Signs point to yes.',
               'Reply hazy, try again.',
               'Ask again later.',
               'Better not tell you now.',
               'Cannot predict now.',
               'Concentrate and ask again.',
               "Don't count on it.",
               'My reply is no.',
               'My sources say no.',
               'Outlook not so good.',
               'Very doubtful.']
  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, arg):
	await ctx.send(arg)
	await client.http.delete_message(ctx.channel.id, ctx.message.id)

@client.command()
async def purge(ctx, amount=1):
  if ctx.author.guild_permissions.administrator:
    await ctx.channel.purge(limit=amount + 1)
  else:
    await ctx.send("Only Administrators can do this.")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
   await member.kick(reason=reason)
   await ctx.send("The {user} has been successfully kicked.")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await ctx.send(f"{user} have been bannned sucessfully")

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return

@client.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.add_field(name="Display Name:", value=member.display_name, inline=False)
    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
   await client.get_channel(idchannel).send(f"{member.name} has joined")

@client.event
async def on_member_remove(member):
   await client.get_channel(idchannel).send(f"{member.name} has left")


def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]


@client.command()
@commands.has_role("【🎁】:: Giveaway Perms")
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 60 seconds!")

    questions = ["Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🥳")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")


@client.command()
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}. They won {prize}!")
    




client.run("token")
