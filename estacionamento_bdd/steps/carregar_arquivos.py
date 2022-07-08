from behave import given, when, then
from estacionamento import *

@given("carregar os arquivos de configuracao do sistema")
def given_carregar_arquivo_configuracao(context):
    context.configuracao = carregar_arquivos()    
    assert context.configuracao != None
