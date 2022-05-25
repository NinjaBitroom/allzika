import discord
from discord.ext import commands
import psycopg2
from secreto import DATABASE_URL


class Mensagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['auto_mensagem', 'auto_msg', 'automsg'])
    @commands.has_permissions(administrator=True)
    async def auto_message(self, ctx: commands.Context):
        if ctx.author.id != 497560936681570324:
            return await ctx.send('Você não tem permissão de usar este comando!')

        if ctx.invoked_subcommand is None:
            await ctx.send('Nada mudou...')

    @auto_message.command(aliases=['toggle', 'change', 'switch'])
    async def toggle_auto_msg(self, ctx):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        cursor.execute('SELECT valor FROM configs WHERE chave=\'auto_msg\'')

        valor = eval(cursor.fetchone()[0])
        valor = str(not valor)

        cursor.execute('UPDATE configs SET valor=%s WHERE chave=\'auto_msg\'', (valor,))

        conn.commit()
        cursor.close()
        conn.close()

        msg = 'Agora o bot não irá enviar mensagens automáticamente!'
        if eval(valor):
            msg = 'Agora o bot irá enviar mensagens automáticamente!'

        await ctx.send(msg)

    @auto_message.command(aliases=['list', 'l'])
    async def list_auto_msg(self, ctx: commands.Context, auto_id: int = None):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        cursor.execute('SELECT id, titulo, mensagens, horario FROM auto_msg ORDER BY id ASC')
        tabela = cursor.fetchall()

        cursor.close()
        conn.close()

        if auto_id is None:
            texto = ''
            for linha in tabela:
                texto += f'{linha[0]:0>2}. {linha[1]} ({len(linha[2])}) [{linha[3]}]\n'

            embed = discord.Embed(title='Lista de mensagens automáticas',
                                  description=texto,
                                  colour=discord.Colour.gold())
            return await ctx.send(embed=embed)

        auto_msg = []
        for linha in tabela:
            if linha[0] == auto_id:
                auto_msg = linha

        if auto_msg:
            msgs = ''
            contador = 0
            for msg in auto_msg[2]:
                msgs += f'{contador}. {msg}\n'
                contador += 1

            embed = discord.Embed(title=f'Mensagens de \'{auto_msg[1]}\'',
                                  description=msgs,
                                  colour=discord.Colour.green())

            return await ctx.send(embed=embed)

        await ctx.send('Automsg não detectada!')

    @auto_message.command(aliases=['add', 'a'])
    async def add_auto_msg(self, ctx, titulo: str = None, msg: str = None, horario: str = None):
        await ctx.send(f'{titulo} | {msg} | {horario}')


def setup(bot):
    bot.add_cog(Mensagens(bot))
