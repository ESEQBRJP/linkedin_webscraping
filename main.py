from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
from logger import XlsxUteis

link_vagas: list = []
job_titles: list = []
company_names: list = []
company_locations: list = []
work_methods: list = []
post_dates: list = []
work_times: list = []
job_desc: list = []


class linkedinScraping:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.email = "xxxxxxxxxxxxxx@gmail.com"
        self.paswrd = pyautogui.password(text='Insira sua senha', title='Senha Linkedin', default='', mask='*')
        self.driver.get("https://www.linkedin.com/")
        time.sleep(2)

    def login_linkedin(self):
        login = self.driver.find_element(By.ID, "session_key")
        password = self.driver.find_element(By.ID, "session_password")
        login.clear()
        password.clear()
        login.send_keys("xxxxxxxxxxxxxxxx")
        time.sleep(2)
        password.send_keys(self.paswrd)
        self.driver.find_element(By.XPATH,
                                 """//*[@id="main-content"]/section[1]/div/div/form[1]/div[2]/button""").click()
        time.sleep(15)

    def pesquisa_linkedin(self):
        barra_pesquisa = self.driver.find_element(By.XPATH, """//*[@id="global-nav-typeahead"]/input""")
        barra_pesquisa.clear()
        barra_pesquisa.send_keys("desenvolvedor javascript")
        barra_pesquisa.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.find_element(By.XPATH, """//*[@id="search-reusables__filters-bar"]/ul/li[1]/button""").click()
        time.sleep(4)
        # self.driver.find_element(By.XPATH, """//*[@id="mmcAxgX4SAyGZQADfRdMTg=="]/div/div[2]/a""").click()

    def armazena_links(self):
        try:
            for page in range(2, 4):
                time.sleep(2)
                bloco_v = self.driver.find_elements(By.CLASS_NAME, """scaffold-layout__list-container""")
                v_list = bloco_v[0].find_elements(By.CSS_SELECTOR, """.jobs-search-results__list-item""")

                for job in v_list:
                    all_links = job.find_elements(By.TAG_NAME, 'a')
                    for a in all_links:
                        if str(a.get_attribute('href')).startswith(
                                "https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in link_vagas:
                            link_vagas.append(a.get_attribute('href'))
                        else:
                            pass
                    # scroll down for each job element
                    self.driver.execute_script("arguments[0].scrollIntoView();", job)

                print(f'Coletando os links da página: {page - 1}')
                # go to next page:
                self.driver.find_element(By.XPATH, f"/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[1]/div/div[6]/ul/li[{page}]").click()
                time.sleep(3)
        except Exception as Error:
            print(Error)
        print('Encontrado ' + str(len(link_vagas)) + ' links com vagas')

    def busca_dados_pagina(self):
        i = 0
        j = 1
        # Visit each link one by one to scrape the information
        print('Visiting the links and collecting information just started.')
        for i in range(len(link_vagas)):
        # for i in range(2):
            try:
                self.driver.get(link_vagas[i])
                i = i + 1
                time.sleep(2)
                # Click See more.
                self.driver.find_element(By.CLASS_NAME, "artdeco-card__actions").click()
                time.sleep(2)
            except:
                pass

            # Find the general information of the job offers
            contents = self.driver.find_elements(By.CLASS_NAME, 'p5')
            for content in contents:
                try:
                    job_titles.append(content.find_element(By.TAG_NAME, "h1").text)
                    company_names.append(
                        content.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name").text)
                    company_locations.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet").text)
                    work_methods.append(
                        content.find_element(By.CLASS_NAME, "jobs-unified-top-card__workplace-type").text)
                    post_dates.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__posted-date").text)
                    work_times.append(content.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-insight").text)
                    print(f'Scraping the Job Offer {j} DONE.')
                    j += 1

                except:
                    pass
                time.sleep(2)

                # Scraping the job description
            job_description = self.driver.find_elements(By.CLASS_NAME, 'jobs-description__content')
            for description in job_description:
                job_text = description.find_element(By.CLASS_NAME, "jobs-box__html-content").text
                job_desc.append(job_text)
                time.sleep(2)

    def gera_pdf(self):
        logger = XlsxUteis()
        logger_data = []
        HEADER = ["Nome_vaga", "Empresa", "Localidade", "Tipo_trabalho", "Data_postagem", "Periodo_trabalho", "Descrição_vaga"]
        for job_title, company_name, company_location, work_method, post_date, work_time, job_descri in zip(job_titles,
                                                                                                company_names,
                                                                                                company_locations,
                                                                                                work_methods,
                                                                                                post_dates,
                                                                                                work_times,
                                                                                                job_desc):
            logger_data.append([job_title, company_name, company_location, work_method, post_date, work_time, job_descri])

        logger.append_sheet_log_data("vagas", HEADER, logger_data)

    def encerra_conexao(self):
        self.driver.close()


LS = linkedinScraping()
LS.login_linkedin()
LS.pesquisa_linkedin()
LS.armazena_links()
LS.busca_dados_pagina()
LS.gera_pdf()
LS.encerra_conexao()
