import requests
import shutil
from IPython.display import Image
from bs4 import BeautifulSoup
import logging
import webbrowser
import json
from time import sleep

JUPTER = False
DEBUG = True

#MAIN_SITE = 'http://cdzgame.com.br/'
MAIN_SITE = 'https://narutogame.com.br/'
#MAIN_SITE = 'http://dragonballgame.com.br/'
class urls:
    CAPTCHA = MAIN_SITE + 'index.php?acao=captcha&s'
    LOGIN = MAIN_SITE +'index.php?acao=login'
    CHARACTERS_PAGE = MAIN_SITE + 'index.php?secao=personagem_selecionar'
    CHARACTER_SELECT = MAIN_SITE + 'index.php?acao=personagem_selecionar_jogar'
    TRAIN =  MAIN_SITE + 'index.php?acao=academia_treinamento_treinar'
    TRAIN_PAGE = MAIN_SITE + 'index.php?secao=academia_treinamento'
    TASK_PAGE = MAIN_SITE + 'index.php?secao=licoes'
    MISSION_PAGE = MAIN_SITE + 'index.php?secao=missoes'
    TAKE_MISSION = MAIN_SITE + 'index.php?acao=missoes_aceitar'
    FINISH_MISSION_PAGE = MAIN_SITE + 'index.php?secao=missoes_espera'
    FINISH_MISSION = MAIN_SITE + 'index.php?acao=missoes_concluida_finaliza'
    CHARACTER_STATUS = MAIN_SITE +'index.php?secao=personagem_status'
    TRAIN_JUTSU = MAIN_SITE + 'index.php?acao=personagem_jutsu'
    TRAIN_JUTSU_PAGE = MAIN_SITE + 'index.php?secao=personagem_jutsu'
    FIDELITY = MAIN_SITE + 'index.php?acao=reward_fidelidade'
    GET_NINJA_CONTEST = MAIN_SITE + 'index.php?acao=estudo_ninja'
    POST_NINJA_CONTEST = MAIN_SITE + 'index.php?acao=estudo_ninja_final'
    
    DOJO_PAGE = MAIN_SITE + 'index.php?secao=dojo'
    CREATE_DOJO = MAIN_SITE + 'index.php?acao=dojo_lutador_criar'
    DOJO_START = MAIN_SITE + 'index.php?acao=dojo_lutador_lutar'
    FIGTH_PAGE = MAIN_SITE + 'index.php?secao=dojo_batalha_lutador'
    FIGTH_ACTION = MAIN_SITE + 'index.php?acao=dojo_lutador_lutar'
    
def dowload_page(rq, file_name):
    f = open(file_name, 'wb')
    rq.raw.decode_content = True
    shutil.copyfileobj(rq.raw, f)  

def show_image(file_name):
    if(JUPTER):
        pil_img = Image(filename=file_name)
        display(pil_img)
    else:
        webbrowser.open(file_name)

def p_get(s, att):
    att = att + ': '
    res = s[s.index(att)+len(att):]
    return res[:res.index(",")]

def start_session():
    headers = { 
        'Referer': 'https://narutogame.com.br/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.3',
    }
    s = requests.Session()
    s.headers = headers
    return s

def get_questions():
    try:
        with open('questions.json') as json_file:
            questions = json.load(json_file)
    except:
        questions = {}
    return questions

def save_questions(questions={}):
    with open('questions.json', 'w') as json_file:
        json.dump(questions, json_file)

def update_questions(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    vs = []
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        vs.append(line)
    tam = len(vs)
    key = ''
    questions = get_questions()
    for i in range(tam):
        if i%2==0:
            key = vs[i]
        else:
            questions[key] = vs[i][prefix_tam:]
    save_questions(questions)

def get_contest_ans(file_path):
    ac = 0
    questions = get_questions()
    with open(file_path) as f:
        soup = BeautifulSoup(f, 'html.parser')
    data = {}
    data['key'] = soup.find('form', id='f-estudo-ninja').find('input')['value']

    lst = soup.find_all('div', class_='bingo_book_pagina')
    for l in lst:
        try:
            quest = l.find('div', class_='nome2').text.strip()
            vs = l.find('div', class_='recompensa').find_all('li')
        except:
            continue
        options = [] 
        for x in vs:
            ans = x.text.strip()
            key = x.find('input')['name']
            value = x.find('input')['value']
            options.append((ans, key, value))

        ans, key, value = options[0]
        data[key] = value
        if quest in questions:
            for ans, key, value in options:
                if ans in questions[quest]:
                    data[key] = value
                    ac += 1
        else:
            pass
    print('Expected result are ' + str(ac) + ' correct ans')
    return data

def get_dojo_info(file_path):
    with open(file_path) as f:
        soup = BeautifulSoup(f, 'html.parser')
    scrs = soup.find_all('script')
    atks = []
    pvp_token = ''
    for scr in scrs:
        lines = str(scr).split('\n')
        for line in lines:
            try:
                var, res = line.split('=')
            except:
                continue
            #print(line)
            if '_pToken' in var:
                pvp_token = res.strip()[1:-2]
            if '_items' in var:
                obj = json.loads(res.strip()[:-1])
                if 'id' in obj:
                    atks.append(obj)
    return pvp_token, atks
    
def get_strpage(rq):
    dowload_page(rq, 'html_pages/tmp.html')
    with open('html_pages/tmp.html') as f:
        s = f.read()
    return s
# Naruto functions

class Character:
    def __init__(self, soup):
        self.img_url = soup['src']
        st = soup['onclick']
        st = st[st.index('(')+1:st.index(')')]
        st = st[st.index(', ')+2:]
        self.id = st[1:st.index(',')-1]
        st = st[st.index(',')+1:]
        self.name = p_get(st, 'nome')[1:-1]
        
    def show(self):
        print('Nome:', self.name)
        if(JUPTER):
            r = requests.get(self.img_url, stream=True)
            dowload_page(r, 'tmp.png')
            show_image('tmp.png')
        

class Session:
    def __init__(self):
        self.session = start_session()
    
    def get_soup(self, url):
        r = self.session.get(url, stream=True)
        dowload_page(r, 'soup.html')
        f = open('soup.html')
        return BeautifulSoup(f, 'html.parser')

    def select_character(self, character):
        data = { 'id':character.id }
        r = self.session.post(urls.CHARACTER_SELECT, stream=True, data=data)
        dowload_page(r, 'html_pages/CHARACTER_SELECT.html')
        print('-----------')
        print('Character was selected')
        character.show()
        
    def download_captcha(self, file_name='captcha.png'):
        r = self.session.get(urls.CAPTCHA, stream=True)
        dowload_page(r, file_name)

    def login(self, email, password, captcha):
        data = {'email':email, 'senha':password, 'captcha':captcha, 'cookie':'28795253-3512-e25c-9356-3f0855ef97cf'}
        r = self.session.post(urls.LOGIN, stream=True, data=data)
        dowload_page(r, 'html_pages/LOGIN.html')
    
    def get_status(self):
        soup = self.get_soup(urls.CHARACTER_STATUS)
        hp = int(soup.find('div', id='cnPHPt').text.split('/')[0])
        sp = int(soup.find('div', id='cnPSPt').text.split('/')[0])
        sta = int(soup.find('div', id='cnPSTAt').text.split('/')[0])
        return hp, sp, sta
        
    def train(self):
        try:
            try:
                soup = self.get_soup(urls.TRAIN_PAGE)
                sp_cost = int(soup.find('span', id='cnTSP').text)
                sta_cost = int(soup.find('span', id='cnTSTA').text)
                hp, sp, sta = self.get_status()
            except AttributeError:
                print('Não foi possível treinar atributos')
                return
            qtd = min(sp//sp_cost, sta//sta_cost)
            data = { 'qtd':qtd }
            r = self.session.post(urls.TRAIN, stream=True, data=data)
            dowload_page(r, 'html_pages/TRAIN.html')
            print('Treino realizado ' + str(qtd) + ' vezes')
        except:
            if DEBUG:
                logging.exception('train error')


    def get_characters(self):
        soup = self.get_soup(urls.CHARACTERS_PAGE)
        characters = []
        for sp in soup.find_all('img', class_='imgPers'):
            characters.append(Character(sp))
        return characters

    def get_tasks(self):
        try:
            try:
                soup = self.get_soup(urls.TASK_PAGE)
                soup = soup.find('div', id='cnBase')
                bts = soup.find_all('a', class_='button')
            except AttributeError:
                print('Não foi possível encontrar uma tarefa')
                return [(0, 0)]
            missions = []
            for b in bts:
                try:
                    st = b['onclick']
                    st = st[st.index('(')+1:st.index(')')]
                    mission_id, mission_key = st.split(',')
                    missions.append((mission_id[1:-1], mission_key[1:-1]))
                except KeyError:
                    pass
            if len(missions)>0:
                return missions
            else:
                print('Não há tarefas realizaveis')
                return [(0, 0)]
        except:
            if DEBUG:
                logging.exception('get_tasks error')
            return [(0, 0)]

    def get_missions(self):
        try:
            try:
                soup = self.get_soup(urls.MISSION_PAGE)
                boxes = soup.find('div', id='missoes-tempo').find_all('tr', class_='cor_sim')
                boxes = boxes + soup.find('div', id='missoes-tempo').find_all('tr', class_='cor_nao')
            except:
                print('Não foi possível encontrar uma missão')
                return [ (0, 0, 0) ]
            missions = []
            for box in boxes:
                try:
                    b = box.find('a', class_='button')
                    st = b['onclick']
                    st = st[st.index('(')+1:st.index(')')].replace(' ', '')
                    tam = len(box.find('select').find_all('option'))
                    mission_id, _, mission_key = st.split(',')
                    missions.append( (mission_id[1:-1], mission_key[1:-1], tam))
                except KeyError:
                    pass
            if len(missions)>0:
                return missions
            else:
                print('Não há missões realizaveis')
                return [(0, 0, 0)]
        except:
            if DEBUG:
                logging.exception('get_missions error')
            return [ (0, 0, 0) ]

    def do_mission(self, mission_id, mission_key, m=None):
        try:
            data = {'id':mission_id, 'missoes_key':mission_key}
            if(m):
                data['m'] = m
            r = self.session.post(urls.TAKE_MISSION, stream=True, data=data)
            dowload_page(r, 'html_pages/TAKE_MISSION.html')
        except:
            if DEBUG:
                logging.exception('do_mission error')

    def get_targets(self):
        try:
            r = self.session.get(urls.TRAIN_JUTSU_PAGE, stream=True)
            dowload_page(r, 'html_pages/TRAIN_JUTSU_PAGE.html')
            with open('html_pages/TRAIN_JUTSU_PAGE.html') as f:
                soup = BeautifulSoup(f, 'html.parser')
            ops = soup.find_all('div', class_='option')
            img_url = 'https://narutogame.com.br/images/layout/sem_aprimoramento.png'
            res = {}
            ops.reverse()
            for op in ops:
                if(op.find('img')['src']==img_url):
                    slot = int(op['data-slot'])
                    uid = int(op['data-target'])
                    if not uid in res:
                        res[uid] = int(1e9)
                    res[uid] = min(res[uid], slot)
            return list(res.items())
        except:
            if DEBUG:
                logging.exception('get_targets error')
            return[(0, 0)]

    def train_jutsu(self, target, slot):
        try:
            list_ = 1
            data = {'list':list_, 'slot':slot, 'target':target}
            r = self.session.post(urls.TRAIN_JUTSU, data=data)
            response_data = r.json()
            items = []
            if 'items' in response_data:
                items = response_data['items']
            if len(items)==0:
                print('Error in train jutsu')
            equip = int(items[0]['slot'])
            uid = int(items[0]['id'])

            data = {'equip':equip, 'slot':slot, 'uid':uid, 'target':target}
            r = self.session.post(urls.TRAIN_JUTSU, data=data)
            response_data = r.json()
            print('Jutsu trained if he has points')
        except:
            if DEBUG:
                logging.exception('get_targets error')

    def do_first_task(self):
        mission_id, mission_key = self.get_tasks()[0]
        if mission_id==0 and mission_key==0:
            return
        self.do_mission(mission_id, mission_key)
        print('Tarefa iniciada')

    def do_first_mission(self):
        missions = self.get_missions()
        mission_id, mission_key, m = missions[0]
        if mission_id == 0 and mission_key ==0 and m ==0:
            return
        self.do_mission( mission_id, mission_key, m)
        print('Missão iniciada')

    def finish_mission(self):
        soup = self.get_soup(urls.FINISH_MISSION_PAGE)
        soup = soup.find('div', id='direita')
        st = ''
        try:
            st = soup.find('input', type='button')['onclick']
        except:
            print('Não há missão para ser resgatada')
            return
        st = st[st.index('(')+1:st.index(')')]
        mission_id = int(st[1:-1])
        data = {'i': mission_id, 'especial': 0}
        r = self.session.post(urls.FINISH_MISSION, stream=True, data=data)
        dowload_page(r, 'html_pages/FINISH_MISSION.html')
        print('Missão resgatada')

    def train_jutsus(self):
        targets = self.get_targets()
        if len(targets) == 0:
            print('Não há jutsu para ser treinado')
            return
        for target, slot in targets:
            if DEBUG:
                print('target', target)
                print('slot', slot)
            self.train_jutsu(target, slot)
        
    def get_fidelity(self):
        for i in range(7):
            data = {'day':i+1}
            r = self.session.post(urls.FIDELITY, data=data)
            response_data = r.json()
            if response_data['success']:
                print('Fidelidade dia ' + str(i+1) + ' resgatada')
                return
        print('Não foi possível resgatar fidelidade ninja')
        
    def make_contest(self): # Estudo ninja
        try:
            r = self.session.get(urls.GET_NINJA_CONTEST ,stream=True)
            dowload_page(r, 'html_pages/GET_NINJA_CONTEST.html')
            try:
                data = get_contest_ans('html_pages/GET_NINJA_CONTEST.html')
            except:
                print('Não foi possível realizar o estudo ninja')
                return
            r = s.session.post(urls.POST_NINJA_CONTEST, stream=True, data=data)
            dowload_page(r, 'html_pages/POST_NINJA_CONTEST.html')
            print('Estudo ninja realizado')
        except:
            if DEBUG:
                logging.exception('make_contest error')
    
    def start_dojo_battle(self):
        rq = self.session.get(urls.DOJO_PAGE, stream=True)
        dowload_page(rq, 'html_pages/DOJO_PAGE.html')
        rq = self.session.post(urls.CREATE_DOJO, stream=True, data={})
        dowload_page(rq, 'html_pages/CREATE_DOJO.html')
        rq = self.session.post(urls.DOJO_START, stream=True, data={'begin':1})
        dowload_page(rq, 'html_pages/DOJO_START.html')
    
    def battle(self):
        rq = self.session.get(urls.FIGTH_PAGE, stream=True)
        dowload_page(rq, 'html_pages/FIGTH_PAGE.html')
        pvp_token, moves = get_dojo_info('html_pages/FIGTH_PAGE.html')
        if len(moves) == 0:
            print('Não foi possível batalhar')
            return 
        
        action_1 = [] # ataques 
        action_2 = [] # buffs 
        action_3 = [] # habilidades de clã e portão
        action_4 = [] # vou descobrir ainda

        for move in moves:
            if move['pre']!=100:
                continue
            if move['ste']!=0:
                move['action'] = '3'
                action_3.append(move)
            elif move['st']!=0:
                move['action'] = '2'
                action_2.append(move)
            elif move['me']!=0:
                move['action'] = '4'
                action_4.append(move)
            else:
                move['action'] = '1'
                action_1.append(move)
        action_1.sort(key= lambda c : -c['id'])
        action_2.sort(key= lambda c : -c['id'])
        action_3.sort(key= lambda c : -c['id'])
        action_4.sort(key= lambda c : -c['id'])

        ping = { '_pvpToken':pvp_token }
        for move in action_3:
            data = { 'itemID': move['id'], 'action':move['action'], '_pvpToken':pvp_token }
            rq = self.session.post(urls.FIGTH_ACTION, data=data, stream=True)
            res = get_strpage(rq)
            if 'Aguardando a sua ação' in res:
                print(move['n'] + ' foi usado')
            else:
                print(res)

        buff_duration = 0
        while True:
            if buff_duration == 0 and len(action_2)>1:
                move = action_2[0]
                data = { 'itemID': str(move['id']), 'action':move['action'], '_pvpToken':pvp_token }
                rq = self.session.post(urls.FIGTH_ACTION, data=data, stream=True)
                res = get_strpage(rq)
                buff_duration = move['du']
                if 'Aguardando a sua ação' in res:
                    print('Buff ' + move['n'] + ' was used')
                else:
                    print(res)
            rq = self.session.post(urls.FIGTH_ACTION, data=ping, stream=True)
            res = get_strpage(rq)
            if 'Aguardando a sua ação' in res:
                print('Realizando ação')
                for move in action_1:
                    data = { 'itemID': str(move['id']), 'action':move['action'], '_pvpToken':pvp_token }
                    rq = self.session.post(urls.FIGTH_ACTION, data=data, stream=True)
                    res = get_strpage(rq)
                    if 'Aguardando a sua ação' in res:
                        print('ataque: ' + move['n'] + ' realizado')
                        break
                    elif 'A habilidade escolhida ainda não está disponível' in res:
                        print('ataque: ' + move['n'] + ' em cooldown')
                    elif 'Você não tem' in res and 'suficiente para usar essa técnica' in res:
                        print('Não possui chakra ou stamina para o ataque ' + move['n'])
                    elif 'A página será recarregada!' in res:
                        print('A batalha acabou')
                        return
                    else:
                        print('else')
                        print(res)
                        break
            elif 'A página será recarregada!' in res:
                print('A batalha acabou')
                return
            else:
                print(res)
            if buff_duration>0:
                buff_duration-=1
            sleep(1)