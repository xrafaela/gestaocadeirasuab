from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Configuração do navegador
def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar em segundo plano (opcional)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# Login no Moodle
def moodle_login(driver, email, password):
    driver.get(
        "https://cas2.uab.pt/cas/login?service=https%3A%2F%2Felearning.uab.pt%2Flogin%2Findex.php"
    )
    try:
        print("✅ Navegou para a página de login")  # Adicionado

        # Espera até que o campo de nome de usuário esteja presente
        print("⏳ Esperando pelo campo de nome de usuário")  # Adicionado
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        print("✅ Campo de nome de usuário encontrado")  # Adicionado
        username_field.send_keys(email)

        # Espera até que o campo de senha esteja presente
        print("⏳ Esperando pelo campo de senha")  # Adicionado
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        print("✅ Campo de senha encontrado")  # Adicionado
        password_field.send_keys(password)

        # Espera até que o botão de login esteja clicável
        print("⏳ Esperando pelo botão de login")  # Adicionado
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )
        print("✅ Botão de login encontrado")  # Adicionado
        login_button.click()
        print("✅ Clicou no botão de login")  # Adicionado

    except Exception as e:
        print(f"❌ Erro ao fazer login: {e}")
        driver.quit()
        exit()


# Extrair tarefas da página /my/
def extract_tasks(driver):
    driver.get("https://elearning.uab.pt/my/")
    try:
        print("✅ Navegou para a página de tarefas")  # Adicionado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".event"))
        )
        tasks = []
        for task_element in driver.find_elements(By.CSS_SELECTOR, ".event"):
            task_name = task_element.find_element(By.CSS_SELECTOR, ".event-title").text
            task_date = task_element.find_element(By.CSS_SELECTOR, ".event-time").text
            tasks.append({"name": task_name, "due_date": task_date})
        print(f"✅ Encontrou {len(tasks)} tarefas")  # Adicionado
        return tasks
    except Exception as e:
        print(f"❌ Erro ao extrair tarefas: {e}")
        return []


# Salvar tarefas em JSON
def save_tasks(tasks, filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump(tasks, f, indent=2)


# Execução principal
def main():
    email = "SEU_EMAIL@uab.pt"  # Substitua pelo seu email
    password = "SUA_SENHA"  # Substitua pela sua senha

    driver = setup_browser()
    try:
        moodle_login(driver, email, password)
        tasks = extract_tasks(driver)
        save_tasks(tasks)
        print(f"✅ {len(tasks)} tarefas salvas em 'tasks.json'!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
