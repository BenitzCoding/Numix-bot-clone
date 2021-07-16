from discord.ext import commands
import discord
import mongoengine


class Prefix(mongoengine.Document):
    _id = mongoengine.IntField(required=True)
    prefix = mongoengine.StringField(default="c!")

    def get_id(self):
        return self._id

    meta = {
        'db_alias': 'core',
        'collection': 'Prefix'
    }


prefix_map = dict()
default_prefix = "c!"


def prefix_get(bot, message):
    server_id = message.guild.id
    if str(server_id) in prefix_map:
        return prefix_map[(str(server_id))]
    return default_prefix


def get_prefix_map():
    for prefix in Prefix.objects():
        prefix_map[str(prefix.get_id())] = prefix.prefix
get_prefix_map()


def set_prefix(prefix_id, prefix: str):
    prefix_data = Prefix.objects.filter(_id=prefix_id).first()
    if prefix_data is None:
        prefix_data = Prefix(_id=prefix_id)
    prefix_data.prefix = prefix
    prefix_data.save()
    get_prefix_map()


class PrefixCommand(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(name="prefix", brief='Prefix command',
                      description='Set and get information of prefix for the server')
    async def prefix_cmd(self, ctx: commands.Context, *args):
        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.set_author(name="Numix Clone Bot", icon_url=self.bot.user.avatar_url)
        if len(args) == 0 or (len(args) == 1 and args[0] == "info"):
            prefix = prefix_map.get(str(ctx.guild.id), default_prefix)
            if prefix == default_prefix:
                embed.description = f"You're currently using the Default Prefix which is `{default_prefix}` " + \
                                    f"You can change the prefix with `{default_prefix} prefix set <new prefix>`"
            else:
                embed.add_field(name="Prefix", value=f"`{prefix}`")
        elif len(args) == 2 and args[0] == "set":
            set_prefix(ctx.guild.id, args[1])
            embed.description = f"Prefix changed for `{args[1]}`"
        self.bot.command_prefix = prefix_get
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PrefixCommand(bot))
