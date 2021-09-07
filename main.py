from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from login import loginemail, loginpass

commentstexts = ["carinha sorridente", "carinha piscando", "polegar para cima",
                 "bíceps flexionados", "mãos batendo palmas", "foguete", "dedos cruzados", "Seta VOLTAR AO TOPO"
                 ]


driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")
time.sleep(3)

# Sign in users data
inputuser = driver.find_element_by_xpath('//*[@id="username"]')
inputpass = driver.find_element_by_xpath('//*[@id="password"]')

inputuser.click()
inputuser.send_keys(loginemail)
time.sleep(2)
inputpass.click()
inputpass.send_keys(loginpass)
time.sleep(3)

driver.find_element_by_xpath(
    '//*[@id="organic-div"]/form/div[3]/button').click()
time.sleep(7)

actions = ActionChains(driver)


def DoComments():

    buttoncomments = driver.find_elements_by_xpath(
        "//button[contains(@aria-label,'Comentário sobre a publicação') ]")
    print(len(buttoncomments))
    driver.execute_script("window.scrollTo(0, 0);")

    poststring = "//div[contains(@data-urn,'urn:li:activity')]"

    posts = driver.find_elements_by_xpath(poststring)

    print(len(posts))
    for post in posts:
        actions.move_to_element(post).perform()
        buttoncomment = post.find_element_by_xpath(
            "/.//button[(@aria-label='Comentar')]")

        actions.move_to_element(buttoncomment).perform()
        buttoncomment.click()
        time.sleep(2)

        emojibutton = post.find_element_by_xpath(
            "/.//button[@title='Abrir teclado de emojis']")
        actions.move_to_element(emojibutton).perform()
        emojibutton.click()
        time.sleep(3)

        time.sleep(2)
        mensageindex = commentstexts[random.randint(0, len(commentstexts)-1)]
        mensage = driver.find_element_by_xpath(
            f"//button[@title='{ mensageindex }']"
        )
        emojisearch = driver.find_element_by_xpath(
            "//*[@id='emoji-popover-search-input-']")
        emojisearch.click()
        time.sleep(1)
        emojibutton.send_keys(mensageindex)

        print(mensageindex)
        mensage.click()
        time.sleep(2)

        buttonpublic = post.find_element_by_xpath(
            "/.//span[@class='artdeco-button__text' and text()='Publicar']")
        # buttonpublic.click()
        postactor = post.find_element_by_xpath(
            "/.//div/div[1]/a/div[3]/span[1]/span/span").text
        print(f"Enviado o comentário {mensageindex} para {postactor}")
        print("Aguardando 60 segundos")
        time.sleep(60)


def DoLikes():
    # Find and load posts for likes. Minimum of 10 likes
    likes = []
    while len(likes) < 9:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        likes = driver.find_elements_by_xpath(
            "//div[contains(@id,'ember')]//div[contains(@class,'feed-shared-social-actions')]//button[@aria-pressed='false' and contains(@aria-label,'Gostar da publicação') ]"
        )
        time.sleep(3)

    print(len(likes))
    driver.execute_script("window.scrollTo(0, 0);")

    # Like loop
    for like in likes:
        like.click()
        time.sleep(10)
        print("Aguardando 10 segundos")
    print(f"Terminamos! Foram curtidas {len(likes)} posts no seu feed.")


reloads = 0
while reloads < 10:
    if reloads > 0:
        time.sleep(6000)
        driver.refresh()
    reloads += 1
    print(f"Laço numero {reloads}")

    #Likes in posts
    DoLikes()

    # Comment in posts
    # DoComments()
