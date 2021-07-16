from discord.ext import commands
import discord


class General(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="links", brief='Show links', description='Show links associated to the bots')
    async def links_cmd(self, ctx: commands.Context):
        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.set_author(name="Numix Clone Bot", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Website Link", value="https://numix.xyz/", inline=False)
        embed.add_field(name="Bot Invite", value="https://numix.xyz/invite", inline=False)
        embed.add_field(name="Support Server", value="https://numix.xyz/discord", inline=False)
        embed.set_footer(text="Numix Clone")
        await ctx.send(embed=embed)

    @commands.command(name="info", brief='Show infos', description='Show informations of the bot')
    async def info_cmd(self, ctx: commands.Context):
        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.set_author(name="Numix Clone Bot", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Developers:", value="`Aehrin/RaconteurDesMondes#8400`", inline=False)
        embed.add_field(name="Bot Version:", value=f"`1.0`", inline=False)
        embed.add_field(name="Support Server:", value="https://numix.xyz/discord", inline=False)
        embed.add_field(name="Ping:", value=f"`{str(round(self.bot.latency * 1000, 1))}` ms", inline=False)
        embed.add_field(name="Invited Servers:", value=f"`{str(len(list(self.bot.guilds)))}` Servers", inline=False)
        embed.add_field(name="Loaded Commands:", value=f"`{str(len(list(self.bot.commands)))}` Commands", inline=False)
        embed.set_footer(text="Numix Clone")
        await ctx.send(embed=embed)

    @commands.command(name="help", brief='Show help', description='Show this help')
    async def help_cmd(self, ctx: commands.Context, command_name: str = None):
        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.set_author(name="Numix Clone Bot", icon_url=self.bot.user.avatar_url)
        if command_name is not None:
            for it in list(self.bot.commands):
                command: commands.Command = it
                if command.name == command_name:
                    embed.add_field(name=command.name, value=command.description, inline=False)
                    break
        else:
            for it in list(self.bot.commands):
                command: commands.Command = it
                if command.description:
                    embed.add_field(name=command.name, value=command.description, inline=False)
            embed.set_footer(text="Numix Clone")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
