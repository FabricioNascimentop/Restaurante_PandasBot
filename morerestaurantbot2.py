import telebot
import pandas

# definições básicas
Contador = {'C_start': [],'C_rodar':[]}
bot = telebot.TeleBot("5232274322:AAElp_W6mB9WIELFc2mhqqJy3liPwfyGP1I")
ProductsDF = pandas.DataFrame(pandas.read_excel("C:\TheBigPython\PyProjects\BosTelegram\Products_Exemple.xlsx"))
pedidos = []
# 5248021415 é o meu número "ID", para testes.
TeleID_Cliente = 5248021415


# puxa direto da planilha e verifica se a "comida"(msg) está no cardápio (só funciona nesse arquivo)
def procurador(msg):
    lista = ['Category0', 'Category1', 'Category2', 'Category3']
    for li in range(0, len(lista)):
        for c in range(0, ProductsDF.shape[0]):
            if str(msg.text).lower() == str(ProductsDF[lista[li]][c]).lower():
                return True
    Contador['C_rodar'].append(1)

    if sum(Contador['C_rodar']) == 0:
        print(msg)


# Responder
def responder(msg):
    return True


# verificar se o cliente tem certeza do seu pedido
@bot.message_handler(func=procurador)
def pedrocertezasbot(msg):
    bot.send_message(msg.chat.id, 'Are you sure of your choice?')
    bot.send_message(msg.chat.id, '/yes')
    bot.send_message(msg.chat.id, '/not')
    pedidos.append(msg.text)


# Negar cadastrar pedido (finalmente)
@bot.message_handler(commands=['not'])
def cadastro_pedido(msg):
    bot.send_message(msg.chat.id, """
your order has already been deleted, do you want to go back to /menu? Just click on the purple link""")


#continuar pedidos ou terminar a operação (ta quase acabando, obg jesus)
@bot.message_handler(commands=['yes'])
def continuar(msg):
    bot.send_message(msg.chat.id, "so let's proceed, what do you want")
    bot.send_message(msg.chat.id, '''/add_products
/show_orders
/close_orders''')


#fechar pedido
@bot.message_handler(commands=['close_orders'])
def pg(msg):
    bot.send_message(msg.chat.id, 'click in the purple link, what you want?')
    bot.send_message(msg.chat.id, '/pix\n' '/card\n' '/money\n')

    #mandar mensagem para cliente com o pedido
    bot.send_message(5248021415,f"o pedido de:{msg.from_user.first_name} {msg.from_user.last_name} foi {pedidos}")
    for p in range(0,len(pedidos)):
        bot.send_message(5248021415,pedidos[p])

#pagamento com pix
@bot.message_handler(commands=['pix'])
def pg_pix(msg):
    bot.send_message(msg.chat.id,'pay to email: Exemple@gmail.com')

#pagamento com cartão
@bot.message_handler(commands=['card'])
def pg_cartao(msg):
    bot.send_message(msg.chat.id,'please have the card in hand. The delivery man will take the machine')

#pagamento com dinheiro (cringe e ultrapassado)
@bot.message_handler(commands=['money'])
def pg_dinheiro(msg):
    bot.send_message(msg.chat.id,'please facilitate the change, give the money to the delivery person')


#adicionar pedidos
@bot.message_handler(commands=['add_products'])
def add_produto(msg):
    cardapio(msg)


#ver pedidos (tem o erro de registrar o "voltar_cardápio" como pedido
@bot.message_handler(commands=['show_orders'])
def ver_pedido(msg):
    from time import sleep
    for c in range(0,len(pedidos)):
        bot.send_message(msg.chat.id,pedidos[c])
    bot.send_message(msg.chat.id,'okay?')
    sleep(0.3)
    bot.send_message(msg.chat.id,'.')
    sleep(0.2)
    bot.send_message(msg.chat.id, '.')
    sleep(0.1)
    bot.send_message(msg.chat.id, '.')
    continuar(msg)


#mensagem cardápio
@bot.message_handler(commands=['menu'])
def cardapio(msg):
    bot.send_message(msg.chat.id,'''What you want to start? 
(Choose one, later you may be catch another)''')
    for c in range(0, len(ProductsDF.columns)):
        if c / 2 == c // 2:
            bot.send_message(msg.chat.id,str('/' + ProductsDF.columns[c]))
    bot.send_message(msg.chat.id,'email to Support Service: Exemple@gmail.com')


#Mostrar Cafés da manhã (C0) (isso ta gramaticalmente certo)
@bot.message_handler(commands=['Category0'])
def Café_Da_Manhã(msg):
    for c in range(0, ProductsDF.shape[0]):
        bot.send_message(msg.chat.id,f"{str(ProductsDF.columns[0])}\n{str(ProductsDF['Category0'][c])}\n{'$'+str(ProductsDF['Price_Category0'][c])+'.00'}")
        bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id,'to buy everyone of this products click in the purple name')
    bot.send_message(msg.chat.id,'You want to see the /menu again? Click in te purple link')


#Mostar Entradas (C1) (Working Progress)
@bot.message_handler(commands=['Category1'])
def Entradas(msg):
    for c in range(0, ProductsDF.shape[0]):
        bot.send_message(msg.chat.id,f"{str(ProductsDF.columns[2])}\n{ProductsDF['Category1'][c]}\n{'$'+str(ProductsDF['Price_Category1'][c])+'.00'}")
        bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'to buy everyone of this products click in the purple name')
    bot.send_message(msg.chat.id, 'You want to see the /menu again? Click in te purple link')

#Mostrar Pratos principais (C2)
@bot.message_handler(commands=['Category2'])
def Pratos_Feitos(msg):
    for c in range(0, ProductsDF.shape[0]):
        bot.send_message(msg.chat.id,f"{(ProductsDF.columns[4])}\n{ProductsDF['Category2'][c]}\n{'$' + str(ProductsDF['Price_Category2'][c]) + '.00'})")
        bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'to buy everyone of this products click in the purple name')
    bot.send_message(msg.chat.id, 'You want to see the /menu again? Click in te purple link')


#Mostrar Bebidas WP (C3)
@bot.message_handler(commands=['Category3'])
def Bebidas(msg):
    for c in range(0, ProductsDF.shape[0]):
        bot.send_message(msg.chat.id,f"{str(ProductsDF.columns[6])}\n{ProductsDF['Category3'][c]}\n{'$' + str(ProductsDF['Price_Category3'][c]) + '.00'})")
        bot.send_photo(msg.chat.id, "https://pbs.twimg.com/media/Fa2KO9TXwAI7Okn?format=png&name=medium")
    bot.send_message(msg.chat.id, 'to buy everyone of this products click in the purple name')
    bot.send_message(msg.chat.id, 'You want to see the /menu again? Click in te purple link')


#Voltar ao Cardápio
@bot.message_handler(commands=['Voltar_Cardapio'])
def voltar_Cardapio(msg):
    for c in range(0, len(ProductsDF.columns)):
        if c / 2 == c // 2:
            bot.send_message(msg.chat.id,str('/' + ProductsDF.columns[c]))


#Mensagem inicial e mensagem de erro
@bot.message_handler(func=responder)
def Startbase(msg):
    if sum(Contador['C_start']) < 1:
        Contador['C_start'].append(1)
        bot.send_message(msg.chat.id,"hi, how i can help you?")
        bot.send_message(msg.chat.id, "write /menu or click in the purple links to see our products")
    else:
        bot.send_message(msg.chat.id, "i can't understanding you mensage, if you want to see /menu click in the purple link")
        return False


bot.polling()