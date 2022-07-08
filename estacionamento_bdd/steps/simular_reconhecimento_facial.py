from behave import given, when, then
from estacionamento import *

@given("simular um cliente acessando o estacionamento")
def given_carregar_arquivo_configuracao(context):
    context.configuracao = carregar_arquivos()    
    assert context.configuracao != None

@when("o cliente {foto} foi identificado")
def when_simular_reconhecimento_facial(context, foto):
    context.foto_escolhida = simular_reconhecimento_facial(foto)
    
    assert context.foto_escolhida != None