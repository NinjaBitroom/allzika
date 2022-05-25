from discord.ext import commands
import discord


class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['help'])
    async def ajuda(self, ctx, *, comando: str = None):
        message = ctx.message

        if comando is None:
            embed = discord.Embed(title='Comandos disponíveis no momento:', colour=discord.Colour.gold())
            embed.add_field(name='🖥Comandos🖥',
                            value=f'{self.bot.command_prefix}desafio\n'
                                  f'{self.bot.command_prefix}wiki (pesquisa)\n'
                                  f'{self.bot.command_prefix}bolsad [membro]\n'
                                  f'{self.bot.command_prefix}coin [membro]\n'
                                  f'{self.bot.command_prefix}ajuda [comando]\n'
                                  f'{self.bot.command_prefix}rank\n'
                                  f'{self.bot.command_prefix}say (texto)\n'
                                  f'{self.bot.command_prefix}ssay (texto)\n'
                                  f'{self.bot.command_prefix}daily\n'
                                  f'{self.bot.command_prefix}eval (expressão)')
            embed.add_field(name='🃏CardGame🃏',
                            value=f'{self.bot.command_prefix}mycards [membro]\n'
                                  f'{self.bot.command_prefix}info (id)\n'
                                  f'{self.bot.command_prefix}gacha (id)\n'
                                  f'{self.bot.command_prefix}fight (id) [membro/id]\n'
                                  f'{self.bot.command_prefix}free\n'
                                  f'{self.bot.command_prefix}minfo (id)')
            embed.add_field(name='🎁Outros🎁',
                            value='ayaya\n'
                                  'tuturu\n'
                                  'fbi\n'
                                  'lolicon\n'
                                  'stonks\n'
                                  'not stonks\n'
                                  'confused stonks\n'
                                  'padoru\n'
                                  'nep\n'
                                  'abababa')
            embed.add_field(name='🛠Admin🛠',
                            value=f'{self.bot.command_prefix}del_mens (canal) (quantidade)\n'
                                  f'{self.bot.command_prefix}quest (comando)')
            embed.add_field(name='Parâmetros:',
                            value='(Obrigatório)\n'
                                  '[Opcional]')
        else:
            embed = discord.Embed(colour=discord.Colour.gold())
            # COMANDOS
            if comando in [f'{self.bot.command_prefix}desafio', 'desafio']:
                nome = f'{self.bot.command_prefix}desafio'
                valor = 'Pensarei em um número de 1 a 10, ' \
                        'se você não responder em 5 segundos ou ' \
                        'se sua resposta não for o número que estou pensando, ' \
                        'perde! Será gasto 1 conto ao desafiar e se ganhar receberá ' \
                        '10 contos!'

            elif comando in [f'{self.bot.command_prefix}wiki', 'wiki', 'wikipedia', f'{self.bot.command_prefix}wikipedia']:
                nome = f'{self.bot.command_prefix}wiki (pesquisa)'
                valor = 'Exibe até 3 resultados de uma pesquisa no ' \
                        'Wikipedia. Este comando pode demorar ' \
                        'um pouco.'

            elif comando in [f'{self.bot.command_prefix}bolsad', f'{self.bot.command_prefix}bd', f'{self.bot.command_prefix}bolsadelicia',
                             'bolsad', 'bd', 'bolsadelicia']:
                nome = f'{self.bot.command_prefix}bolsad [membro]'
                valor = f'Exibe o cartão do Bolsa Delícia de algum membro do servidor.\n' \
                        f'Você pode usar o alias `{self.bot.command_prefix}bd`'

            elif comando in ['coin', 'coins', 'conto', 'contos', 'moeda', 'moedas', 'dinheiro',
                             f'{self.bot.command_prefix}coin', f'{self.bot.command_prefix}coins', f'{self.bot.command_prefix}conto',
                             f'{self.bot.command_prefix}contos', f'{self.bot.command_prefix}moeda', f'{self.bot.command_prefix}moedas',
                             f'{self.bot.command_prefix}dinheiro']:
                nome = f'{self.bot.command_prefix}coin [membro]'
                valor = 'Exibe quantos contos o membro possui.'

            elif comando in [f'{self.bot.command_prefix}ajuda', f'{self.bot.command_prefix}help', 'ajuda', 'help']:
                nome = f'{self.bot.command_prefix}ajuda [comando]'
                valor = 'Exibe uma lista de comandos ou ' \
                        'uma explicação sobre algum comando.'

            elif comando in [f'{self.bot.command_prefix}rank', 'rank', f'{self.bot.command_prefix}ranking', 'ranking']:
                nome = f'{self.bot.command_prefix}rank'
                valor = 'Exibe a qunatidade de vezes que cada um pegou na madeira.'

            elif comando in [f'{self.bot.command_prefix}say', 'say', 'diga', 'fale', 'falar', 'dizer',
                             f'{self.bot.command_prefix}diga', f'{self.bot.command_prefix}fale', f'{self.bot.command_prefix}falar',
                             f'{self.bot.command_prefix}dizer']:
                nome = f'{self.bot.command_prefix}say (texto)'
                valor = 'Deixe o bot falar por você.'

            elif comando in ['supersay', 'superfala', 'ss', 'supers', 'ssay',
                             f'{self.bot.command_prefix}supersay', f'{self.bot.command_prefix}superfala', f'{self.bot.command_prefix}ss',
                             f'{self.bot.command_prefix}supers', f'{self.bot.command_prefix}ssay']:
                nome = f'{self.bot.command_prefix}ssay (texto)'
                valor = 'Deixe o bot te copiar e falar por você.'

            elif comando in [f'{self.bot.command_prefix}daily', 'daily']:
                nome = f'{self.bot.command_prefix}daily'
                valor = 'Contos diarios.'

            elif comando in ['eval', f'{self.bot.command_prefix}eval']:
                nome = f'{self.bot.command_prefix}eval (expressão)'
                valor = 'Exibe o resultado de uma expressão!'

            # CARDGAME
            elif comando in ['my_cards', 'mycards', 'mc',
                             f'{self.bot.command_prefix}my_cards', f'{self.bot.command_prefix}mycards', f'{self.bot.command_prefix}mc']:
                nome = f'{self.bot.command_prefix}mycards [membro]'
                valor = f'Exibe as suas cartas.\n' \
                        f'Use o alias `{self.bot.command_prefix}mc` para o mesmo efeito.'

            elif comando in ['info', 'inf', 'in', 'i',
                             f'{self.bot.command_prefix}info', f'{self.bot.command_prefix}inf', f'{self.bot.command_prefix}in',
                             f'{self.bot.command_prefix}i']:
                nome = f'{self.bot.command_prefix}info (id)'
                valor = 'Exibe as informações de uma carta.'

            elif comando in [f'{self.bot.command_prefix}gacha', 'gacha']:
                nome = f'{self.bot.command_prefix}gacha (id)'
                valor = f'Tente a sorte em um gacha! ' \
                        f'`{self.bot.command_prefix}gacha` para mais informações!'

            elif comando in [f'{self.bot.command_prefix}fight', 'fight']:
                nome = f'{self.bot.command_prefix}fight (id) [membro/id]'
                valor = 'Lute contra alguém! Você também pode lutar contra um BOT! ' \
                        'Basta digitar um número ou não digitar nada no lugar do membro.'

            elif comando in ['free', f'{self.bot.command_prefix}free']:
                nome = f'{self.bot.command_prefix}free'
                valor = 'Gacha grátis! Só pode ser usado uma vez por pessoa!'

            elif comando in ['miniinfo', 'mininfo', 'minfo', 'minin', 'mi',
                             f'{self.bot.command_prefix}miniinfo', f'{self.bot.command_prefix}mininfo', f'{self.bot.command_prefix}minfo',
                             f'{self.bot.command_prefix}minin', f'{self.bot.command_prefix}mi']:
                nome = f'{self.bot.command_prefix}minfo'
                valor = f'Comando `{self.bot.command_prefix}info` só que em um embed menor.\n' \
                        f'Use `{self.bot.command_prefix}mi` para o mesmo efeito.'
            # OUTROS
            elif comando == 'ayaya':
                nome = comando
                valor = 'Ayaya~'

            elif comando == 'tuturu':
                nome = comando
                valor = 'Tuturuuuuuu...'

            elif comando == 'fbi':
                nome = comando
                valor = 'Liga pro FBI!'

            elif comando == 'lolicon':
                nome = comando
                valor = '~~Emmanuel~~'

            elif comando == 'stonks':
                nome = comando
                valor = 'Stonks!'

            elif comando == 'not stonks':
                nome = comando
                valor = 'Not stonks!'

            elif comando == 'confused stonks':
                nome = comando
                valor = 'Confused stonks!'

            elif comando == 'padoru':
                nome = comando
                valor = 'Padoru padoruuuuu'

            elif comando == 'nep':
                nome = comando
                valor = 'Nep nep'

            elif comando in ['abababa', 'awawawa']:
                nome = comando
                valor = comando.capitalize()

            # ADMINISTRADOR
            elif comando in ['deletar_mensagens', 'del_men', 'delete_messages', 'del_mens',
                             f'{self.bot.command_prefix}deletar_mensagens', f'{self.bot.command_prefix}del_men',
                             f'{self.bot.command_prefix}delete_messages', f'{self.bot.command_prefix}del_mens']:
                nome = f'{self.bot.command_prefix}del_mens (canal) (quantidade)'
                valor = 'Comando para deletar várias mensagens de um canal... ' \
                        'Cuidado ao usar este comando!'

            elif comando in [f'{self.bot.command_prefix}quest', 'quest', f'{self.bot.command_prefix}q', 'q']:
                nome = f'{self.bot.command_prefix}quest (comando)'
                valor = f'Comando para adicionar ou remover quests. ' \
                        f'`{self.bot.command_prefix}q add "texto1" "texto2"` para adicionar uma quest. ' \
                        f'`{self.bot.command_prefix}q del 1 2` para remover quests.'

            else:
                nome = f'Comando não existe!'
                valor = f'Não foi possível achar o comando "{comando}"'

            embed.add_field(name=nome, value=valor)
        await message.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.remove_command('help')
    bot.add_cog(Ajuda(bot))
