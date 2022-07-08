Feature: Verificando se o motorista é um cliente mensal

Scenario: Um cliente chega no estacionamento e deve ser reconhecido pela foto
    Given reconhecer cliente
    When a foto ./fotos/ayrton1.jpeg for carregada
    Then o cliente ./fotos/ayrton1.jpeg deve ser reconhecido para acessar a vaga reservada