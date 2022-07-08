from behave import given, when, then
from estacionamento import *

@given("reconhecer cliente")
def given_carregar_arquivo_configuracao(context):
    context.configuracao = carregar_arquivos()    
    assert context.configuracao != None

@when("a foto {foto} for carregada")
def when_simular_reconhecimento_facial(context, foto):
    context.foto_escolhida = simular_reconhecimento_facial(foto)
    assert context.foto_escolhida != None

@then("o cliente {foto_cliente_simulacao} deve ser reconhecido para acessar a vaga reservada")
def then_cliente_reconhecido(context, foto_cliente_simulacao):
    context.reconhecido, context.mensagem, context.motorista = reconhecer_cliente(foto_cliente_simulacao)
    assert context.reconhecido == True