from discord.ext import commands
import discord
import mongoengine


class Bal(mongoengine.Document):
    _id = mongoengine.IntField(required=True)
    wallet = mongoengine.IntField(default=0)
    bank = mongoengine.IntField(default=0)

    meta = {
        'db_alias': 'core',
        'collection': 'Bal'
    }


'''
Better Way to get MongoDB Data:

cluster = MongoClient("MongoURL")
collection = cluster.database.collection
for data in collection.find({ "_id": member.id }):
    bal = data["bal"]
    return bal

'''


def get_bal(account_id) -> Bal:
    bal = Bal.objects.filter(_id=account_id).first()
    return bal


def create_bal(account_id) -> Bal:
    bal = Bal()
    bal._id = account_id
    bal.bank = 0
    bal.wallet = 0
    bal.save()
    return bal


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bal", brief='Show bal', description='Show balance of the user')
    async def bal_cmd(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            account_id = ctx.author.id
            user = ctx.author

        else:
            account_id = member.id
            user = member
        bal = get_bal(account_id)
        # user = get(self.bot.get_all_members(), id=str(account_id))
        if user:
            pass
        else:
            print("Not found")
            return

        if not bal:
            print("Create new account !")
            bal = create_bal(account_id)
        print("Wallet:", bal.wallet)
        print("Bank:", bal.bank)

        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="Wallet", value="$" + str(bal.wallet), inline=False)
        embed.add_field(name="Bank Balance:", value="$" + str(bal.bank), inline=False)
        embed.set_footer(text="Numix Clone")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
