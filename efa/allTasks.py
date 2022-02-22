import efa.artikel as artikel
import efa.partner as partner
import common.menu as m
import common.element as el



class AllTasks():
    def __init__(self):
        m.showMenuIfHidden()
        # Šifrant artiklov
        el.choose([['menu_3', 'id'], ['menu_3.1', 'id'], ['Vnos Artikla', 'xpath']])
        #menu.choose(['Šifranti', 'Artikli', 'Vnos Artikla'])
        #artikel.insert()
       # artikel.edit()
        #el.choose([['Partnerji', 'xpath'], ['menu_3.2.1', 'xpath'], ['Dodaj', 'xpath']])
        #menu.choose(['Partnerji', 'menu_3.2.1', 'Dodaj'])
        #partner.insert()


