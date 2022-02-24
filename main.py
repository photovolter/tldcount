from domainnames import tldlist
import requests
import re

# cleantest = re.compile('<.*?>|- ')
# Zmienna będzie wykorzystana do wyczyszczenia tagów HTML i usunięcia wiodących znaków - (minus).
# Zapis ('<.*?>|- ') oznacza: weź wzorzec regex "<.*?>" lub "- ".
# re.compile oznacza kompilację wzorca do obiektu regex, który będzie później wykorzystany w innych funkcjach.

orangutan = 'https://zajecia-programowania-xd.pl/flagi'
surowe_info = requests.get(orangutan)
text = surowe_info.text
cleantest = re.compile('<.*?>|- ')
efekt = text.rsplit('</p>')
letterslist = 'abcdefghijklmnopqrstuvwxyz'

def listToString(listjoin):
    return (''.join(listjoin))


# Funkcja maxstr wykorzystuje wbudowane funkcje min i max do znalezienia najdłuższego i najkrótszego elementu na liście.

def maxstr(tocheck):
    maxlen = max(tocheck, key=len)
    minlen = min(tocheck, key=len)
    return [minlen, maxlen]


# Funkcja splittld.
# FQDN - pełna nazwa domenowa. Np www.onet.pl lub www.moja.domena.com.pl
# splitted - lista elementów FQDN powstała po podziale w miejscu kropki - ['www', 'onet', 'pl'], ['www', 'moja', 'domena', 'com', 'pl']
# myjoin - sklejony ostatni i przedostatni człon FQDN - onet.pl, com.pl
# tld - ostatni człon FQDN - pl
# Funkcja zwraca listę 2 wartości, np: ['onet', 'pl'] lub ['com', 'pl']

def splittld(tosplit):
    splitted = tosplit.split('.')
    myjoin = splitted[-2] + '.' + splitted[-1]
    tld = splitted[-1]
    return [myjoin, tld]


# Funkcja validateDomain. Argumentem jest domniemana nazwa domeny
# Funkcja zwróci wartoś false jeżeli ciąg znaków jest pusty lub nie pasuje do wzorca.
# W pozostałych przypadkach zwróci wartość true.
#
# 1. Wyrażenie regularne sprawdzające czy ciąg znaków jest domeną.
# 2. Kompilacja wyrażenia regularnego w celu jego późniejszego użycia.
# 3. Sprawdzamy czy string nie jest pusty, zwracamy false, jeżeli jest.
# 4. Użycie mudułu Pythona re (regex) w celu dopasowania ciągu znaków do wzorca.

def validateDomain(domainname):
    regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
    p = re.compile(regex)
    if domainname is None:
        return False
    if re.search(p, domainname):
        return True
    else:
        return False


newefekt = []


# Teraz już z górki
# Iterujemy sobie po naszej liści, która powstała w wyniku text.rsplit('</p>')
# 1. Każdą linię czyścimy z tagów HTML i śmieci w postaci myślników.
# 2. Sprawdzamy, czy ta już oczyszczona linia pasuje do wzorca domeny.
# 4. Jeżeli pasuje do wzorca, to wrzucamy ją na nową listę. W ten sposób powstaje wyłącznie lista domen.

for i, linia in enumerate(efekt):
    efekt[i] = re.sub(cleantest, '', linia)
    if validateDomain(efekt[i]):
        newefekt.append(efekt[i])



stringfromlist = listToString(newefekt).lower()
lettersdict = {}
for letter in letterslist:
    lettersdict[letter] = stringfromlist.count(letter)


# W następnych 2 liniach wykorzystano mechanizm List Comprehension.
# Jest to inna metoda zapisu pętli for.
sumapl = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] not in tldlist and splittld(s)[1]=='pl')
sumapltld = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] in tldlist)

print()
print(f"Flagi w domenie pl, bez domeny drugiego poziomu: {sumapl}")
print(f"Flagi w domenie pl z domeną drugiego poziomu: {sumapltld}")
print()
print(f"Najkrótsza nazwa domeny: {maxstr(newefekt)[0]}")
print(f"Najkrótsza nazwa domeny: {maxstr(newefekt)[1]}")
print()
print('Liczebność znaków alfabetu:')
[print(key,':',value) for key, value in lettersdict.items()]
