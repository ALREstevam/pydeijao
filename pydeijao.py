import requests as reqs
from bs4 import BeautifulSoup as bs, Comment
import examplehtml

isExample = False

class Pydeijao:
    def __init__(self):
        print('Starting Pydeijão...')
        self.encoding = 'utf-8'
        self.link = 'http://www.pfl.unicamp.br/Rest/view/site/cardapio.php'
        self.soup = ''
        print('\tDone.\n')

        print('Using the sample html file:\n\t{:s}.\n'.format(str(isExample)))

        self.run()
        input()

    def run(self):
        print('Accessing the page...')
        self.soup = self.loadPage(self.link)
        print('\tDone.\n')
        comments = self.soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        self.soup = self.soup.find_all('tr')

        if not self.verifyValid()[0]:
            print('\n{:s}'.format(self.getDecorator(50)))
            print('| /!\ The menu could not be loaded.\n'
                  '| The page says: {}'.format(self.verifyValid()[1]), end='')
            print('\n{:s}'.format(self.getDecorator(50)))
            input()
            exit(0)

        else:
            self.printSpace()

            print(self.getDecorator(53) + '\n')

            title = self.extractTitle()
            date = self.extractDay()

            print('\t' + self.extractType()[0])
            print('{:^50s}'.format(title).upper())
            print('{:^50s}'.format(date[0]))
            print('{:^50s}'.format(date[1]))

            lunch = self.extractMenuLunch()

            print()
            print(self.getDecorator(53))
            for meat in lunch:
                print('| {:>23s} : {:<23s} |'.format(meat[0], meat[1]))
            print(self.getDecorator(53))

            obss = self.extractObservations()

            print('{:s}: {:s}'.format(obss[0], obss[1]))

    def loadPage(self, link):
        try:
            if isExample:
                soup = bs(examplehtml.exampleHtml, 'html.parser')
            else:
                page = reqs.get(link)
                soup = bs(page.content, 'html.parser', from_encoding='iso-8859-1')
            return soup
        except:
            print('\n' + self.getDecorator(50))
            print('| /!\ The page could not be loaded,\n| verify your internet connection.')
            print(self.getDecorator(50))
            input()
            exit(0)


    def extractDay(self):
        daystr = self.soup[0].getText()
        #daystr = daystr.strip()
        baseList = daystr.split(' - ')
        return baseList[1].strip().split(' ')

    def extractTitle(self):
        tstr = self.soup[0].getText()
        tlst = tstr.split(' - ')
        return tlst[0].strip()


    def verifyValid(self):
        verifyStr = self.soup[4].getText().strip()
        return [not verifyStr == 'NÃO HÁ CARDÁPIO CADASTRADO!', verifyStr]


    def extractMenuLunch(self):
        lst = self.soup[3].getText().split('\n')
        newlst = []

        for elem in lst:
            if elem != '' and elem != '\n':
                newlst.append(elem)

        rsp = []
        rsp.append(['PEDREIRAGEM', newlst[0]])

        for elem in newlst[1:7]:
            tupelem = elem.split(':')

            tupelem[0] = tupelem[0].strip()
            tupelem[1] = tupelem[1].strip()

            rsp.append(tupelem)

        # newlst[7] = newlst[7].replace(':', '')
        # newlst[8] = newlst[8].strip()
        # rsp.append([newlst[7], newlst[8]])

        return rsp

    def extractType(self):
        lst = self.soup[2].getText().replace('\n\n\n\n', '').split()
        return lst

    def extractObservations(self):
        lst = self.soup[3].getText().split('\n')
        newlst = []

        for elem in lst:
            if elem != '' and elem != '\n':
                newlst.append(elem)

        newlst[7] = newlst[7].replace(':', '')
        newlst[8] = newlst[8].strip()
        return [newlst[7], newlst[8]]

    def getDecorator(self, size):
        return '+' + ('-' * (size - 2)) + '+'

    def printSpace(self):
        print('\n'*5)

p = Pydeijao()
