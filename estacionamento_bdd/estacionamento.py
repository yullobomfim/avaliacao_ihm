from time import sleep
import face_recognition
import json
import simpy
import random
 
FOTOS_MOTORISTAS = [
                "./fotos/ayrton1.jpeg",
                "./fotos/ayrton2.jpeg",
                "./fotos/ayrton3.jpeg",
                "./fotos/roberto1.jpeg",
                "./fotos/roberto2.jpeg",
                "./fotos/roberto3.jpeg", 
                "./fotos/zeca1.jpeg",
                "./fotos/zeca2.jpeg",
                "./fotos/zeca3.jpeg",                
                "./fotos/rubinho1.jpeg",
                "./fotos/rubinho2.jpeg",
                "./fotos/rubinho3.jpeg",                
                "./fotos/ronaldo.jpeg",
                "./fotos/romario.jpeg",
]

ARQUIVO_CONFIGURACAO = "./configuracao.json"

def carregar_arquivos():
    with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)
    arquivo_configuracao.close()
    return configuracao

def simular_reconhecimento_facial(foto_cliente):
    foto = {
        "foto": foto_cliente
    }
    return foto

def reconhecer_cliente(foto_cliente_simulacao):
    reconhecido = False
    total_reconhecimentos = 0
    mensagem = "Motorista não reconhecido. Cliente Avulso!"
    
    clientes_permitidos = simular_reconhecimento_facial(foto_cliente_simulacao)    

    try:
        foto_clientes_permitidos = face_recognition.load_image_file(clientes_permitidos["foto"])
        encoding_foto_cliente_permitido = face_recognition.face_encodings(foto_clientes_permitidos)[0]
    except:
        motorista = []
        
        return reconhecido, mensagem, motorista

    base_motorista = carregar_arquivos()
        
    for cliente in base_motorista["clientes"]:
    
        for fotos_cliente in cliente["fotos"]:
    
            foto_banco = face_recognition.load_image_file(fotos_cliente)
            encoding_foto_banco = face_recognition.face_encodings(foto_banco)
            if len(encoding_foto_banco) > 0:
                biden_encoding = encoding_foto_banco[0]
                foto_reconhecida = face_recognition.compare_faces([encoding_foto_cliente_permitido], biden_encoding)[0]
            
            if foto_reconhecida:
                    total_reconhecimentos += 1
    
        if total_reconhecimentos/len(cliente["fotos"]) > 0.7:
            reconhecido = True
            mensagem    = "Um motorista foi reconhecido, verificando dados cadastrados..."
            motorista = cliente
            break
    
    return reconhecido, mensagem, motorista

def reservar_vaga(reconhecido, mensagem, motorista):
    resposta = False
    print("Verificando se o motorista é um cliente mensal")
    reconhecido, mensagem, motorista        
    if reconhecido:
        print(mensagem)
        if motorista["eh_mensalista"] == True:
            resposta = indicar_vaga(motorista)
        else:
            resposta = oferecer_plano(motorista)
    else:
        print(mensagem)   
                 
    return resposta

def oferecer_plano(motorista):
    print(motorista["nome"], " foi reconhecido, mas não é assinante mensal")
    print(motorista["status"], ". Assine nosso plano por apenas 200 reais.")
    return True

def indicar_vaga(motorista):
    print("Seja Bem vindo ", motorista["nome"], "a sua vaga esta reservada.")
    print("Voce pode estacionar nas vagas ", motorista["vagas"])
    return True