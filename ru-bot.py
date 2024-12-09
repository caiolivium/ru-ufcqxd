import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

# Lista de contas
contas = [
    {'usuario': 'usuario1', 'senha': 'senha1'},
    {'usuario': 'usuario2', 'senha': 'senha2'},
    {'usuario': 'usuario3', 'senha': 'senha3'},
]

url = "https://si3.ufc.br/sigaa/verTelaLogin.do"

async def iniciarBot(usuario, senha, url):
    caminho = r"C:\\Users\\SeuUsuario\\localDoArquivo\\chromedriver.exe"
    
    # Inicializar o serviço do Chrome com o caminho do chromedriver
    service = Service(caminho)
    driver = webdriver.Chrome(service=service)
    
    try:
        # Abrir o site no Chrome
        driver.get(url)
        
        # Preencher o campo de nome de usuário e senha
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user.login"))).send_keys(usuario)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user.senha"))).send_keys(senha)
        
        # Clicar no botão de login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))).click()

        # Aguardar o botão "Continuar" aparecer e clicar nele, se disponível
        try:
            continuar_botao = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.NAME, "j_id_jsp_1809757351_1:j_id_jsp_1809757351_2"))
            )
            continuar_botao.click()
            print(f"Conta {usuario}: botão 'Continuar' clicado.")
        except Exception:
            print(f"Conta {usuario}: botão 'Continuar' não encontrado, prosseguindo.")
        
        # Aguardar o carregamento completo da página principal após clicar em "Continuar"
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/sigaa/verPortalDiscente.do']"))).click()
        
        # Localizar o item de menu "Restaurante Universitário"
        restaurante_universitario = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Restaurante Universitário']")))
        
        # Inicializar ActionChains
        actions = ActionChains(driver)
        
        # Passar o mouse sobre o item de menu "Restaurante Universitário"
        actions.move_to_element(restaurante_universitario).perform()
        
        # Esperar o submenu aparecer e localizar e clicar em "Agendar Refeição"
        agendar_refeicao = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='ThemeOfficeMenuItemText' and text()='Agendar Refeição']")))
        agendar_refeicao.click()
        
        # Obter as próximas 5 datas úteis
        datas = obter_proximas_datas(5)
        
        for data in datas:
            for j in range(2):  # 0 para Almoço e 1 para Jantar
                # Encontrar o campo de data pelo ID
                campo_data = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "formulario:data_agendamento")))
                campo_data.click()  # Garantir que o campo de data está ativo
                campo_data.clear()
                campo_data.send_keys(data)
            
                # Encontrar e clicar na opção de tipo de refeição
                tipo_refeicao = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "formulario:tipo_refeicao")))
                tipo_refeicao.click()
                if j == 0:
                    opcao_refeicao = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='formulario:tipo_refeicao']//option[text()='Almoço']")))
                    opcao_refeicao.click()
                else:
                    opcao_refeicao = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='formulario:tipo_refeicao']//option[text()='Jantar']")))
                    opcao_refeicao.click()
            
                # Encontrar e clicar no campo de horário agendado
                horario_agendado = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "formulario:horario_agendado")))
                horario_agendado.click()

                # Alternar entre "11:00 - 14:00" e "17:00 - 18:45"
                if j == 0:
                    opcao_horario = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='formulario:horario_agendado']//option[text()='11:00 - 14:00']")))
                    opcao_horario.click()
                else:
                    opcao_horario = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='formulario:horario_agendado']//option[text()='17:00 - 18:45']")))
                    opcao_horario.click()
            
                # Clicar no botão de cadastro de agendamento
                botao_cadastrar = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "formulario:cadastrar_agendamento_bt")))
                botao_cadastrar.click()
                
                print(f"Conta: {usuario} - Refeição '{'Almoço' if j == 0 else 'Jantar'}' para o horário '{'11:00 - 14:00' if j == 0 else '17:00 - 18:45'}' selecionada e agendamento realizado para a data {data}.")
                
                # Pausa para garantir que o agendamento foi registrado
                time.sleep(2)
        
    except Exception as e:
        print(f"Erro na conta {usuario}: {str(e)}")
    
    finally:
        driver.quit()

def obter_proximas_datas(n=5):
    datas = []
    hoje = datetime.date.today()
    while len(datas) < n:
        hoje += datetime.timedelta(days=1)
        # Verificar se é um dia útil
        if hoje.weekday() < 5:  # 0=Segunda, ..., 4=Sexta
            datas.append(hoje.strftime("%d%m%Y"))
    return datas

async def executar_para_todas_as_contas():
    for conta in contas:
        await iniciarBot(conta['usuario'], conta['senha'], url)

asyncio.run(executar_para_todas_as_contas())