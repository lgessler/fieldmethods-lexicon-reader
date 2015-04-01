#Luke Gessler
# February 4, 2015
# Linguistic Field Methods
# ANTH 5401, UVa Spring 2015
import os
import sys

#declare Word class 
class Word:
    def __init__(self,forms,meanings,tags=[]):
        self.forms = forms
        self.meanings = meanings
        self.tags = tags
    def __repr__(self):
        return "\nForms   : \t"+','.join(self.forms)+"\n"+    \
               "Meanings: \t"+','.join(self.meanings)+"\n"+ \
               "Tags    : \t"+','.join(self.tags)+"\n"

#declare Lexicon class
class Lexicon:
    def __init__(self,lexicon):
        self.lexicon = lexicon

    def __repr__(self):
        return ''.join(map(repr,self.lexicon))

    def tag(self,tag):
        return [item for item in \
                filter(lambda x: tag in ''.join(x.tags),self.lexicon)]

    def form(self,form):
        return [item for item in \
                filter(lambda x: form in ''.join(x.forms),self.lexicon)]

    def meaning(self,meaning):
        return [item for item in \
                filter(lambda x: meaning in ''.join(x.meanings),self.lexicon)]

#remove comments
def uncomment(s):
    comment = None
    if s.find('#') != -1:
        s = s[:s.find('#')]
        comment = s[s.find('#')+1:]
    return s,comment

def generate_lexicon(filename='sessions/cumulative.txt'):
    with open(filename) as f:
        lines = [line.strip() for line in f]

    #will store Word objects
    lexicon = []
    currtag = None
    just_glossed = False
    from time import sleep
    for i in range(len(lines)):
        line = lines[i]
        if line == '' or line[0] == '#':       #skip empty lines
            continue
        elif just_glossed:   #skip the gloss line if it was handled below
            just_glossed = False
            continue
        elif line[0] == '#':   #skip comments
            continue
        elif line[0] == '@':   #extract tags
            currtag = line[1:]
            continue
        elif len(lines[i+1]) > 0 and lines[i+1][0]=="'": #a word will always be glossed with '
            forms = line.split(',')
            glosses,comment = uncomment(lines[i+1])
            meanings = glosses.replace("'","").split(',')
            tags = [currtag]
            lexicon = lexicon[:] + [Word(forms,meanings,tags)]
            just_glossed = True
        else:
            print("ERROR: poorly-formatted string near line %s" % (i+1))
            sys.exit(1)
    return Lexicon(lexicon)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        lexicon = generate_lexicon()
        print "Loaded default file successfully."
        while True:
            s = raw_input()
            if 'form' in s:
                print lexicon.form(s[s.find(' ')+1:])
            elif 'meaning' in s:
                print lexicon.meaning(s[s.find(' ')+1:])
            elif 'tag' in s:
                print lexicon.tag(s[s.find(' ')+1:])
            else:
                sys.exit(1)
    else:
        lexicon = generate_lexicon(sys.argv[1])
