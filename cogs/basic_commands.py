import discord
from discord import app_commands
from discord.ext import commands
from config import BOT_NAME, BOT_VERSION, BOT_CREATOR

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check if the bot is online")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="help", description="Show available commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Basic Commands",
            value="`/ping` - Check bot status\n"
                  "`/help` - Show this help message\n"
                  "`/info` - Show bot information\n"
                  "`/server` - Show server information\n"
                  "`/user` - Show user information",
            inline=False
        )
        
        embed.add_field(
            name="Moderation Commands",
            value="`/kick` - Kick a user\n"
                  "`/ban` - Ban a user\n"
                  "`/warn` - Warn a user\n"
                  "`/clear` - Clear messages",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Show bot information")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Information",
            color=discord.Color.blue()
        )
        embed.add_field(name="Name", value=BOT_NAME)
        embed.add_field(name="Version", value=BOT_VERSION)
        embed.add_field(name="Creator", value=BOT_CREATOR)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="server", description="Show server information")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Server Information - {guild.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Server ID", value=guild.id)
        embed.add_field(name="Member Count", value=guild.member_count)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"))
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="user", description="Show user information")
    async def user(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(
            title=f"User Information - {member.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="User ID", value=member.id)
        embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Roles", value=", ".join([role.name for role in member.roles[1:]]))
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
