Feature: Verificando se o motorista é um cliente mensal

Scenario: simular reconhecimento facial de um cliente
    Given simular um cliente acessando o estacionamento
    When o cliente ./fotos/ayrton1.jpeg foi identificado