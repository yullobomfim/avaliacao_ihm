import face_recognition
import secrets
import random
import simpy
import json

FOTOS_MOTORISTAS = [
                "./faces/ayrton1.jpeg",
                "./faces/ayrton2.jpeg",
                "./faces/ayrton3.jpeg",
                "./faces/roberto1.jpeg",
                "./faces/roberto2.jpeg",
                "./faces/roberto3.jpeg", 
                "./faces/zeca1.jpeg",
                "./faces/zeca2.jpeg",
                "./faces/zeca3.jpeg",                
                "./faces/rubinho1.jpeg",
                "./faces/rubinho2.jpeg",
                "./faces/rubinho3.jpeg"                
]
ARQUIVO_CONFIGURACAO = "./configuracao.json"

PROBABILIDADE_A1 = 1
PROBABILIDADE_A2 = 6
PROBABILIDADE_A3 = 5
PROBABILIDADE_B1 = 3
PROBABILIDADE_B2 = 5
PROBABILIDADE_B3 = 1

PROBABILIDADE_DE_SER_AUTORIZADO = 30
PROBABILIDADE_DE_SER_LIBERADO = 100 - PROBABILIDADE_DE_SER_AUTORIZADO
PROBABILIDADE_NECESSIDADE_DE_VAGA = 5
PROBABILIDADE_DE_LIBERACAO_DA_VAGA = 30

CAPACIDADE_MAXIMA_ESTACIONAMENTO = 10

TEMPO_ENTRE_CLIENTES = 20
TEMPO_RECONHECIMENTO_AUTORIZACAO = 20
TEMPO_VERIFICACAO_DISPONIBILIDADE_VAGAS = 20
TEMPO_LIBERACAO_CLIENTE = 20
TEMPO_LIBERACAO_VAGAS = 20

def carregar():
    global configuracao
    
    configuracao = None
    with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)
        if configuracao:
            print("----------------ESTACIONAMENTO DIGITAL INTELIGENTE------------------------")
            print("Arquivos de configuração carregados...")
            print("Iniciando o simulador de eventos...")

    global clientes_reconhecidos
    clientes_reconhecidos = {}

    global clientes_mensalistas
    clientes_mensalistas = {}

    global clientes_em_vagas_reservadas 
    clientes_em_vagas_reservadas = {}

    global total_vagas
    total_vagas = {
        "A1": (random.randint(1, 10) <= PROBABILIDADE_A1),
        "A2": (random.randint(1, 10) <= PROBABILIDADE_A2),
        "A3": (random.randint(1, 10) <= PROBABILIDADE_A3),
        "B1": (random.randint(1, 10) <= PROBABILIDADE_B1),
        "B2": (random.randint(1, 10) <= PROBABILIDADE_B2),
        "B3": (random.randint(1, 10) <= PROBABILIDADE_B3)
    }

def simular_estacionamento():
    motorista = {
        "foto": random.choice(FOTOS_MOTORISTAS),
        "cliente": None

    }

    return motorista

def reconhecer_cliente(motorista):
    global configuracao

    print("Realizando o reconhecimento facial dos motoristas...")
    
    foto_motorista = face_recognition.load_image_file(motorista["foto"])
    encoding_foto_motorista = face_recognition.face_encodings(foto_motorista)[0]
    reconhecido = False
    
    for cliente in configuracao["clientes"]:
        fotos_banco = cliente["fotos"]
        total_reconhecimentos = 0

        for foto in fotos_banco:
            foto_banco = face_recognition.load_image_file(foto)
            encoding_foto_banco = face_recognition.face_encodings(foto_banco)[0]

            foto_reconhecida = face_recognition.compare_faces([encoding_foto_motorista], encoding_foto_banco)[0]
            if foto_reconhecida:
                total_reconhecimentos += 1

        if total_reconhecimentos/len(fotos_banco) > 0.7:
            reconhecido = True

            motorista["cliente"] = {}
            motorista["cliente"]["nome"] = cliente["nome"]
            motorista["cliente"]["status"] = cliente["status"]
            motorista["cliente"]["vagas"] = random.choice(["A1", "A2", "A3", "B1", "B2", "B3"])
            motorista["cliente"]["mensalista"] = cliente["mensalista"]

    return reconhecido, motorista

def imprimir_cliente(cliente):
    print("Nome:", cliente["cliente"]["nome"])
    print("Vaga:", cliente["cliente"]["vagas"])
    print("Status:", cliente["cliente"]["status"])
    print("**************************************************************************")

def reconhecer_motorista(env):
    global clientes_reconhecidos

    while True:
        print("Verificando se o motorista é um cliente mensalista:", env.now)
        motorista = simular_estacionamento()
        reconhecido, cliente = reconhecer_cliente(motorista)
        if reconhecido:
            id_atendimento = secrets.token_hex(nbytes=16).upper()
            clientes_reconhecidos[id_atendimento] = cliente
            print("Motorista reconhecido, verificando os dados do Cliente ...")
            imprimir_cliente(cliente)
        else:
            print("Motorista não reconhecido. Assine nossos planos e seja um cliente mensalista")

        yield env.timeout(TEMPO_ENTRE_CLIENTES)

def identificar_autorizacao(env):
    global clientes_reconhecidos
    global clientes_mensalistas

    while True:
        if len(clientes_reconhecidos):
            print("verificando autorizacao de acesso", env.now)
            total_clientes_mensalistas = 0
            for id_atendimento, cliente in list(clientes_reconhecidos.items()):
                autorizacao_reconhecida = cliente["cliente"]["mensalista"]
                if autorizacao_reconhecida:
                    cliente["mensalista"] = False
                    clientes_mensalistas[id_atendimento] = cliente
                    clientes_reconhecidos.pop(id_atendimento)
                    print("O cliente", cliente["cliente"]["nome"], "está autorizado a estacionar na vaga")
                    total_clientes_mensalistas += 1

            timeout = 1
            if total_clientes_mensalistas > 0:
                timeout = total_clientes_mensalistas * TEMPO_RECONHECIMENTO_AUTORIZACAO

            yield env.timeout(timeout)
        else:
            yield env.timeout(1)

def verificar_vaga(env):
    global clientes_reconhecidos

    while True:
        if len(clientes_reconhecidos):
            print("verificando Localização de vagas para os clientes ...", env.now)
            total_liberacoes = 0
            for id_atendimento, cliente in list(clientes_reconhecidos.items()):
                cliente_liberado = (random.randint(1, 10) <= PROBABILIDADE_DE_SER_LIBERADO)
                if cliente_liberado:
                    print("O cliente", cliente["cliente"]["nome"], "está verificando a vaga ", cliente["cliente"]["vagas"])
                    clientes_reconhecidos.pop(id_atendimento)

                    total_liberacoes += 1

            timeout = 1
            if total_liberacoes > 0:
                timeout = total_liberacoes * TEMPO_LIBERACAO_CLIENTE

            yield env.timeout(timeout)
        else:
            yield env.timeout(1)

def disponibilizar_vagas(env):
    global clientes_mensalistas
    global total_vagas

    while True:
        if len(clientes_mensalistas):
            print("Identificar o local da vaga reservada para os mensalistas ", env.now)
            
            total_verificacoes_vagas = 0
            for cliente in clientes_mensalistas.values():
                if not cliente["mensalista"]:
                    tipo_vagas = cliente["cliente"]["vagas"]
                    tem_vagas = total_vagas[tipo_vagas]
                    if tem_vagas:
                        print("O cliente", cliente["cliente"]["nome"], "deve dirigir até a vaga", tipo_vagas )
                    else:
                        print("Atenção", cliente["cliente"]["nome"], "não temos vagas", tipo_vagas )

                    cliente["mensalista"] = True
                    total_verificacoes_vagas += 1

            timeout = 1
            if total_verificacoes_vagas > 0:
                timeout = total_verificacoes_vagas * TEMPO_VERIFICACAO_DISPONIBILIDADE_VAGAS

            yield env.timeout(timeout)
        else:
            yield env.timeout(1)

def reservar_vaga(env):
    global clientes_mensalistas
    global clientes_em_vagas_reservadas

    while True:
        if len(clientes_mensalistas):
            print("Verificando Vagas para o cliente ", env.now)

            if len(clientes_em_vagas_reservadas) == CAPACIDADE_MAXIMA_ESTACIONAMENTO:
                print("Não há vagas")

                yield env.timeout(1)
            else:
                total_clientes_em_vagas_reservadas = 0
                for id_atendimento, cliente in list(clientes_mensalistas.items()):
                    necessita_vagas = (random.randint(1, 10) <= PROBABILIDADE_NECESSIDADE_DE_VAGA)
                    if necessita_vagas:
                        clientes_em_vagas_reservadas[id_atendimento] = cliente
                        clientes_mensalistas.pop(id_atendimento)

                        print("cliente", cliente["cliente"]["nome"], " é mensalista e precisa de uma vaga")

                        total_clientes_em_vagas_reservadas += 1

                timeout = 1
                if total_clientes_em_vagas_reservadas > 0:
                    timeout = total_clientes_em_vagas_reservadas * TEMPO_RECONHECIMENTO_AUTORIZACAO

                yield env.timeout(timeout)
        else:
            yield env.timeout(1)

def liberar_vaga(env):
    global clientes_em_vagas_reservadas

    while True:
        if len(clientes_em_vagas_reservadas):
            print("verificando liberacao de Vagas", env.now)

            total_liberacoes_vagas = 0
            for id_atendimento, cliente in list(clientes_em_vagas_reservadas.items()):
                liberar_vaga = (random.randint(1, 10) <= PROBABILIDADE_DE_LIBERACAO_DA_VAGA)

                if liberar_vaga:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print("O cliente", cliente["cliente"]["nome"], " está saindo e liberando uma Vaga")
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    clientes_em_vagas_reservadas.pop(id_atendimento)
                    total_liberacoes_vagas += 1

            timeout = 1
            if total_liberacoes_vagas > 0:
                timeout = total_liberacoes_vagas * TEMPO_LIBERACAO_VAGAS 
            yield env.timeout(timeout)
        else:
            yield env.timeout(1)

if __name__ == "__main__":
    carregar()

    env = simpy.Environment()
    env.process(reconhecer_motorista(env))
    env.process(identificar_autorizacao(env))
    env.process(verificar_vaga(env))
    env.process(disponibilizar_vagas(env))
    env.process(reservar_vaga(env))
    env.process(liberar_vaga(env))
    env.run(until=10000)
