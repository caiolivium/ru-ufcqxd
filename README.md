# Agendador de Refeições UFC Quixada - Restaurante Universitário (SIGAA)

Este projeto automatiza o processo de agendamento de refeições no Restaurante Universitário da Universidade Federal do Ceará (UFC) por meio do sistema SIGAA, utilizando o Selenium WebDriver em conjunto com Python. O bot realiza login no sistema, navega pelas páginas, e agenda refeições (almoço e jantar) para as próximas datas úteis, de acordo com as preferências definidas.

## Funcionalidades

- **Login automático**: O bot faz login no sistema SIGAA utilizando credenciais predefinidas (usuário e senha).
- **Agendamento de refeições**: Para cada conta fornecida, o bot agenda refeições para os próximos 5 dias úteis, permitindo a seleção entre almoço e jantar, além dos horários disponíveis.
- **Controle de datas**: O bot calcula automaticamente as próximas datas úteis (segunda a sexta-feira), ignorando os finais de semana.
- **Suporte a múltiplas contas**: O script pode ser configurado para trabalhar com várias contas de uma vez, realizando o agendamento de forma simultânea.

## Pré-requisitos

Antes de rodar o projeto, você precisará ter os seguintes requisitos instalados:

- **Python 3.x**: O código foi desenvolvido para rodar com Python 3.x.
- **Selenium**: Biblioteca para automação do navegador.
- **Chromedriver**: O Selenium utiliza o Chromedriver para interagir com o navegador Chrome. O [Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br) deve ser instalado na versão correspondente ao seu navegador.
- **Asyncio**: Biblioteca para execução assíncrona. É uma biblioteca padrão do Python 3.7+.

## Como rodar o projeto

1. Clone o repositório ou baixe os arquivos.
2. Instale as dependências (se ainda não tiver o Selenium):
   ```bash
   pip install selenium
3. Baixe o Chromedriver e coloque-o no diretório especificado no código (ou altere o caminho no código conforme necessário).
4. Abra o arquivo bot.py e defina as credenciais das contas que deseja usar no agendamento, conforme o formato:
    ```py
    contas = [
    {'usuario': 'usuario1', 'senha': 'senha1'},
    {'usuario': 'usuario2', 'senha': 'senha2'},
    {'usuario': 'usuario3', 'senha': 'senha3'},
    ]
5. Execute o script:
    ```bash
    python bot.py
6. O bot irá realizar o login e agendar as refeições nas próximas datas úteis.