Feature: verificando se o motorista é um cliente mensal

Scenario: indicar localizacao da vaga ao motorista mensal
    Given verificar status do pagamento
    When a foto ./fotos/ayrton1.jpeg do cliente for identificada
    Then o cliente ./fotos/ayrton1.jpeg deve ser reconhecido
    When verificar status do ./fotos/ayrton1.jpeg
    Then verificar se o motorista é um cliente mensal


Scenario: indicar localizacao da vaga ao motorista mensal
    Given verificar status do pagamento
    When a foto ./fotos/zeca1.jpeg do cliente for identificada
    Then o cliente ./fotos/zeca1.jpeg deve ser reconhecido
    When verificar status do ./fotos/zeca1.jpeg
    Then verificar se o motorista não é um cliente mensal

