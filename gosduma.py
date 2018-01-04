import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

#Создаём пустой список словарей deputies = [{'ФИО': ***, 'Год рождения': ***}, ...]
deputies = list()
#Создаём функцию depcount для заполнения deputies
def depcount (url):
    #При помощи urllib.request модуля читаем данные страницы url в строковую переменную html
    html = urllib.request.urlopen(url).read()
    #При помощи BeautifulSoup библиотеки создаём BeautifulSoup объект страницы
    global soup
    soup = BeautifulSoup(html, 'html.parser')
    #Сохраняем в переменную trtag список <tr> таблицы с информацией о депутатах на i-ую букву алфавита
    #см. 'Python.pptx' Document Object Model 1.1, слайды 5, 6
    trtags = soup.find('table', id="lists_list_elements_35")('tr')
    for trtag in trtags:
        #Пропускаем первую строку таблицы
        if trtag==trtags[0]: continue
        #Сохраняем ФИО депутата в переменную name
        name = trtag('td')[1].a.contents[0]
        #Сохраняем относительную ссылку на страницу депутата на сайте Государственной Думы в переменную href
        href = trtag('td')[1].a.get('href', None)
        urli = 'http://www.duma.gov.ru'+href
        #Читаем данные страницы депутата и создаём BeautifulSoup объект этой страницы
        htmli = urllib.request.urlopen(urli).read()
        soupi = BeautifulSoup(htmli, 'html.parser')
        #Сохраняем дату рождения в переменную dob (date of birth)
        #см. 'Python.pptx' Document Object Model 2, слайды 9-11
        dob = soupi.find('p', "deputat-info-date").contents[0]
        #При помощи re модуля находим год рождения депутата и сохраняем его в строковой переменной years
        years = re.findall('[0-9]{4}', dob)
        year = int(years[0])
        deputy = {'ФИО': name, 'Год рождения': year}
        deputies.append(deputy)
        print(deputy)

#Вызываем функцию depcount с аргументом - 
#адрес страницы сайта Государственная Дума/Состав и структура Гос. Думы/Состав Гос. Думы седьмого созыва
#http://www.duma.gov.ru/structure/deputies/
depcount ('http://www.duma.gov.ru/structure/deputies/') 

#Сохраняем в переменную alphabet список <a> c относительными сылками на страницы с информацией о депутатах на i-ую букву алфавита
#см. 'Python.pptx' Document Object Model 1.2, слайды 7, 8
alphabet = soup.find('div', "page-nave-1")('a')
for alpha in alphabet:
    #Пропускаем последний <a> 'Все'
    if alpha.contents[0]=='Все': continue
    urli = 'http://www.duma.gov.ru'+alpha.get('href', None)
    #Вызываем функцию depcount с аргументом - адрес страницы с информацией о депутатах на i-ую букву алфавита
    depcount (urli)

sum = 0
for d in deputies:
    sum = sum + d['Год рождения']

print ('Количество депутатов ГД РФ ', len(deputies))
print ('Средний возраст депутута ГД РФ ', (2017-sum/len(deputies)), ' года')
