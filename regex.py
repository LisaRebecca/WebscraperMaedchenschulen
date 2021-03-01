import re

wikilink = re.compile('/wiki/|/w/')
found = wikilink.search('/w/index.php?title=St.-Theresien-Gymnasium&action=edit&redlink=1')
print(found)

# source_annotation = re.compile('\[ [0-9]* \]')
# string = 'Staatliche Sophie-Scholl-Realschule für Mädchen [68]'
res = re.split(r' \[', 'Staatliche Sophie-Scholl-Realschule für Mädchen [68]')
print(res)