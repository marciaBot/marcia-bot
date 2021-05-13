import re
pattern_data = r"(?<=\d{2}\/\d{2}\/\d{4}\s\d{2}\:\d{2}\s\-\s).*"
pattern_name = r"(?<=:\s).+"
arquivo = open("whatsappbot/Conversa do WhatsApp com Wellen.txt", "r")
conversa = arquivo.readlines()
conversa = [re.search(pattern_data, c) for c in conversa]
conversa = [(re.search(pattern_name, c.group()).group() if re.search(pattern_name, c.group()) is not None else "" )if c is not None else "" for c in conversa]
saida = open("Conversa_Formatada.txt", "w")
saida.writelines(conversa)
arquivo.close()
saida.close()
