from behave import given, when, then
from estacionamento import *

@given("verificar status do pagamento")
def given_carregar_arquivo_configuracao(context):
    context.configuracao = carregar_arquivos()    
    assert context.configuracao != None

@when("a foto {foto} do cliente for identificada")
def when_simular_reconhecimento_facial(context, foto):
    context.foto_selecionada = simular_reconhecimento_facial(foto)
    
    assert context.foto_selecionada != None

@then("o cliente {foto_cliente_simulação} deve ser reconhecido")
def then_cliente_reconhecido(context, foto_cliente_simulação):
    context.reconhecido, context.mensagem, context.motorista = reconhecer_cliente(foto_cliente_simulação)
    
    assert context.reconhecido == True

@when("verificar status do {motorista_identificado}")
def when_verificar_status_cliente(context, motorista_identificado):
    context.reconhecido, context.mensagem, context.motorista = reconhecer_cliente(motorista_identificado)
    
    assert context.motorista['status'] != None

@then("verificar se o motorista é um cliente mensal")
def then_indicar_vaga(context):
    context.autorizado = reservar_vaga(context.reconhecido, context.mensagem, context.motorista)
    
    assert context.autorizado == True

@then("verificar se o motorista não é um cliente mensal")
def then_oferecer_plano(context):
    context.negado = reservar_vaga(context.reconhecido, context.mensagem, context.motorista)
    
    assert context.negado == True
    
