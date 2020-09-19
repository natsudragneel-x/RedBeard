import discord
from discord.ext import commands


# Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument("Invalid ID") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        re = argument

        if len(re) > 512:
            reason_max = 512 - len(re) - len(argument)
            raise commands.BadArgument(f'Reason is too long ({len(argument)}/{reason_max})')
        return re


class ModeratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason='No reason was given' if reason is None else reason)
            await ctx.send(
                f"{ctx.member.mention} has kicked {member.mention}\n Reason: {'No reason was given' if reason is None else reason}")
            await ctx.send(f"Success :white_check_mark:")

        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason=None):
        m = ctx.guild.get_member(member)
        if m is None:
            await ctx.send("Invalid!")
        try:
            await ctx.guild.ban(discord.Object(id=member), reason='No reason was given' if reason is None else reason)
            await ctx.send(f"They have been banned! \nReason: {'No reason was given' if reason is None else reason}")
            await ctx.send(f"Success :white_check_mark:")

        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason=None):
        try:
            await ctx.guild.unban(discord.Object(id=member), reason='No reason was given' if reason is None else reason)
            await ctx.send("They have been Unbanned! \nReason: {'No reason was given' if reason is None else reason}")
            await ctx.send("Success :white_check_mark:")
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(ModeratorCommands(bot))
