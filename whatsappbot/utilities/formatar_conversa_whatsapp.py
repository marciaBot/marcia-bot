arquivo = open("whatsappbot/Conversa do WhatsApp com Wellen.txt", "r")
conversa = arquivo.readlines()
conversa = [c.replace("\n", " ")[19:] for c in conversa]
conversa_formatada = []
resposta_formatada = ""
mesma_pessoa_falando = False
ultima_pessoa_falando = "dsasds"
inicio = 0
for c in conversa:
    if ultima_pessoa_falando in c:
        mesma_pessoa_falando = True
    else:
        mesma_pessoa_falando = False
    try:
        ultima_pessoa_falando = c[:c.index(":")+2]
    except:
        pass
    if mesma_pessoa_falando:
        resposta_formatada += " "+c.replace(ultima_pessoa_falando, "").strip()
    else:
        if resposta_formatada != "":
            conversa_formatada.append(resposta_formatada+"\n")
        resposta_formatada = ""
        resposta_formatada += c.replace(ultima_pessoa_falando, "").strip()

print(conversa_formatada[:10])

saida = open("Conversa_Formatada.txt", "w")
saida.writelines(conversa_formatada)
arquivo.close()
saida.close()
