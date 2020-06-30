import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''
dirr = True
args = sys.argv
if dirr:
    try:
        os.mkdir(args[1])
    except FileExistsError:
        print("Directory already exists")
    dirr = False
# write your code here
list_of_pages = set()
stack = deque()
stop_on = True
while stop_on:
    page = input('> ')
    if '.' not in page and page not in list_of_pages and page != 'exit' and page != 'back':
        print('Error: Incorrect URL')
    elif page[-3] == '.' or page[-4] == '.':
        if page.startswith('https'):
            r = requests.get(page)
            ind = page.rfind('.')
            ind2 = page.find('/')
            list_of_pages.add(page[ind2 + 2:ind])
            soup = BeautifulSoup(r.text, 'html.parser')
            tags_h = soup.find_all(('p', 'a', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'))
            txt = ''
            for z in tags_h:
                if z.has_attr('href'):
                    txt += Fore.BLUE + z.text
                    print(Fore.BLUE + z.text)
                else:
                    txt += z.text
                    print(z.text)
            with open(f'{args[1]}/{page[ind2 + 2:ind]}.txt', 'w', encoding='utf-8') as file:
                print(txt, file=file)
        else:
            page = 'https://' + page
            r = requests.get(page)
            ind = page.rfind('.')
            ind2 = page.find('/')
            list_of_pages.add(page[ind2 + 2:ind])
            soup = BeautifulSoup(r.text, 'html.parser')
            tags_h = soup.find_all(('p', 'a', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'))
            txt = ''
            for z in tags_h:
                if z.has_attr('href'):
                    txt += Fore.BLUE + z.text
                    print(Fore.BLUE + z.text)
                else:
                    txt += z.text
                    print(z.text)
            with open(f'{args[1]}/{page[ind2 + 2:ind]}.txt', 'w', encoding='utf-8') as file:
                print(txt, file=file)
    elif page in list_of_pages:
        with open(f'{args[1]}/{page}.txt', 'r', encoding='utf-8') as file:
            red = file.read()
            print(red)
    elif page == 'back' and len(stack) > 0:
        stack.pop()
        back_page = stack.pop()
        with open(f'{args[1]}/{back_page}.txt', 'r', encoding='utf-8') as file:
            red = file.read()
            print(red)
    elif page == 'exit':
        stop_on = False
