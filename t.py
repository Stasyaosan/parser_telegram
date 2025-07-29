a = [5,6,1,2]
for index, i in enumerate(a):
    print(index)

b = ['.png']
print('|'.join(b))
import re


q = 'https://cdn4.cdn-telegram.org/file/ZGJZRs_augTmqtibZaG2oe9ZfXQAcILzrwTzOfDJGD9q4pT7RJmtCIecJvgURMo5sFgs5KYUeBdXCLUq-IBx98N-Cfzi5pmc07rHHEpKlYSZzH1hNhwUNDzLlfTtkPMHJ-woksXaaQhDtTBpQ4Gy95HL7kgupxoJTJ93X4TPEOTmPWwLMxlKGMLw9TK-wvy5eI0Orx7z2v4Sj5p8_0KAYOEkxo27fYmWbkuyJ7z6y2GKMeVLF9ibluAfkZMMuSzSkcfh5q5m9ntoRPEYxfKORVeoqs08iQR0JiavnmFs5VdhJEOu1-3jxXcOyV6gq7U_JnzFm23I45NJBRaJrWcjUA.jpg'
print(len(q))
pattern = r'https.*\.(?:jpg|png)'
print(re.findall(pattern, q))


print(f'{1:1f}')