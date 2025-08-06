from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
import time


# --- Função para coletar dados do usuário ---
def coletar_dados_do_usuario():
    dados = {}
    
    print("\n--- Digite os dados para o cadastro da Inscrição Principal ---")
    dados['nucleo_selecionado'] = input("Núcleo (Ex: CDA - Cultura Digital para Adultos e Idosos): ")
    dados['nome_completo'] = input("Nome Completo: ")
    dados['data_nascimento'] = input("Data de Nascimento (dd/mm/aaaa): ")
    dados['genero'] = input("Gênero (Masculino/Feminino): ")
    
    tem_responsavel = input("Tem Responsável? (sim/nao): ").lower()
    dados['tem_responsavel'] = 'sim' if tem_responsavel == 'sim' else 'nao'

    dados['cpf'] = input("CPF (apenas números): ")
    dados['rg'] = input("RG (opcional): ")
    dados['cep'] = input("CEP (apenas números): ")
    dados['numero_endereco'] = input("Número do Endereço (opcional): ")
    dados['complemento_endereco'] = input("Complemento do Endereço (opcional): ")

    if dados['tem_responsavel'] == 'sim':
        print("\n--- Digite os dados para o Responsável ---")
        dados['nome_responsavel'] = input("Nome Completo do Responsável: ")
        dados['cpf_responsavel'] = input("CPF do Responsável (apenas números): ")
        dados['rg_responsavel'] = input("RG do Responsável (opcional): ")
        dados['cep_responsavel'] = input("CEP do Responsável (apenas números): ")
        dados['numero_responsavel'] = input("Número do Endereço do Responsável (opcional): ")
        dados['complemento_responsavel'] = input("Complemento do Endereço do Responsável (opcional): ")
        # Adicione outros campos do responsável conforme necessário, ex:
        # dados['tipo_responsavel'] = input("Tipo de Responsável (Ex: Pai, Mãe, Outro): ")
    else:
        # Garante que as chaves existam, mesmo que vazias, para evitar KeyError
        dados['nome_responsavel'] = ''
        dados['cpf_responsavel'] = ''
        dados['rg_responsavel'] = ''
        dados['cep_responsavel'] = ''
        dados['numero_responsavel'] = ''
        dados['complemento_responsavel'] = ''
        # dados['tipo_responsavel'] = '' # se for adicionar

    return dados


driver = webdriver.Chrome() 

# --- Abrir uma página web ---
print("Abrindo o Google...")
driver.get("https://www.abasige.online/login")

# --- login e senha ---
print("Preenchendo credenciais...")
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys("admin")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("euma581622")
password_field.send_keys(Keys.RETURN)
print("Aguardando carregamento após o login...")
time.sleep(6)

# --- menu  ---
try:
    print("Tentando clicar no menu hambúrguer...")
    menu_hamburguer = driver.find_element(By.CSS_SELECTOR, ".bx.bx-menu")
    menu_hamburguer.click()
    print("Menu hambúrguer clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no menu hambúrguer: {e}")
   

print("Aguardando o menu lateral abrir...")
time.sleep(1)

# --- "Inscrições/Matrícula ---
try:
    print("Tentando clicar em 'Inscrições/Matrícula'...")
    inscricoes_matricula_link = driver.find_element(By.LINK_TEXT, "Inscrições/Matrícula")
    inscricoes_matricula_link.click()
    print("Link 'Inscrições/Matrícula' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no link 'Inscrições/Matrícula': {e}")

   

print("Aguardando o sub-menu de Inscrição/Matrícula aparecer...")
time.sleep(1)


try:
    print("Tentando clicar no sub-item 'Inscrição'...")
    inscricao_sub_item_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Inscrição")
    inscricao_sub_item_link.click()
    print("Sub-item 'Inscrição' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar no sub-item 'Inscrição': {e}")
    
    
time.sleep(2)

dados_inscricao_atual = coletar_dados_do_usuario()
print(f"\nAutomatizando inscrição para: {dados_inscricao_atual['nome_completo']}")

    
try:
    print("Tentando clicar em 'Nova +'...")
    nova_inscricao_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.btn-add"))
    )
    nova_inscricao_button.click()
    print("Botão 'Nova +' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar em Nova +: para {dados_inscricao_atual['nome_completo']}: {e}")
    driver.quit()
    exit()
    
time.sleep(2)
    
try:
    print("Tentando clicar em 'add nova inscricao'...")
    add_nova_inscricao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "adicionar-pessoa"))
    )
    add_nova_inscricao.click()
    print("Botão 'add nova iscricao' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar em add nova iscricao: {e}")
    driver.quit()
    exit()

time.sleep(2)
    
print("Aguardando o formulário de Inscrição carregar...")
time.sleep(2) 

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

try:
    print("Tentando clicar em 'cadastro'...")
    add_nova_inscricao = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Cadastro"))
    )
    add_nova_inscricao.click()
    print("Botão 'cadastro' clicado com sucesso!")
except Exception as e:
    print(f"Não foi possível clicar em cadastro: {e}")
    driver.quit()
    exit()

time.sleep(2)  
  
    # --- Preencher os campos da aba 'Cadastro' ---
try:
        # Nome
        print(f"Preenchendo Nome: {dados_inscricao_atual['nome_completo']}")
        campo_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "nome"))
        )
        campo_nome.send_keys(dados_inscricao_atual['nome_completo'])

        # Nascimento
        print(f"Preenchendo Nascimento: {dados_inscricao_atual['data_nascimento']}")
        campo_nascimento = driver.find_element(By.NAME, "nascimento") # Já deve estar presente se o nome foi encontrado
        campo_nascimento.send_keys(dados_inscricao_atual['data_nascimento'])
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
        if dados_inscricao_atual['tem_responsavel'].lower() == 'sim':
            print("Clicando em 'Tem Responsável: Sim'")
            radio_responsavel_sim = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "flexRadioDefault1"))
            )
            radio_responsavel_sim.click()
            time.sleep(0.5)

            # CPF
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
            
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"Alerta de CPF inválido detectado: {alert.text}")
            alert.accept()
            print("Alerta aceito. Prosseguindo...")
            
            # print("Limpando o campo CPF inválido...")
            # campo_cpf.clear()
            # time.sleep(2) 
            # alert.accept()
            # time.sleep(0.5) 
            
        except TimeoutException:
            print("Nenhum alerta de CPF inválido apareceu.")
        except NoAlertPresentException:
            print("Nenhum alerta de CPF inválido apareceu.")
        
        # RG (Opcional)
        if dados_inscricao_atual['rg']:
            print(f"Preenchendo RG: {dados_inscricao_atual['rg']}")
            campo_rg = driver.find_element(By.NAME, "rg")
            campo_rg.send_keys(dados_inscricao_atual['rg'])

        # CEP
        print(f"Preenchendo CEP: {dados_inscricao_atual['cep']}")
        campo_cep = driver.find_element(By.NAME, "cep")
        campo_cep.send_keys(dados_inscricao_atual['cep'])
        campo_cep.send_keys(Keys.TAB)
        time.sleep(2) # Pequena pausa para o endereço auto-preencher

        # Número (Opcional)
        if dados_inscricao_atual['numero_endereco']:
            print(f"Preenchendo Número: {dados_inscricao_atual['numero_endereco']}")
            campo_numero = driver.find_element(By.NAME, "numero")
            campo_numero.send_keys(dados_inscricao_atual['numero_endereco'])
        
        # Complemento (Opcional)
        if dados_inscricao_atual['complemento_endereco']:
            print(f"Preenchendo Complemento: {dados_inscricao_atual['complemento_endereco']}")
            campo_complemento = driver.find_element(By.NAME, "complemento")
            campo_complemento.send_keys(dados_inscricao_atual['complemento_endereco'])

        
        # --- Salvar ---
        print("Tentando clicar no botão 'Salvar'...")
        botao_salvar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Salvar')]" ))
        )
        botao_salvar.click()
        print("Botão 'Salvar' clicado com sucesso!")
        time.sleep(3)
       
except Exception as e:
        print(f"Erro ao preencher campos ou salvar para {dados_inscricao_atual['nome_completo']}: {e}")
 
 
 # --- Seção para adicionar Responsável ---
try:
    print("Tentando clicar na aba 'Responsável'...")
    tab_responsavel = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Responsável")) 
    )
    tab_responsavel.click()
    print("Aba 'Responsável' clicada com sucesso!")
    time.sleep(2) 

        # Salva o handle da janela principal ANTES de clicar em "+ Novo"
    main_window_handle = driver.current_window_handle
    print(f"Handle da janela principal: {main_window_handle}")

        # --- Clicar no botão '+ Novo' para adicionar Responsável ---
    print("Tentando clicar no botão '+ Novo' da aba Responsável...")
    add_responsavel_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '+ Novo')]")) 
    )
    add_responsavel_button.click()
    print("Botão '+ Novo' da aba Responsável clicado com sucesso!")
    time.sleep(3) # Tempo para a nova aba/janela carregar

        # --- Mudar o foco para a nova aba/janela ---
    new_window_handle = None
        # Espera até que o número de janelas seja 2 (original + nova)
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2)) 
        
        # Itera sobre todas as handles para encontrar a nova
    for window_handle in driver.window_handles:
        if window_handle != main_window_handle:
            new_window_handle = window_handle
            break
        
    if new_window_handle:
        driver.switch_to.window(new_window_handle)
        print(f"Foco mudado para a nova janela (Handle: {new_window_handle})")
        print(f"URL da nova janela: {driver.current_url}") # Para depuração

            # --- AQUI VOCÊ ADICIONARÁ O CÓDIGO PARA PREENCHER OS CAMPOS DO RESPONSÁVEL ---
            # Use os dados do CSV para o responsável:
            # Certifique-se que seu CSV tem as colunas para o responsável:
            # 'nome_responsavel', 'cpf_responsavel', 'tipo_responsavel', etc.
            
        print(f"Preenchendo formulário do responsável para {dados_inscricao_atual['nome_responsavel']}...")
            
            # Exemplo de preenchimento (AJUSTE OS NOMES DOS CAMPOS/SELETORES conforme a nova aba):
            # Nome do Responsável
        campo_nome_responsavel = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "nome_responsavel"))
        )
        campo_nome_responsavel.send_keys(dados_inscricao_atual['nome_responsavel'])
        campo_nome_responsavel.send_keys(Keys.TAB)
        time.sleep(0.5)

            # Tipo de Responsável (Dropdown - exemplo, ajuste seletor)
        if 'tipo_responsavel' in dados_inscricao_atual and dados_inscricao_atual['tipo_responsavel']:
            print(f"Selecionando Tipo de Responsável: {dados_inscricao_atual['tipo_responsavel']}")
                # Você precisará inspecionar o dropdown "Tipo de Responsável" na nova aba
                # Se for um select2 como os outros, pode ser algo como:
                # tipo_responsavel_dropdown_abrir = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.ID, "select2-id_do_tipo_responsavel-container"))
                # )
                # tipo_responsavel_dropdown_abrir.click()
                # opcao_tipo_responsavel = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{dados_inscricao_atual['tipo_responsavel']}')]"))
                # )
                # opcao_tipo_responsavel.click()
                # time.sleep(0.5)
            pass # Substitua pelo código real

            # CPF do Responsável (usar JavaScript, como no CPF principal)
            print(f"Preenchendo CPF do Responsável com JavaScript: {dados_inscricao_atual['cpf_responsavel']}")
            campo_cpf_responsavel = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "cpf")) # Verifique o 'name' real na nova aba
            )
            campo_cpf_responsavel.clear()
            driver.execute_script(f"arguments[0].value = '{dados_inscricao_atual['cpf_responsavel']}';", campo_cpf_responsavel)
            driver.execute_script("arguments[0].blur();", campo_cpf_responsavel)
            time.sleep(0.5)

            # RG do Responsável (Opcional)
            if 'rg_responsavel' in dados_inscricao_atual and dados_inscricao_atual['rg_responsavel']:
                print(f"Preenchendo RG do Responsável: {dados_inscricao_atual['rg_responsavel']}")
                campo_rg_responsavel = driver.find_element(By.NAME, "rg") # Verifique o 'name' real
                campo_rg_responsavel.send_keys(dados_inscricao_atual['rg_responsavel'])
                campo_rg_responsavel.send_keys(Keys.TAB)

            # CEP do Responsável
            print(f"Preenchendo CEP do Responsável: {dados_inscricao_atual['cep_responsavel']}")
            campo_cep_responsavel = driver.find_element(By.NAME, "cep") # Verifique o 'name' real
            campo_cep_responsavel.send_keys(dados_inscricao_atual['cep_responsavel'])
            campo_cep_responsavel.send_keys(Keys.TAB)
            time.sleep(2) # Tempo para auto-preenchimento do endereço

            # Número do Endereço do Responsável (Opcional)
            if 'numero_responsavel' in dados_inscricao_atual and dados_inscricao_atual['numero_responsavel']:
                print(f"Preenchendo Número do Responsável: {dados_inscricao_atual['numero_responsavel']}")
                campo_numero_responsavel = driver.find_element(By.NAME, "numero") # Verifique o 'name' real
                campo_numero_responsavel.send_keys(dados_inscricao_atual['numero_responsavel'])
                campo_numero_responsavel.send_keys(Keys.TAB)

            # Complemento do Endereço do Responsável (Opcional)
            if 'complemento_responsavel' in dados_inscricao_atual and dados_inscricao_atual['complemento_responsavel']:
                print(f"Preenchendo Complemento do Responsável: {dados_inscricao_atual['complemento_responsavel']}")
                campo_complemento_responsavel = driver.find_element(By.NAME, "complemento") # Verifique o 'name' real
                campo_complemento_responsavel.send_keys(dados_inscricao_atual['complemento_responsavel'])
                campo_complemento_responsavel.send_keys(Keys.TAB)

            # --- Clicar no botão 'Salvar' do formulário do Responsável ---
            print("Tentando clicar no botão 'Salvar' do formulário do Responsável...")
            # Assumindo que o botão Salvar é igual ao da inscrição principal
            botao_salvar_responsavel = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Salvar')]"))
            )
            botao_salvar_responsavel.click()
            print("Botão 'Salvar' do Responsável clicado com sucesso!")
            time.sleep(3) # Tempo para salvar e a janela fechar/redirecionar

            # --- Verificar se a nova aba fechou automaticamente após salvar ---
            # Se não fechou, você pode fechar explicitamente:
            # driver.close() # Fecha a aba que está com foco (a do responsável)
            # print("Nova janela/aba do responsável fechada.")

        else:
            print("Erro: Não foi possível encontrar a nova janela/aba do responsável.")
            # Decide se quer continuar ou parar se a nova janela não for encontrada


        # --- Voltar o foco para a janela principal ---
        driver.switch_to.window(main_window_handle)
        print("Foco retornado para a janela principal.")
        time.sleep(1) # Pequena pausa após retornar o foco

except Exception as e:
        print(f"Erro ao navegar para aba Responsável ou adicionar/preencher/salvar novo: {e}")
        # Tenta voltar para a janela principal se um erro ocorreu na janela do responsável
        try:
            driver.switch_to.window(main_window_handle)
            print("Tentativa de retornar à janela principal após erro na aba do responsável.")
        except Exception as ex:
            print(f"Não foi possível retornar à janela principal: {ex}")


         
    
print("Aguardando 5 segundos para visualização...")
time.sleep(10) 

# --- Fechar o navegador ---
print("Fechando o navegador.")
driver.quit()

print("Automação concluída!")