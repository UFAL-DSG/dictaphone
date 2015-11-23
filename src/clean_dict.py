#!/usr/bin/env python3

import argparse

cmu2ipa = [
    ('EH', 'ɜə'),
    ('AH', 'ə'),
    ('EY', 'eı'),
    ('IY', 'ı'),
    ('EY IH', 'ei'),
    ('AW', 'aʋ'),
    ('AA', 'ɒ'),
    ('TH', 'ɵ'),
    ('AW', 'ʋ'),
    ('Z', 'z'),
    ('EH', 'e'),

    ('AA', 'ɑ'),
    ('AE', 'æ'),
    ('AH', 'ʌ'),
    ('AO', 'ɔ'),
    ('AW', 'aʊ'),
    ('AY', 'aɪ'),
    ('B', 'b'),
    ('CH', 'tʃ'),
    ('D', 'd'),
    ('DH', 'ð'),
    ('EH', 'ɛ'),
    ('ER', 'ɚ'),
    ('EY', 'eɪ'),
    ('F', 'f'),
    ('G', 'g'),
    ('HH', 'h'),
    ('IH', 'ɪ'),
    ('IY', 'i'),
    ('JH', 'dʒ'),
    ('K', 'k'),
    ('L', 'l'),
    ('M', 'm'),
    ('N', 'n'),
    ('NG', 'ŋ'),
    ('OW', 'oʊ'),
    ('OY', 'ɔɪ'),
    ('P', 'p'),
    ('R', 'r'),
    ('S', 's'),
    ('SH', 'ʃ'),
    ('T', 't'),
    ('TH', 'θ'),
    ('UH', 'ʊ'),
    ('UW', 'u'),
    ('V', 'v'),
    ('W', 'w'),
    ('Y', 'j'),
    ('Z', 's'),
    ('ZH', 'ʒ'),

    ('ER', 'ɜ R'),
    ('IE', 'a IY'),
    ('OW', 'AH ʋ'),
    ('OW', 'o UW'),
    ('AW', 'a UW'),
    ('AE S', 'a S'),
    ('AH R', 'a R'),
    ('AE', 'a:'),
    ('AE', 'aː'),
    ('AH S', 'ac'),
    ('ER', 'ɜ: R'),
    ('ER', 'ɜː R'),
    ('R AA N', 'R o N'),
    ('AE', 'a'),
    ('AH', 'o'),
    ('IH', 'y'),
    ('K S', 'c S'),
    ('', 'ː'),
    ('', '\''),
    ('', 'ˌ'),
    ('', 'ˈ'),
    ('', ':'),
    ('', ','),
]


def ipa2ascii(i):
    a = i.lower()
    for cmu, ipa in cmu2ipa:
        a = a.replace(ipa, ' ' + cmu + ' ').replace('   ', ' ').replace('  ', ' ')

    return a


def clean(fn_i, fn_o):
    phonetic_set = set()

    with open(fn_i, 'rt', encoding='utf8') as i:
        with open(fn_o, 'wt', encoding='utf8') as o:
            for l in i:
                l = l.strip()
                if '<' in l or '>' in l:
                    continue

                if '\t' in l:
                    # if tabs are used then word cannot contain any blanks (spaces)

                    w, p = l.split('\t')

                    if ' ' in w:
                        # skip multi-word entries
                        continue

                    p = ipa2ascii(p.strip()).strip()

                    phonetic_set.update(set(p.split(' ')))

                    n = w + '\t' + p
                else:
                    w, p = l.split(' ', maxsplit=1)
                    p = ipa2ascii(p.strip()).strip()

                    phonetic_set.update(set(p.split(' ')))

                    n = w + '\t' + p

                for c in ['a', 'ac', 'co', 'c', ',', 'o', 'y', 'ɜ', '-->', '<!--']:
                    # print(set(p.split(' ')))
                    if c in set(p.split(' ')):
                        print(l)
                        print(n)
                        print('')

                n = n.upper()

                for c, r in [('‐', '-'),]:
                    n = n.replace(c, r)

                o.write(n)
                o.write('\n')


    return phonetic_set

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
    Filter the dictionary items so that thy are suitable for an ASR system.

    """)

    parser.add_argument('input', action="store", help='a file with input dictionary')
    parser.add_argument('output', action="store", help='a file for the output dictionary')

    args = parser.parse_args()

    phonetic_set = clean(args.input, args.output)

    print('Phonetic alphabet of the cleaned dictionary')
    for p in sorted(phonetic_set):
        print(p, sep=' ', end=' ')

    print('')
    print('')
