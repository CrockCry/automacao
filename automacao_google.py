from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import Select 
import time

# --- Função para coletar dados do usuário ---
def coletar_dados_do_usuario():
    dados = {}
    
    print("\n--- Digite os dados para o cadastro da Inscrição Principal ---")
    dados['nucleo_selecionado'] = input("Núcleo (Ex: CDA - Cultura Digital para Adultos e Idosos): ")
    dados['nome_completo'] = input("Nome Completo: ")
    dados['data_nascimento'] = input("Data de Nascimento (dd/mm/aaaa): ")
    dados['genero'] = input("Gênero (Masculino/Feminino): ")
    
    tem_responsavel_geral = input("A inscrição terá pelo menos um responsável? (sim/nao): ").lower() #
    dados['tem_responsavel_geral'] = 'sim' if tem_responsavel_geral == 'sim' else 'nao' #

    dados['cpf'] = input("CPF (apenas números): ")
    dados['rg'] = input("RG (opcional): ")
    dados['cep'] = input("CEP (apenas números): ")
    dados['numero_endereco'] = input("Número do Endereço (opcional): ")
    dados['complemento_endereco'] = input("Complemento do Endereço (opcional): ")
    
    dados['responsaveis'] = []

    if dados['tem_responsavel_geral'] == 'sim': #
        continuar_adicionando_responsavel = 'sim' #
        responsavel_num = 1 #
        while continuar_adicionando_responsavel == 'sim': #
            print(f"\n--- Digite os dados para o Responsável {responsavel_num} ---") #
            responsavel_dados = {} #
            responsavel_dados['nome_responsavel'] = input("Nome Completo do Responsável: ") #
            responsavel_dados['tipo_responsavel'] = input("Tipo de Responsável (Ex: Pai, Mãe, Outro): ") #
            responsavel_dados['empregado_responsavel'] = input("Responsável Empregado? (sim/nao): ") #
            responsavel_dados['cpf_responsavel'] = input("CPF do Responsável (apenas números): ") #
            responsavel_dados['rg_responsavel'] = input("RG do Responsável (opcional): ") #
            
            # Os dados de CEP, Número e Complemento do Responsável serão reciclados da inscrição principal,
            # mas podemos perguntar se são os mesmos ou se são diferentes para cada responsável
            # Por simplicidade, vamos manter reciclando do principal por enquanto,
            # mas saiba que pode ser adaptado para serem diferentes.
            responsavel_dados['cep_responsavel'] = dados['cep'] #
            responsavel_dados['numero_responsavel'] = dados['numero_endereco'] #
            responsavel_dados['complemento_responsavel'] = dados['complemento_endereco'] #
            
            dados['responsaveis'].append(responsavel_dados) # Adiciona o dicionário do responsável à lista

            continuar_adicionando_responsavel = input("Adicionar mais um responsável? (sim/nao): ").lower() #
            responsavel_num += 1 #
            
    return dados

# --- Inicialização do WebDriver ---
driver = webdriver.Chrome() 

# --- Abrir a página de login ---
print("Abrindo a página de login...")
driver.get("https://www.abasige.online/login")

# --- Preencher login e senha ---
print("Preenchendo credenciais...")
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys("admin")
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("euma581622")
password_field.send_keys(Keys.RETURN)

# --- Esperar o login carregar e o dashboard aparecer ---
print("Aguardando carregamento após o login...")
time.sleep(6) 

# --- Clicar no menu hambúrguer ---
try:
    print("Tentando clicar no menu hambúrguer...")
    menu_hamburguer = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".bx.bx-menu"))
    )
    menu_hamburguer.click()
    print("Menu hambúrguer clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no menu hambúrguer: {e}")
    driver.quit()
    exit()

# --- Aguardar o menu lateral abrir e clicar em "Inscrições/Matrícula" ---
print("Aguardando o menu lateral abrir...")
time.sleep(1) 
try:
    print("Tentando clicar em 'Inscrições/Matrícula'...")
    inscricoes_matricula_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Inscrições/Matrícula"))
    )
    inscricoes_matricula_link.click()
    print("Link 'Inscrições/Matrícula' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no link 'Inscrições/Matrícula': {e}")
    driver.quit()
    exit()

# --- Aguardar o sub-menu "Inscrição" aparecer e clicar nele ---
print("Aguardando o sub-menu de Inscrição/Matrícula aparecer...")
time.sleep(1) 
try:
    print("Tentando clicar no sub-item 'Inscrição'...")
    inscricao_sub_item_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Inscrição"))
    )
    inscricao_sub_item_link.click()
    print("Sub-item 'Inscrição' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no sub-item 'Inscrição': {e}")
    driver.quit()
    exit()

# --- Coletar os dados do usuário antes de iniciar a automação do formulário ---
dados_inscricao_atual = coletar_dados_do_usuario()

print(f"\n--- Iniciando o processo de inscrição para: {dados_inscricao_atual['nome_completo']} ---")

# --- Clicar no botão 'Nova +' para abrir um novo formulário ---
try:
    print("Tentando clicar em 'Nova +'...")
    nova_inscricao_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.btn-add"))
    )
    nova_inscricao_button.click()
    print("Botão 'Nova +' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar em Nova + para {dados_inscricao_atual['nome_completo']}: {e}")
    driver.quit()
    exit()
    
    
try:
    print("Tentando clicar em 'Adicionar Nova Pessoa'...")
    nova_inscricao_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "adicionar-pessoa"))
    )
    nova_inscricao_button.click()
    print("Botão 'Adicionar Nova Pessoa' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar em Adicionar Nova Pessoa para {dados_inscricao_atual['nome_completo']}: {e}")
    driver.quit()
    exit()
time.sleep(1) 

# --- Aguardar o formulário de Inscrição carregar ---
print("Aguardando o formulário de Inscrição carregar...")
time.sleep(1) 

# --- Selecionar o Núcleo ---
try:
    print(f"Abrindo dropdown de 'Núcleos' para {dados_inscricao_atual['nucleo_selecionado']}...")
    nucleos_dropdown_abrir = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-selection.select2-selection--multiple"))
    )
    nucleos_dropdown_abrir.click()
    print("Dropdown de 'Núcleos' aberto.")

    print("Aguardando as opções do dropdown'...")

    print(f"Selecionando 'Núcleo': {dados_inscricao_atual['nucleo_selecionado']}")
    opcao_nucleo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{dados_inscricao_atual['nucleo_selecionado']}')]"))
        )
    opcao_nucleo.click()
    print("Núcleo selecionado com sucesso!")
except Exception as e:
        print(f"Não foi possível selecionar o Núcleo para {dados_inscricao_atual['nome_completo']}: {e}")
         
    
time.sleep(1)
    
# --- Clicar na aba 'Cadastro' ---
try:
    print("Tentando clicar na aba 'Cadastro'...")
    tab_cadastro = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Cadastro"))
    )
    tab_cadastro.click()
    print("Aba 'Cadastro' clicada com sucesso!")
    time.sleep(1) 
except Exception as e:
    print(f"Não foi possível clicar na aba 'Cadastro': {e}")
    driver.quit()
    exit() 

# --- Preencher os campos da aba 'Cadastro' ---
try:
    # Nome
    print(f"Preenchendo Nome: {dados_inscricao_atual['nome_completo']}")
    campo_nome = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "nome"))
    )
    campo_nome.send_keys(dados_inscricao_atual['nome_completo'])
    campo_nome.send_keys(Keys.TAB) 
    time.sleep(0.5) 

    # Nascimento 
    if dados_inscricao_atual['data_nascimento']:
        print(f"Preenchendo Nascimento: {dados_inscricao_atual['data_nascimento']}")
        campo_nascimento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "nascimento"))
        )
        campo_nascimento.send_keys(dados_inscricao_atual['data_nascimento'])
        campo_nascimento.send_keys(Keys.TAB) 
        time.sleep(0.5) 

    # Gênero
    print(f"Selecionando Gênero: {dados_inscricao_atual['genero']}")
    genero_dropdown_abrir = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "select2-selection__arrow"))
        )
    genero_dropdown_abrir.click()

    opcao_genero = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{dados_inscricao_atual['genero']}')]"))
        )
    opcao_genero.click()
    time.sleep(0.5)

    # Responsável (Radio Button)
    if dados_inscricao_atual['tem_responsavel_geral'].lower() == 'sim':
        print("Clicando em 'Tem Responsável: Sim'")
        radio_responsavel_sim = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "flexRadioDefault1")) 
        )
        radio_responsavel_sim.click()
        time.sleep(0.5)
    
    # CPF (Preenchendo com JavaScript para evitar problemas de máscara)
    print(f"Preenchendo CPF com JavaScript: {dados_inscricao_atual['cpf']}")
    campo_cpf = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.NAME, "cpf"))
    )
    campo_cpf.clear() 
    driver.execute_script(f"arguments[0].value = '{dados_inscricao_atual['cpf']}';", campo_cpf)
    driver.execute_script("arguments[0].blur();", campo_cpf) 
    time.sleep(0.5) 

    # --- TRATAMENTO DO ALERT DE CPF INVÁLIDO ---
    try:
        print("Verificando se há um alerta de CPF inválido...")
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alerta de CPF inválido detectado: {alert.text}")
        alert.accept() 
        print("Alerta aceito. Prosseguindo...")
        
    except TimeoutException: 
        print("Nenhum alerta de CPF inválido apareceu.")
    except NoAlertPresentException:
        print("Nenhum alerta de CPF inválido apareceu.")
    
    # RG (Opcional)
    if dados_inscricao_atual['rg']: 
        print(f"Preenchendo RG: {dados_inscricao_atual['rg']}")
        campo_rg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "rg"))
        )
        campo_rg.send_keys(dados_inscricao_atual['rg'])
        campo_rg.send_keys(Keys.TAB) 
        time.sleep(0.5)

    # CEP
    print(f"Preenchendo CEP: {dados_inscricao_atual['cep']}")
    campo_cep = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "cep"))
    )
    campo_cep.clear()
    driver.execute_script(f"arguments[0].value = '{dados_inscricao_atual['cep']}';", campo_cep)
    driver.execute_script("arguments[0].blur();", campo_cep)
    campo_cep.send_keys(Keys.TAB) 
    time.sleep(2) 
    
        # --- TRATAMENTO DO ALERT DE CEP INVÁLIDO ---
    try:
        print("Verificando se há um alerta de CEP inválido...")
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Alerta de CEP inválido detectado: {alert.text}")
        alert.accept() 
        print("Alerta aceito. Prosseguindo...")
        
    except TimeoutException: 
        print("Nenhum alerta de CEP inválido apareceu.")
    except NoAlertPresentException:
        print("Nenhum alerta de CEP inválido apareceu.")

    # Número (Opcional)
    if dados_inscricao_atual['numero_endereco']:
        print(f"Preenchendo Número: {dados_inscricao_atual['numero_endereco']}")
        campo_numero = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "numero"))
        )
        campo_numero.send_keys(dados_inscricao_atual['numero_endereco'])
        campo_numero.send_keys(Keys.TAB) 
        time.sleep(0.5)
    
    # Complemento (Opcional)
    if dados_inscricao_atual['complemento_endereco']:
        print(f"Preenchendo Complemento: {dados_inscricao_atual['complemento_endereco']}")
        campo_complemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "complemento"))
        )
        campo_complemento.send_keys(dados_inscricao_atual['complemento_endereco'])
        campo_complemento.send_keys(Keys.TAB) 
        time.sleep(0.5)

    # --- Clicar no botão 'Salvar' da inscrição principal ---
    print("Tentando clicar no botão 'Salvar' da inscrição principal...")
    botao_salvar_inscricao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Salvar')]"))
    )
    botao_salvar_inscricao.click()
    print("Botão 'Salvar' da inscrição principal clicado com sucesso!")
    
    time.sleep(3) 

except Exception as e:
    print(f"Erro ao preencher campos ou salvar para {dados_inscricao_atual['nome_completo']}: {e}")
    driver.quit()
    exit()

# --- Seção para adicionar Responsável (apenas se 'tem_responsavel' for 'sim') ---
if dados_inscricao_atual['tem_responsavel_geral'].lower() == 'sim':
    try:
        print("Tentando clicar na aba 'Responsável'...")
        tab_responsavel = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Responsável")) 
        )
        tab_responsavel.click()
        print("Aba 'Responsável' clicada com sucesso!")
        time.sleep(2) 

        main_window_handle = driver.current_window_handle
        print(f"Handle da janela principal: {main_window_handle}")
        
         # --- Loop para adicionar múltiplos responsáveis ---
        for responsavel_atual in dados_inscricao_atual['responsaveis']:
            print(f"\n--- Adicionando Responsável: {responsavel_atual['nome_responsavel']} ---")

        # --- Clicar no botão '+ Novo' para adicionar Responsável ---
        print("Tentando clicar no botão '+ Novo' da aba Responsável...")
        add_responsavel_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '+ Novo')]")) 
        )
        add_responsavel_button.click()
        print("Botão '+ Novo' da aba Responsável clicado com sucesso!")
        time.sleep(3) 

        # --- Mudar o foco para a nova aba/janela ---
        new_window_handle = None
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)) 
        
        for window_handle in driver.window_handles:
            if window_handle != main_window_handle:
                new_window_handle = window_handle
                break
        
        if new_window_handle:
            driver.switch_to.window(new_window_handle)
            print(f"Foco mudado para a nova janela (Handle: {new_window_handle})")
            print(f"URL da nova janela: {driver.current_url}") 

            # --- PREENCHER OS CAMPOS DO RESPONSÁVEL AQUI (AJUSTADO COM OS NAMES CORRETOS) ---
            print(f"Preenchendo formulário do responsável para {responsavel_atual['nome_responsavel']}...")
            
            # 1. Campo Nome do Responsável (By.NAME, "nome_responsavel")
            campo_nome_responsavel = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "nome_responsavel")) 
            )
            campo_nome_responsavel.send_keys(responsavel_atual['nome_responsavel'])
            campo_nome_responsavel.send_keys(Keys.TAB)
            time.sleep(0.5)

            # 2. Dropdown Tipo de Responsável (By.NAME, "tipo_responsavel")
            if 'tipo_responsavel' in responsavel_atual and responsavel_atual['tipo_responsavel']:
                print(f"Selecionando Tipo de Responsável: {responsavel_atual['tipo_responsavel']}")
                try:
                    select_tipo_responsavel_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "tipo_responsavel")) 
                    )
                    select_tipo_responsavel = Select(select_tipo_responsavel_element)
                    select_tipo_responsavel.select_by_visible_text(responsavel_atual['tipo_responsavel'])
                    print(f"Tipo de Responsável '{responsavel_atual['tipo_responsavel']}' selecionado.")
                    time.sleep(0.5)
                except Exception as ex_dropdown:
                    print(f"Erro ao selecionar Tipo de Responsável: {ex_dropdown}")
                    print("Por favor, verifique se o texto exato está correto no input e na página ('Pai', 'Mãe', 'Outro').")
                    
            # 3. Dropdown "Empregado?" (By.NAME, "empregado_responsavel")
            if 'empregado_responsavel' in responsavel_atual:
                print(f"Selecionando 'Empregado?': {responsavel_atual['empregado_responsavel']}")
                try:
                    select_empregado_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "empregado_responsavel")) 
                    )
                    select_empregado = Select(select_empregado_element)
                    if responsavel_atual['empregado_responsavel'].lower() == 'sim':
                        select_empregado.select_by_value("1") 
                    elif responsavel_atual['empregado_responsavel'].lower() == 'nao':
                        select_empregado.select_by_value("0") 
                    print(f"'Empregado?' '{responsavel_atual['empregado_responsavel']}' selecionado.")
                    time.sleep(0.5)
                except Exception as ex_dropdown:
                    print(f"Erro ao selecionar 'Empregado?': {ex_dropdown}")
                    print("Por favor, verifique o 'name' correto e os 'value's para o dropdown 'Empregado?'.")

            # 4. CPF do Responsável (usar JavaScript) - name="cpf_responsavel"
            if 'cpf_responsavel' in responsavel_atual and responsavel_atual['cpf_responsavel']:
                print(f"Preenchendo CPF do Responsável com JavaScript: {responsavel_atual['cpf_responsavel']}")
                campo_cpf_responsavel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "cpf_responsavel"))
                )
                campo_cpf_responsavel.clear()
                driver.execute_script(f"arguments[0].value = '{responsavel_atual['cpf_responsavel']}';", campo_cpf_responsavel)
                driver.execute_script("arguments[0].blur();", campo_cpf_responsavel)
            time.sleep(0.5)
            

            # 5. RG do Responsável (Opcional) - name="rg_responsavel"
            if responsavel_atual['rg_responsavel']: 
                print(f"Preenchendo RG do Responsável: {responsavel_atual['rg_responsavel']}")
                campo_rg_responsavel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "rg_responsavel")) 
                )
                campo_rg_responsavel.send_keys(responsavel_atual['rg_responsavel'])
                campo_rg_responsavel.send_keys(Keys.TAB)
                time.sleep(0.5)

            # --- PREENCHENDO ENDEREÇO DO RESPONSÁVEL COM DADOS DA INSCRIÇÃO PRINCIPAL ---
            # 6. CEP do Responsável - name="endereco_cep_responsavel"
            if responsavel_atual['cep_responsavel']: 
                print(f"Preenchendo CEP do Responsável (reciclado do principal): {responsavel_atual['cep_responsavel']}")
                campo_cep_responsavel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "endereco_cep_responsavel")) 
                )
                driver.execute_script(f"arguments[0].value = '{responsavel_atual['cep_responsavel']}';", campo_cep_responsavel)
                driver.execute_script("arguments[0].blur();", campo_cep_responsavel)
                time.sleep(3) 

            # 7. Número do Endereço do Responsável (Opcional) - name="endereco_numero_responsavel"
            if responsavel_atual['numero_responsavel']:
                print(f"Preenchendo Número do Responsável (reciclado do principal): {responsavel_atual['numero_responsavel']}")
                campo_numero_responsavel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "endereco_numero_responsavel")) 
                )
                campo_numero_responsavel.send_keys(responsavel_atual['numero_responsavel'])
                campo_numero_responsavel.send_keys(Keys.TAB) 
                time.sleep(0.5)
            
            # 8. Complemento do Endereço do Responsável (Opcional) - name="endereco_complemento_responsavel"
            if responsavel_atual['complemento_responsavel']:
                print(f"Preenchendo Complemento do Responsável (reciclado do principal): {responsavel_atual['complemento_responsavel']}")
                campo_complemento_responsavel = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "endereco_complemento_responsavel")) 
                )
                campo_complemento_responsavel.send_keys(responsavel_atual['complemento_responsavel'])
                campo_complemento_responsavel.send_keys(Keys.TAB) 
                time.sleep(0.5)

            # --- Clicar no botão 'Salvar' do formulário do Responsável ---
            print("Tentando clicar no botão 'Salvar' do formulário do Responsável...")
            botao_salvar_responsavel = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Salvar')]"))
            )
            botao_salvar_responsavel.click()
            print("Botão 'Salvar' do Responsável clicado com sucesso!")
            time.sleep(3) 

            try:
                if driver.current_window_handle == new_window_handle:
                    driver.close() 
                    print("Nova janela/aba do responsável fechada.")
            except Exception as ex_close:
                print(f"Erro ao tentar fechar a aba do responsável (pode já ter fechado): {ex_close}")

        else:
            print("Erro: Não foi possível encontrar a nova janela/aba do responsável.")
            driver.quit()
            exit()

        driver.switch_to.window(main_window_handle)
        print("Foco retornado para a janela principal.")
        time.sleep(1) 

    except Exception as e:
        print(f"Erro ao navegar para aba Responsável ou adicionar/preencher/salvar novo: {e}")
        try:
            driver.switch_to.window(main_window_handle)
            print("Tentativa de retornar à janela principal após erro na aba do responsável.")
        except Exception as ex:
            print(f"Não foi possível retornar à janela principal: {ex}")
        driver.quit()
        exit()
else:
    print("Inscrição sem responsável, pulando a seção de Responsáveis.")


print(f"\n--- Processo de inscrição para {dados_inscricao_atual['nome_completo']} concluído! ---")
time.sleep(5) 
print("Fechando o navegador.")
driver.quit()
print("Automação concluída!")