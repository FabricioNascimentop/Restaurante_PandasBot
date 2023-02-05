import telebot
import pandas
from time import sleep


# definições básicas
bot = telebot.TeleBot("5232274322:AAElp_W6mB9WIELFc2mhqqJy3liPwfyGP1I")
ProductsDF = pandas.DataFrame(pandas.read_excel("C:\TheBigPython\PyProjects\BosTelegram\Restaurante_Pandas.xlsx"))
Contador = []
preços = []
vf = [0]
produtos = []
endereços = []
metodos_pagamentos = []
PedidoDict = {'Produto':produtos, 'Preço':preços, 'Preço_Total':vf, 'Metodo_Pagamento':metodos_pagamentos, 'Endereço':endereços}
# 5248021415 é o meu número "ID", para testes.
TeleID_Cliente = 5248021415


# puxa direto da planilha e verifica se a "comida"(msg) está no cardápio (só funciona nesse arquivo)
def procurador(msg):
    Contador.append(1)
    for c in range(0, len(produtos)):
        if msg.text == f"/Pedido_{c + 1}_{str(produtos[c]).replace('/', '')}":
            produtos.remove(produtos[c])
            preços.remove(preços[c])
            continuar(msg)
    lista = ["Cafe_Da_Manha","Precos_Cafe_Da_Manha","Entradas","Precos_Entradas","Pratos_Feitos","Precos_Pratos_Feitos","Bebidas","Precos_Bebidas"]
    for i in range(0, len(lista)):
        if i//2 == i/2:
            for c in range(0, len(ProductsDF[lista[i]])):
                if str(msg.text).lower() == str(ProductsDF[lista[i]][c]).lower():
                    produtos.append(str(msg.text).replace('/',''))
                    preços.append(float(ProductsDF[lista[i+1]][c]))
                    vf.pop()
                    vf.append(sum(preços))
                    return True



@bot.message_handler(commands=['Retirar_Pedido'])
def retirarpedido(msg):
    if len(produtos) == 0:
        bot.send_message(msg.chat.id,"Você não fez pedido nenhum ainda, deseja ver /menu ? Clique no link azul")
    else:
        bot.send_message(msg.chat.id,f"clique no pedido que deseja retirar")
        for c in range(0, len(produtos)):
            bot.send_message(msg.chat.id,f"/Pedido_{c + 1}_{str(produtos[c]).replace('/','')} - {dinheirinhos(preços[c])}")
        bot.send_message(msg.chat.id,f"Total: {dinheirinhos(sum(preços))}")
        bot.send_message(msg.chat.id,"Deseja voltar ao /menu ?")
        sleep(1)
        bot.send_message(msg.chat.id,"Ou deseja simplesmente continuar seu pedido?")
        bot.send_message(msg.chat.id,"/sim para continuar o pedido")
        return True


# Responder
def responder(msg):
    if len(endereços) > 0:
        endereços.pop()
        endereços.append(msg.text)
        mandar_pedido_cliente(msg)
    return True


# verificar se o cliente tem certeza do seu pedido
@bot.message_handler(func=procurador)
def pedrocertezasbot(msg):
    bot.send_message(msg.chat.id, 'Você tem certeza da sua escolha?')
    bot.send_message(msg.chat.id, '/sim')
    bot.send_message(msg.chat.id, '/nao')


# Negar cadastrar pedido (finalmente)
@bot.message_handler(commands=['nao'])
def cadastro_pedido(msg):
    bot.send_message(msg.chat.id, """seu pedido já foi deletado, deseja voltar ao /menu ? Só clicar no link em azul""")
    preços.pop()
    produtos.pop()

#continuar pedidos ou terminar a operação (ta quase acabando, obg jesus)
@bot.message_handler(commands=['sim'])
def continuar(msg):
    bot.send_message(msg.chat.id, "então vamos prosseguir, o que você deseja?")
    bot.send_message(msg.chat.id, '''/adicionar_produtos
/mostrar_pedidos
/fechar_pedidos''')


#fechar pedido
@bot.message_handler(commands=['fechar_pedidos'])
def pg(msg):
    bot.send_message(msg.chat.id, 'clique no link azul, o que você deseja?')
    bot.send_message(msg.chat.id, '/pix\n' '/cartao\n' '/dinheiro\n')
    return True



#pagamentos
@bot.message_handler(commands=['pix','cartao','dinheiro'])
def pagamento(msg):
    metodos_pagamentos.append(str(msg.text).replace('/',''))
    Endereço(msg)


def Endereço(msg):
    bot.send_message(msg.chat.id,'Qual seu endereço?')
    endereços.append('.')
    return True


#adicionar pedidos
@bot.message_handler(commands=['adicionar_produtos'])
def add_produto(msg):
    cardapio(msg)


#ver pedidos (tem o erro de registrar o "voltar_cardápio" como pedido
@bot.message_handler(commands=['mostrar_pedidos'])
def ver_pedido(msg):
    if len(produtos) == 0:
        bot.send_message(msg.chat.id,"você ainda não fez pedido nenhum")
        bot.send_message(msg.chat.id,"Caso desejes voltar ao /menu clique no link azul")
    else:
        for c in range(0,len(produtos)):
            bot.send_message(msg.chat.id,f"{str(produtos[c]).replace('/','')} - {dinheirinhos(float(preços[c]))}")
        bot.send_message(msg.chat.id,f"Total: {dinheirinhos(float(sum(preços)))}")
        bot.send_message(msg.chat.id,"Deseja /Retirar_Pedido ? Se sim clique no link azul para isso. Caso não")
        sleep(0.5)
        bot.send_message(msg.chat.id,"...")
        sleep(0.5)
        continuar(msg)


#mensagem cardápio
@bot.message_handler(commands=['menu'])
def cardapio(msg):
    bot.send_message(msg.chat.id,'''Com o que desejas começar?
(Você poderá trocar mais tarde)''')
    for c in range(0, len(ProductsDF.columns)):
        if c / 2 == c // 2:
            bot.send_message(msg.chat.id,str('/' + ProductsDF.columns[c]))
    bot.send_message(msg.chat.id,'email para o serviço de suporte: Exemplo2@gmail.com')


#conversor de número chato pra numero dinheirinho
def dinheirinhos(valor):
    if type(valor) == int:
        valor = round(valor, 2)
        return f"R${valor},00"
    if valor * 10 == int(valor * 10):
        valor = round(valor, 2)
        return f"R${str(valor).replace('.',',')}0"
    if int(valor * 100) == int(valor * 100):
        valor = round(valor,2)
        return f"R${str(valor).replace('.',',')}"


#Mostrar Cafés da manhã (C0) (isso ta gramaticalmente certo)
@bot.message_handler(commands=['Cafe_Da_Manha'])
def Café_Da_Manhã(msg):
    for c in range(0, len(ProductsDF['Cafe_Da_Manha'])):
        bot.send_message(msg.chat.id,f"{str(ProductsDF['Cafe_Da_Manha'][c])} {dinheirinhos(float(ProductsDF['Precos_Cafe_Da_Manha'][c]))}")
        #bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id,'para comprar qualquer um desses produtos clique no link azul')
    bot.send_message(msg.chat.id,'você deseja ver o /menu de novo? Clique no link azuk')


#Mostar Entradas (C1) (Working Progress)
@bot.message_handler(commands=['Entradas'])
def Entradas(msg):
    for c in range(0, len(ProductsDF['Entradas'])):
        bot.send_message(msg.chat.id,f"{ProductsDF['Entradas'][c]} {dinheirinhos(float(ProductsDF['Precos_Entradas'][c]))}")
        #bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'Para comprar qualquer um desses produtos clique no link azul')
    bot.send_message(msg.chat.id, 'você deseja ver o /menu de novo? Clique no link azuk')


#Mostrar Pratos principais (C2)
@bot.message_handler(commands=['Pratos_Feitos'])
def Pratos_Feitos(msg):
    for c in range(0, len(ProductsDF['Pratos_Feitos'])):
        bot.send_message(msg.chat.id,f"{ProductsDF['Pratos_Feitos'][c]} {dinheirinhos(float(ProductsDF['Precos_Pratos_Feitos'][c]))}")
        #bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'Para comprar qualquer um desses produtos clique no link azul')
    bot.send_message(msg.chat.id, 'você deseja ver o /menu de novo? Clique no link azuk')


#Mostrar Bebidas WP (C3)
@bot.message_handler(commands=['Bebidas'])
def Bebidas(msg):
    for c in range(0, ProductsDF.shape[0]):
        bot.send_message(msg.chat.id,f"{ProductsDF['Bebidas'][c]} {dinheirinhos(float(ProductsDF['Precos_Bebidas'][c]))}")
        #bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'Para comprar qualquer um desses produtos clique no link azul')
    bot.send_message(msg.chat.id, 'você deseja ver o /menu de novo? Clique no link azuk')


#Mensagem inicial, mensagem de erro e finalização
@bot.message_handler(func=responder)
def Startbase(msg):
    cv = 0
    if sum(Contador) <= 1:
        bot.send_message(msg.chat.id,"Olá, como posso ajudar você?")
        bot.send_message(msg.chat.id, "escreva /menu ou clique no link azul para ver nosso catálogo")
    if len(PedidoDict['Endereço']) > 0 and PedidoDict['Endereço'] != '.' and cv == 0:
            bot.send_message(msg.chat.id, 'Obrigado por usar. Deu bastante trabalho pra fazer')
            cv += 1
    else:
        bot.send_message(msg.chat.id, "Não consigo entender sua mensagem se quiser ver o /menu clique no link azul")

        return False





#vindo das funções e comandos: /pix, /cartao, /dinheiro delimita quando o pedido foi finalizado e o código pode mandar pedido ao cliente
@bot.message_handler(commands=['fechar_pedidos'])
def mandar_pedido_cliente(msg):
    bot.send_message(TeleID_Cliente, f"o pedido de: {msg.from_user.first_name} {msg.from_user.last_name} foi:")
    for c in range(0,len(PedidoDict['Produto'])):
        bot.send_message(TeleID_Cliente,f"{PedidoDict['Produto'][c]} - {dinheirinhos(PedidoDict['Preço'][c])}")
    bot.send_message(TeleID_Cliente,f"""Preço total:{dinheirinhos(float(PedidoDict['Preço_Total'][0]))}
Método de pagamento: {PedidoDict['Metodo_Pagamento'][0]}
Endereço: {PedidoDict['Endereço'][0]}""")



bot.polling()