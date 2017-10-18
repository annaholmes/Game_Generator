

# http://eli.thegreenplace.net/2010/01/28/generating-random-sentences-from-a-context-free-grammar/


# TODO bugs:
'''

need collectionvars and typedvars
___ sto whatever, ___ is missing
'''
import random
import re
import string
import copy


# first option
# strings are randomly chosen from A-E
# nums randomly chosen from 0-5
# items that can have 1+ instances or 0+ instances
# instead occur once (recursion into teams was deleted)
# make new key for multiple instances of things like condact, etc
#
# to have option to make as many as u want, generate
# a new self-referential rule with the options (Null | thisRule)
# so that it could potentially create as many as needed but not
# more so
#

# make 52 card deck, 2 players on own team

class Bunch():
    # source for this class (again) >> http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/?in=user-97991

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def toString(self):
        toPrint = ""
        for k, v in self.__dict__.items():
            toPrint = toPrint + str(k) + ' ' + str(v) + ' | '
        return toPrint

'''
    need to:
        take in g4 file
        parse & clean into lists of rules
        for a recursive rule: generate new recursiveRule with options (Null | thisrule)
            so that it could potentially create more of itself
        add rules to CFG
        generate card game
            handle first section: create 52 card deck with 2 players on own team
            begin generation:
                needs to handle:
                    -scope
                    -locations
                    -players

                    eventually:
                        -variables
                        -preventing dumb stuff (moving cards in loops)



        start with limitations:
            write setup by hand (so locations are generated already)
            generate one stage game
                pass in 'STAGE'
                at option:
                    let CFG pick (e.g. 'multiaction'):

            write scoring by hand

problem: making individual parts relevant to each other.
ex: any (current player iloc HAND) 'C:
    move x top (y)
    x needs to be 'C or some other movable object in scope
    y needs to be a named location


'''

import collections

'''make table to keep track of items that
change based on scope:
    -created variables (like a collection of cards)
    -locations

'''

# make variables like a b-tree ! don't contain strings in this struct
class BTree():
    def __init__(self):
        self.vars = {}

    def startScope(self):
        # should
        self.vars = {}

    def define(self, name, type):
        b = Bunch(name=None, type=None)
        b.type = type
        if b.type == "loc":
            self.strings[name] = b
        else:
            self.vars[name] = b


    def getVar(self, type):
        b = Bunch(name=0, type=0)
        name = ''
        if type == "var" and len(self.vars) != 0:
            name = random.choice(self.vars.keys())
        elif type == "loc" and len(self.strings) != 0:
            name = random.choice(self.strings.keys())
        b = self.vars[name]
        return b.type



class CFG():
    def __init__(self):
        self.prod = collections.defaultdict(list)
        self.strings = ['STOCK', 'HAND']
        self.pcount = collections.defaultdict(int)
        self.cfactor = .05



    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))


    # TODO make this better later
    def pickString(self):

        return random.choice(string.ascii_letters).upper()


    # TODO collectionvars and typedvars

    def processCreate(self, symbol, rand_prod, dict):

        # let = varanything
        var = ''
        type = ''
        # make this smaller and only happen once thanks TODO
        if symbol == "let":
            print("is let")
            type = random.choice(['int', 'boolean', 'namegr'])

            temp = list(rand_prod)
            temp[temp.index("typed")] = type
            rand_prod = tuple(temp)

            if type not in dict.keys():
                dict[type] = []
            var = "'" + self.pickString()
            # FIX THIS...
            while var in dict[type]:
                var = self.pickString() + self.pickString()
            print("var: " + var)
            dict[type].append(var)

    # TODO how to handle recursive filters as type isn't set?
    # TODO right now can't do recursive filters
        elif symbol == "filter" or symbol == "agg":
            print("is agg")
            type = random.choice(['cstorage', 'strcollection',
                                  'cstoragecollection', "'player'",
                                  "'team'", 'whot', 'other', 'range'])

            temp = list(rand_prod)
            print('temp list' + str(temp))
            temp[temp.index("collection")] = type
            rand_prod = tuple(temp)
            print('tuple again: ' + str(rand_prod))
            #if 'collection' not in dict.keys():
            #    dict['collection'] = []

            if type == "'player'":
                if 'who' not in dict.keys():
                    dict['who'] = []
                dict['who'].append(var)
                type = 'whop'
            elif type == "'team'":
                if 'who' not in dict.keys():
                    dict['who'] = []
                dict['who'].append(var)
                type = 'whot'
            if type not in dict.keys():
                dict[type] = []
            var = "'" + self.pickString()
            # FIX THIS...
            while var in dict.keys():
                var = self.pickString() + self.pickString()
            dict[type].append(var)
            print("var: " + var)

        # TODO handle dynamically later:
        #elif symbol == "initpoints":


        self.pcount[rand_prod] += 1

        temp = list(rand_prod)
        print('before putting var:' + str(temp))
        temp[temp.index("var")] = var
        rand_prod = tuple(temp)
        #print(rand_prod)
        print("prod after var: " + str(rand_prod))

        print('var created: ' + var + "type: " + type)
        print('final prod:' + str(rand_prod))
        return rand_prod, dict
        # declare = varanything
        # irrelevant right now
        #elif symbol == "declare":
        #    pass
        # need to return dict & created var



    def get_name(self):
        i = random.randint(0, len(self.strings))
        if i == len(self.strings):
            self.strings.append(self.rand_string(5))
        return self.strings[i]

    def rand_string(self, length):
        rand_str = lambda n: ''.join([random.choice(string.ascii_uppercase) for i in range(n)])
        return rand_str(length)

    def gen_random_convergent(self,
                              symbol, dict):
        print("function called")

        """ Generate a random sentence from the
            grammar, starting with the given symbol.

            Uses a convergent algorithm - productions
            that have already appeared in the
            derivation on each branch have a smaller
            chance to be selected.

            cfactor - controls how tight the
            convergence is. 0 < cfactor < 1.0

            pcount is used internally by the
            recursive calls to pass on the
            productions that have been used in the
            branch.
        """
        sentence = ''
        rand_prod = ''
        var = ''
        print("symbol: " + symbol)
        # The possible productions of this symbol are weighted
        # by their appearance in the branch that has led to this
        # symbol in the derivation


        weights = []
        for prod in self.prod[symbol + '_']:

            if prod[0] in ["varwho", "varnamegr", "varlocnamegr",
                                                        "varcstorage",
                                                        "varwhop", "varint"]:

                if prod[0][3:] not in dict.keys():
                    weights.append(0.0)
                else:
                    print(self.pcount[prod])
                    weights.append(self.cfactor ** (self.pcount[prod]))
            elif prod in self.pcount:
                print(self.pcount[prod])
                weights.append(self.cfactor ** (self.pcount[prod]))
            else:
                weights.append(1.0)
        rand_prod = self.prod[symbol + '_'][weighted_choice(weights)]
        print("random production " + rand_prod[0])


            # pcount is a single object (created in the first call to
            # this method) that's being passed around into recursive
            # calls to count how many times productions have been
            # used.
            # Before recursive calls the count is updated, and after
            # the sentence for this call is ready, it is rolled-back
            # to avoid modifying the parent's pcount.



        var = ''

        if len(rand_prod) == 1 and rand_prod[0] in ["varwho", "varnamegr", "varlocnamegr",
                                                    "varcstorage",
                                                    "varwhop", "varint"]:

            if rand_prod[0][3:] in dict.keys():
                print(dict.keys())

                rand_prod = random.choice(dict[rand_prod[0][3:]])


        self.pcount[rand_prod] += 1


        if symbol in ["let", "agg", "initpoints", "filter"]:
            print("should make var")
            self.pcount[rand_prod] -= 1
            rand_prod, dict = self.processCreate(symbol, rand_prod, dict)



        for sym in rand_prod:
            #print("symbol: " + sym)
            if sym == 'namegr':

                sym = self.get_name()
                print("changed name: " + sym)
                sentence += sym + ' '
                #print("changed symbol (namegr): " + sym)

            # create new variables here and store them in dict in the function
            # shouldn't happen here, should happen above
            elif sym in ["let", "agg", "filter"]:

                sentence += self.gen_random_convergent(
                    sym, dict)

            # for non-terminals, recurse
            elif sym + '_' in self.prod and var == '':

                sentence += self.gen_random_convergent(
                    sym, dict)
            else:
                if sym == 'lambda' or var == 'lambda':
                    pass
                elif sym == 'varinitpoints':
                    sentence += random.choice(dict['initpoints'])
                else:
                    match = re.search("\'.+\'", sym)
                    if match:
                        sym = sym.replace("'", "")
                    #if var == '':
                    #    sentence += sym + ' '
                    #else:
                    sentence += str(sym) + ' '

            # backtracking: clear the modification to pcount
        self.pcount[rand_prod] -= 1
        return sentence

def weighted_choice(weights):
    print(weights)
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


# make tokens like game_, regular words like 'game'

def parseFile(f):
    keyValues = []
    file = open(f).read()
    rulecount = 1
    s = file.split(';')
    keyValues = []
    for i, line in enumerate(s):
        if s[i] != '':

            newline = line


            name = re.search(".*?:", newline)
            sentence = re.search(":.*", newline)

            # one or more
            if bool(re.search("\(([^)]*)\)\+\?", newline)):
                matches = re.findall("\(([^)]*)\)\+\?", newline)
                for newrule in matches:
                    newname = "rule" + str(rulecount)
                    rulecount += 1
                    newname2 = "rule" + str(rulecount)
                    rulecount += 1
                    tempsentence = newline.replace("("+newrule+")+?", newname2)
                    keyValues.append([newname2 + '_', newname + " | " + newname + " " + newname2 + " "])
                    keyValues.append([newname + '_', newrule])
                    sentence = re.search(":.*", tempsentence)
                    newline = tempsentence

            # zero or more
            if bool(re.search("\(([^)]*)\)\*\?", newline)):
                matches = re.findall("\(([^)]*)\)\*\?", newline)
                for newrule in matches:
                    newname = "rule" + str(rulecount)
                    rulecount += 1
                    newname2 = "rule" + str(rulecount)
                    rulecount += 1
                    tempsentence = newline.replace("("+newrule+")*?", newname2)
                    keyValues.append([newname2 + '_', "lambda | " + newname + " " + newname2 + " "])
                    keyValues.append([newname + '_', newrule])
                    sentence = re.search(":.*", tempsentence)
                    newline = tempsentence
            # regular parenthesis
            if bool(re.search("\(([^)]*)\)", newline)):
                matches = re.findall("\(([^)]*)\)", newline)
                for newrule in matches:
                    newname = "rule" + str(rulecount)
                    rulecount += 1
                    tempsentence = newline.replace("("+newrule+")", newname)

                    sentence = re.search(":.*", tempsentence)
                    keyValues.append([newname + '_', newrule])
                    newline = tempsentence
            # TODO handle +?, *?, + in single words



            if name and sentence:
                keyValues.append([name.group(0)[:-2] + '_', sentence.group(0)[2:]])
    return keyValues

def main():
    recycle = CFG()
    dict = {'initpoints': ["'POINTS"]}

    f = parseFile('clean_recycle.txt')
    base = open('base').read()
    scoring = open('scoring').read()
    for line in f:
        #print("Rule " + line[0] + ": " + line[1])
        #print(line[0], line[1])
        recycle.add_prod(str(line[0]), str(line[1]))
    result = recycle.gen_random_convergent('stage', dict)
    toWrite = open('/Users/anna/Desktop/cardstock/CardStockXam/games/generated2.gdl', 'w')
    for line2 in base:
        toWrite.write(line2)
    s = re.split(r"(\(.*?\))", result)
    for line in s:
        toWrite.write(line + '\n')
    for line3 in scoring:
        toWrite.write(line3)


main()





'''
# grab name
# check for (ajsdof | jl) or +? or *?
# if (sfjio) exists:
make new rule with (ajsdklf | j) as definition,
replace that instance with name of rule
# if +? exists - one or more
 generate rule - recursiveCondact

game: (multiaction | stage)+?
becomes: newrule3+?

recursive2: newrule3 | newrule3 recursive2

# if *? exists - zero or more
 generate rule (ex) for ( namegr ',' )*? -
 multNameGr : ( ' ' | multNameGr multNameGr )







'''













