from domainnames import tldlist
import requests
import re

flagsurl = 'https://zajecia-programowania-xd.pl/flagi'
rawdata = requests.get(flagsurl)
text = rawdata.text
cleantext = re.compile('<.*?>|- |:(.*)+|/(.*)+')
urlslist = text.rsplit('</p>')
letterslist = 'abcdefghijklmnopqrstuvwxyz.'


def by_size(words, size):
    return [word for word in words if len(word) == size]


def maxstr(tocheck):
    maxlen = max(tocheck, key=len)
    minlen = min(tocheck, key=len)
    return [minlen, maxlen]


def splittld(tosplit):
    splitted = tosplit.split('.')
    myjoin = splitted[-2] + '.' + splitted[-1]
    tld = splitted[-1]
    return [myjoin, tld]


def validatedomain(domainname):
    regex = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" + "+[A-Za-z]{2,6}"
    p = re.compile(regex)
    if domainname is None:
        return False
    if re.search(p, domainname):
        return True
    else:
        return False


newefekt = []
for i, linia in enumerate(urlslist):
    urlslist[i] = re.sub(cleantext, '', linia)
    if validatedomain(urlslist[i]):
        newefekt.append(urlslist[i])


lettersdict = {}
for letter in letterslist:
    lettersdict[letter] = str(newefekt).lower().count(letter)

sumapl = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] not in tldlist and splittld(s)[1]=='pl')
sumapltld = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] in tldlist)
sumanotpl = sum(1 for i, s in enumerate(newefekt) if splittld(s)[0] not in tldlist and splittld(s)[1]!='pl')

shortestdomainsize = len(maxstr(newefekt)[0])
longestdomainsize = len(maxstr(newefekt)[1])
shortestdomain = by_size(newefekt, shortestdomainsize)
longestdomain = by_size(newefekt, longestdomainsize)

print()
print(f"Flagi w domenie pl, bez domeny drugiego poziomu: {sumapl}")
print(f"Flagi w domenie pl z domeną drugiego poziomu: {sumapltld}")
print(f"Flagi poza domeną pl: {sumanotpl}")
print()
print(f"Najkrótsza nazwa domeny: {shortestdomainsize} znaków")
print(*shortestdomain)
print(f"Najdłuższa nazwa domeny: {longestdomainsize} znaków")
print(*longestdomain)
print()
print('Liczebność znaków alfabetu:')

[print(key,':',value) for key, value in lettersdict.items()]
