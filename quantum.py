#! /usr/bin/env python3

import argparse
import base64
import random
import binascii


THE_WORD = "MONKEY"
rounds = 10
splitlen = 20


def hexify_string(string):
    return 'b"' + "".join(['\\x'+hex(x)[2:] for x in string]) + '"'


def gen_file(content, filename):
    content += "__obfuscator__ = 'Quantum'\n__authors__ = ('1337-sup3r-h4x0r')\n__github__ = 'https://github.com/1337-sup3r-h4x0r/QuantumObfuscator'\n__license__ = 'EPL-2.0'\n\nfrom builtins import *\n"
    content += 'Alpha = __import__\n'
    content += f'__{(THE_WORD+"_") *30}{THE_WORD} = b""\n'
    thecode = None
    with open(filename, 'r') as f:
        thecode = f.read().encode('utf-8')

    dcode_str = 'exec('
    encodings = [(base64.a85encode, "a85decode"), (base64.b16encode, "b16decode"), (base64.b32encode, "b32decode"), (base64.b64encode, "b64decode"), (base64.b85encode, "b85decode")]
    for i in range(0, rounds):
        encoding = random.choice(encodings)
        thecode = encoding[0](thecode)
        dcode_str += 'Alpha("46esab"[::-1]).' + encoding[1] + '('
    dcode_str += f'__{(THE_WORD+"_") *30}{THE_WORD}' + (')'*(rounds+1)) + '\n'

    n = len(thecode)
    slices = [thecode[max(0,i-splitlen):i] for i in range(n,0,-splitlen)]
    slices = [hexify_string(x) for x in slices]

    content += "\n".join([f'__{(THE_WORD+"_") *30}{THE_WORD} += ' + x for x in slices[::-1]]) + '\n'
    content += dcode_str

    return content


def main():
    parser = argparse.ArgumentParser(prog='QuantumObfuscator',
                                     description='The most powerful 100% \
                                                    Python obfuscator.')
    parser.add_argument('filename', help='Name of the file to obfuscate')
    args = parser.parse_args()

    content = ''

    content = gen_file(content, args.filename)

    print(content)


if __name__ == '__main__':
    main()
