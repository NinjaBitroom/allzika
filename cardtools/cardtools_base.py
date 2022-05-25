import random


class Carta:
    def __init__(self, atributos: iter):
        self.id = atributos[0]
        self.nome = atributos[1]
        self.ataque = atributos[2]
        self.defesa = atributos[3]
        self.destreza = atributos[4]
        self.vida = atributos[5]
        self.raridade = atributos[6]
        self.imagem = atributos[7]
        self.dados = [0]

        self.vida_max = self.vida
        self.vida_padrao = self.vida
        self.vida_atual = self.vida

        self.bonus_ataque = 0
        self.bonus_defesa = 0
        self.bonus_destreza = 0
        self.bonus_dados = 0

    def rolar_dados(self, dados: str = '1d6'):
        separado = dados.split('d')
        resultados = []
        for dado in range(int(separado[0])):
            resultados.append(random.randint(1, int(separado[1])))

        return resultados

    def atacar(self):
        resultado_dado = sum(self.rolar_dados())
        resultado = resultado_dado + self.bonus_ataque
        return resultado


class Jogador:
    def __init__(self, player_id: int, nome: str, carta: Carta):
        self.id = player_id
        self.nome = nome
        self.carta = carta
        self.cartas = [carta]
        self.turno_atq = 0

    async def defender(self, *args, **kwargs):
        pass
