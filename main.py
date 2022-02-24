from domainnames import tldlist
import requests
import re

orangutan = 'https://zajecia-programowania-xd.pl/flagi'
surowe_info = requests.get(orangutan)
text = surowe_info.text
cleantest = re.compile('<.*?>|- ')
efekt = text.rsplit('</p>')


def splittld(tosplit):
    splitted = tosplit.split('.')
    myjoin = splitted[-2] + '.' + splitted[-1]
    tld = splitted[-1]
    return [myjoin, tld]


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

for i, linia in enumerate(efekt):
    efekt[i] = re.sub(cleantest, '', linia)
    if validateDomain(efekt[i]):
        newefekt.append(efekt[i])


sumapl = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] not in tldlist and splittld(s)[1]=='pl')
sumapltld = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] in tldlist)
print(f"Flagi w domenie pl, bez domeny drugiego poziomu: {sumapl}")
print(f"Flagi w domenie pl z domeną drugiego poziomu: {sumapltld}")

