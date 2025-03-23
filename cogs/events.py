import discord
from discord.ext import commands
from utils.database import db
from config import LOG_CHANNEL_ID

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Member Joined",
                description=f"{member.mention} joined the server",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"ID: {member.id}")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Member Left",
                description=f"{member.mention} left the server",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"ID: {member.id}")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"Message by {message.author.mention} deleted in {message.channel.mention}",
                color=discord.Color.red()
            )
            if message.content:
                embed.add_field(name="Content", value=message.content)
            embed.set_footer(text=f"User ID: {message.author.id}")
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        
        await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Events(bot))
