from logging import getLogger


from discord.ext import commands


from src.data import data


logger = getLogger('bot')


class plugin_connect_command(commands.Cog):
    """シージプラグインと連携しているコマンド群です。
    接続できない時は使うことができません。
    """
    def __init__(self,bot):
        self.bot=bot

    @commands.group()
    async def siege(self,ctx):
        """一番基本的なコマンドです。
        """
        if ctx.invoked_subcommand is None:
            self.bot.help_command.context = ctx
            await self.bot.help_command.send_group_help(ctx.command)

    @siege.command()
    async def tps(self,ctx):
        message = await ctx.reply(
            '情報を取得しています、、、',
            summary_author=False
            )
        sio_id, queue = data.add_b2p_event()
        data.sio.emit(
            'tab_now_tps',
            {
                'to': 'SiegePlugin',
                'id': sio_id,
            }
            )
        now_tps = await queue.get()
        await message.edit(content=now_tps)


def startup(bot):
    bot.add_cog(plugin_connect_command(bot))
