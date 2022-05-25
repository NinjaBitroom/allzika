import discord
from discord.ext import commands


class Administrador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['del_men', 'delete_messages', 'del_mens'])
    @commands.has_permissions(administrator=True)
    async def deletar_mensagens(self, ctx: commands.Context, canal: discord.TextChannel, quantidade: int):
        if ctx.author.id not in [497560936681570324, 297556371929300993, 297548590619033603]:
            return await ctx.send('Você não tem permissão de usar este comando!\n'
                                  'Peça para o desenvolvendor te dar a permissão!')
        async for message in canal.history(limit=quantidade):
            await message.delete()

    @commands.group(aliases=['q'])
    @commands.has_permissions(administrator=True)
    async def quest(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Para adicionar uma quest utilize `{self.bot.command_prefix}q add texto1 texto2`\n'
                           f'Ex.: `{self.bot.command_prefix}q add "minecraft pe" "epic games store"`\n'
                           f'Para remover uma quest tente usar `{self.bot.command_prefix}q del num`\n'
                           f'Ex.: `{self.bot.command_prefix}q del 1`')

    @quest.command(aliases=['add', 'adicione', 'a'])
    async def adicionar(self, ctx: commands.Context, jogo: str = None, loja: str = None, link: str = ''):
        if loja is None:
            return await ctx.send(f'Para adicionar uma quest utilize `{self.bot.command_prefix}q add texto1 texto2`\n'
                                  f'Ex.: `{self.bot.command_prefix}q add "minecraft pe" "epic games store"`\n')

        mural = self.bot.get_channel(583068172710707220)

        numeros = []
        async for message in mural.history(limit=200):
            if message.embeds:
                embed = message.embeds[0]
                if not embed.description:
                    continue
                if not embed.description.startswith('#'):
                    continue
                num = int(embed.description[1:])
                numeros.append(num)

        quest_id = 1000
        for i in range(1000):
            if i not in numeros:
                quest_id = i
                break

        with open('./imagens/Pasteugusto_rosto.png', 'rb') as pasteugusto:
            pasteru = await mural.create_webhook(name='Pasteugusto', avatar=pasteugusto.read())

        jogo = jogo.upper()
        loja_dividida = loja.split(' ')
        novo_nome = []
        for nome in loja_dividida:
            novo_nome.append(nome.capitalize())
        loja = ' '.join(novo_nome)

        embed = discord.Embed(description=f'#{quest_id:0>3}', title=f'**{jogo} ({loja})**',
                              colour=discord.Colour.green())
        embed.set_footer(text=f'Requisitado por {ctx.author.name}')

        await pasteru.send(f'@everyone {link}', embed=embed)
        await pasteru.delete()
        await ctx.send(f'Quest "{jogo} on {loja}" adicionado no {mural.mention} com o id #{quest_id:0>3}')

    @quest.command(aliases=['del', 'remove', 'delete', 'rm', 'rmv', 'rem', 'd', 'remover'])
    async def deletar(self, ctx, *, q_id: str = None):
        if q_id is None:
            return await ctx.send(f'Para remover uma quest tente usar `{self.bot.command_prefix}q del num`\n'
                                  f'Ex.: `{self.bot.command_prefix}q del 1`')

        mural = self.bot.get_channel(583068172710707220)

        ids = q_id.split()
        str_q = []
        for i in range(len(ids)):
            try:
                int_q = int(ids[i])
            except ValueError:
                await ctx.send(f'Erro ao deletar as quests. Tente `{self.bot.command_prefix}q del 1 2`')
                return

            str_q.append(f'#{int_q:0>3}')

        async for message in mural.history(limit=999):
            if message.embeds:
                embed = message.embeds[0]
                if not embed.description:
                    continue
                if not embed.description.startswith('#'):
                    continue
                if embed.description in str_q:
                    await ctx.send(f'Deletando quest {embed.title}...')
                    await message.delete()
                    await ctx.send(f'Quest com o ID:{embed.description} deletada!')


def setup(bot):
    bot.add_cog(Administrador(bot))
