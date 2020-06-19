from selenium import webdriver
from constants import id_
from constants import url
from constants import css
from constants import skill
from selenium.webdriver.support.ui import Select
import datetime
from time import sleep

DRAW = -1
NOT_YET = 0
PLAYER_1 = 1
PLAYER_2 = 2

def get_time(hours=0, minutes=0, seconds=0):
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours)

class BrowserError(Exception):
    pass

class Browser:
    def __init__(self, driver):
        self.driver = driver

    def get_current_page(self):
        return self.driver.current_url

    def get_page(self, url):
        current_url = self.get_current_page()
        if current_url == url:
            return True
        self.driver.get(url)
        current_url = self.get_current_page()
        if current_url == url:
            return True
        raise BrowserError('Erro ao acessar {}'.format(url))

    def login(self, email, password):
        self.get_page(url.HOME)
        header = self.driver.find_element_by_id(id_.FORMULARIO)
        email_box = header.find_element_by_id(id_.EMAIL)
        password_box = header.find_element_by_id(id_.PASSWORD)
        email_box.send_keys(email)
        password_box.send_keys(password)

    def get_ninjas(self):
        self.get_page(url.NINJA_SELECT)
        body = self.driver.find_element_by_id(id_.RIGHT)
        ninjas_imgs =  body.find_elements_by_css_selector(css.NINJA_SELECT_IMAGE)
        self.ninjas = []
        for button in ninjas_imgs:
            button.click()
            self.ninjas.append(Ninja(self.driver))
        return self.ninjas
    
    def select_ninja(self, ninja_name):
        self.get_page(url.NINJA_SELECT)
        body = self.driver.find_element_by_id(id_.RIGHT)
        ninjas_imgs =  body.find_elements_by_css_selector(css.NINJA_SELECT_IMAGE)
        for button in ninjas_imgs:
            button.click()
            ninja = Ninja(body)
            if ninja.name == ninja_name:
                button = body.find_element_by_link_text('Jogar')
                button.click()
                return True
        raise BrowserError('Erro ao selecionar ninja: {}'.format(ninja_name))

    def close_pop_up(self):
        try:
            pop_up = self.driver.find_element_by_css_selector(POP_UP)
            close_button = pop_up.find_element_by_css_selector(BUTTON+CLOSE)
            close_button.click()
        except:
            raise BrowserError('Erro ao fechar pop-up')

class NinjaError(Exception):
    pass

class Ninja(Browser):
    def __init__(self, driver=None):
        if(driver):
            self.driver = driver
            self.name = self.driver.find_element_by_id(id_.NINJA_NAME).text
            self.level = self.driver.find_element_by_id(id_.NINJA_LEVEL).text
            self.ryous = self.driver.find_element_by_id(id_.NINJA_RYOUS).text
    
    def select(self):
        self.select_ninja(self.name)

    def update_status(self, mode='Normal'):
        if mode=='Normal':
            self.get_page(url.NINJA_STATUS)
            body_left = self.driver.find_element_by_id(id_.LEFT)
            ninja_name = body_left.find_element_by_css_selector(css.NAME).text
            if ninja_name!= self.name:
                raise NinjaError('O ninja {} não corresponde ao ninja esperado'.format(ninja_name))
        try:
            header = self.driver.find_element_by_id(STATUS_ICONS)
            self.current_life, self.max_life = map(int, header.find_element_by_id(HEART_ICON).text.split('/'))
            self.current_chakra, self.max_chakra = map(int, header.find_element_by_id(CHAKRA_ICON).text.split('/'))
            self.current_stamina, self.max_stamina = map(int, header.find_element_by_id(STAMINA_ICON).text.split('/'))
            return True
        except:
            return False

    def training_attributes(self, num):
        self.get_page(url.TRAINING_ATTRIBUTES)
        self.close_pop_up()
        body = self.driver.find_element_by_id(id_.PAGE_BODY)
        select = Select(body.find_element_by_id(id_.QUANTITY))
        option = select.options[0]
        diff = abs(int(option.text)-num)
        for op in select.options:
            n = int(op.text)
            if abs(n-num)<diff:
                option = op
                diff = abs(n-num)
        option.click()
        button = body.find_element_by_link_text('Treinar')
        button.click()

    def make_task(self):
        self.get_page(url.TASK)
        body = self.driver.find_element_by_id(id_.RIGHT)
        buttons = body.find_elements_by_css_selector(css.BUTTON)
        disabled_buttons = body.find_elements_by_css_selector(css.BUTTON+css.DISABLED)
        for button in buttons:
            if not button in disabled_buttons:
                button.click()
                return get_time(minutes=1)
        raise NinjaError('Nenhuma tarefa foi encontrada')
    
    def get_mission(self):
        self.get_page(url.MISSION_STATUS)
        body = self.driver.find_element_by_id(id_.RIGHT)
        try:
            body.find_element_by_link_text('Missão Concluída')
        except:
            NinjaError('Missão não foi concluída ou ninja não está em missão')
        button = body.find_element_by_css_selector(css.BUTTON)   
        button.click()

    def update_battle_status(self):
        body = self.driver.find_element_by_id(id_.PAGE_BODY)
        left = body.find_element_by_css_selector(css.BATTLE_LEFT)
        right = body.find_element_by_css_selector(css.BATTLE_RIGHT)
        lhea = left.find_element_by_id(id_.PLAYER_HEART)
        rhea = right.find_element_by_id(id_.ENEMY_HEART)
        lcha = left.find_element_by_id(id_.PLAYER_CHAKRA)
        rcha = right.find_element_by_id(id_.ENEMY_CHAKRA)
        lsta = left.find_element_by_id(id_.PLAYER_STAMINA)
        rsta = right.find_element_by_id(id_.ENEMY_STAMINA)
        enemy = Ninja()
        enemy.name = right.find_element_by_css_selector(css.NAME_BATTLE).text
        enemy.current_life = int(rhea.text.split()[1])
        enemy.current_chakra = int(rcha.text.split()[1])
        enemy.current_stamina = int(rsta.text.split()[1])
        self.current_life = int(lhea.text.split()[1])
        self.current_chakra = int(lcha.text.split()[1])
        self.current_stamina = int(lsta.text.split()[1])
        return enemy

    def print_status(self, ninja):
        print('----')
        print('Ninja: {}'.format(ninja.name))
        print('Vida: {}'.format(ninja.current_life))
        print('Chakra: {}'.format(ninja.current_chakra))
        print('Stamina: {}'.format(ninja.current_stamina))
        print('----')

    def get_winner(self, p1, p2):
        m_p1 = min(p1.current_life, min(p1.current_chakra, p1.current_stamina))
        m_p2 = min(p2.current_life, min(p2.current_chakra, p2.current_stamina))
        if m_p1<10 and m_p2<10:
            return DRAW
        elif m_p1<10 and not m_p2<10:
            return PLAYER_2
        elif not m_p1<10 and m_p2<10:
            return PLAYER_1
        else:
            return NOT_YET

    def get_story_mod(self):
        N_PAGES = 4
        self.get_page(url.HISTORY_MODE)
        body = self.driver.find_element_by_id(id_.RIGHT)
        b_tab = body.find_element_by_id(id_.BUTTONS_TAB)
        options = b_tab.find_elements_by_css_selector(css.BUTTON)
        contents = [id_.HM_BATTLE_PAGE1, id_.HM_BATTLE_PAGE2, id_.HM_BATTLE_PAGE3, id_.HM_BATTLE_PAGE4]
        for i in range(N_PAGES):
            options[i].click()
            content = body.find_element_by_id(contents[i])
            done_chs = content.find_elements_by_css_selector(css.COMPLETE_HISTORY)
            chs = content.find_elements_by_css_selector(css.HISTORY)
            for chapter in chs:
                if chapter not in done_chs:
                    exp = chapter.find_element_by_css_selector(css.EXPAND_BUTTON)
                    exp.click()
                    history = content.find_element_by_css_selector(css.HISTORY_EXPANDED)
                    buttons = history.find_elements_by_css_selector(css.BUTTON)
                    for button in buttons:
                        if button.text == 'Duelar':
                            button.click()
                            return True
                    raise NinjaError('Não foi possível batalhar no modo história')
        raise NinjaError('O usuário já completou o modo história')
        
    def figth(self, blows):
        self.get_page(url.DOJO_FIGHT)
        body = self.driver.find_element_by_id(id_.PAGE_BODY)
        #options = body.find_elements_by_css_selector(BATTLE_OPTIONS)
        att_list = body.find_element_by_id(id_.SKILL_LIST)
        enemy = self.update_battle_status()
        n = len(blows)
        i = 0
        while True:
            blow = blows[i%n]
            i+=1
            win = self.get_winner(self, enemy)
            if win==NOT_YET:
                try:
                    self.print_status(self)
                    self.print_status(enemy)
                    button = att_list.find_element_by_id(blow)
                    button.click()
                    body.click()
                    enemy = self.update_battle_status()
                    sleep(2)
                except:
                    print('Erro ao atacar')
            else:
                sleep(3)
                for _ in range(3):
                    try:
                        msg = body.find_element_by_id(BATTLE_MESSAGE)
                        link = msg.find_element_by_css_selector(TEXT_LINK)
                        link.click()
                        break
                    except:
                        print('Esperando mensagem para finalizar...')
                        sleep(3)
                if win==DRAW:
                    print('Empate')
                    return False
                elif win==PLAYER_1:
                    print('Você ganhou')
                    return True
                elif win==PLAYER_2:
                    print('Você perdeu')
                    return False
                raise NinjaError('Erro inesperado na função figth')

    
    