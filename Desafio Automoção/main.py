import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurações do WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def read_credentials_from_csv(file_path):
    """Lê as credenciais de login de um arquivo CSV"""
    data = pd.read_csv(file_path)
    return data['username'][0], data['password'][0]

def login(driver, username, password):
    """Realiza o login no site Swag Labs"""
    driver.get('https://www.saucedemo.com/')
    enter_username(driver, username)
    enter_password(driver, password)
    click_login_button(driver)

def enter_username(driver, username):
    """Insere o nome de usuário"""
    find_element_and_send_keys(driver, By.ID, 'user-name', username)

def enter_password(driver, password):
    """Insere a senha"""
    find_element_and_send_keys(driver, By.ID, 'password', password)

def click_login_button(driver):
    """Clica no botão de login"""
    find_element_and_click(driver, By.ID, 'login-button')

def add_item_to_cart(driver, item_name):
    """Adiciona um item ao carrinho"""
    find_item_and_click_add_to_cart(driver, item_name)

def process_checkout(driver):
    """Realiza o checkout"""
    click_shopping_cart(driver)
    click_checkout(driver)
    enter_shipping_info(driver)
    click_continue(driver)

def find_element_and_send_keys(driver, by, selector, keys):
    """Encontra um elemento e insere texto"""
    time.sleep(2)  # Aguarda para garantir que a página carregue completamente
    driver.find_element(by, selector).send_keys(keys)

def find_element_and_click(driver, by, selector):
    """Encontra um elemento e clica nele"""
    time.sleep(1)  # Aguarda para garantir que o elemento esteja interativo
    driver.find_element(by, selector).click()

def find_item_and_click_add_to_cart(driver, item_name):
    """Encontra um item e adiciona ao carrinho"""
    time.sleep(2)  # Aguarda para garantir que o elemento esteja visível
    item_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
    driver.find_element(By.XPATH, item_xpath).click()

def click_shopping_cart(driver):
    """Clica no carrinho de compras"""
    find_element_and_click(driver, By.CLASS_NAME, 'shopping_cart_link')

def click_checkout(driver):
    """Clica no botão de checkout"""
    find_element_and_click(driver, By.ID, 'checkout')

def enter_shipping_info(driver):
    """Insere informações de envio"""
    enter_first_name(driver, 'Test')
    enter_last_name(driver, 'User')
    enter_postal_code(driver, '12345')

def enter_first_name(driver, first_name):
    """Insere o primeiro nome"""
    find_element_and_send_keys(driver, By.ID, 'first-name', first_name)

def enter_last_name(driver, last_name):
    """Insere o sobrenome"""
    find_element_and_send_keys(driver, By.ID, 'last-name', last_name)

def enter_postal_code(driver, postal_code):
    """Insere o código postal"""
    find_element_and_send_keys(driver, By.ID, 'postal-code', postal_code)

def click_continue(driver):
    """Clica no botão de continuar"""
    find_element_and_click(driver, By.ID, 'continue')

def get_cart_total(driver):
    """Obtém o valor total do carrinho"""
    click_shopping_cart(driver)
    total = driver.find_element(By.CLASS_NAME, 'summary_total_label').text
    return total

def print_cart_total(driver):
    """Imprime o valor total do carrinho"""
    total = get_cart_total(driver)
    print(f"Valor total: {total}")

def main():
    username, password = read_credentials_from_csv('login_data.csv')
    login(driver, username, password)
    
    items_to_add = [
        "Test.allTheThings() T-Shirt (Red)",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Bike Light"
    ]
    
    for item in items_to_add:
        add_item_to_cart(driver, item)
    
    process_checkout(driver)
    time.sleep(2)  # Aguarda um pouco para garantir que o checkout seja concluído
    
    print_cart_total(driver)
    
    # Aguarda 20 segundos para visualização antes de fechar o navegador
    time.sleep(20)
    
    driver.quit()

if __name__ == "__main__":
    main()
