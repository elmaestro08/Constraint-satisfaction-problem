import random,copy,operator
from collections import OrderedDict
clauses = []
clauses_pl = []
num_tables,num_people = 0,0
def readfile_and_process():
    global clauses,clauses_pl,num_people,num_tables
    with open('input.txt','r') as f:
        contents = f.read().strip().split('\n')
    num = contents[0].strip().split(' ')
    num_tables = int(num[0])
    num_people = int(num[1])
    for person in range(int(num[0])):
        y = []
        for table in range(int(num[1])):
            y.append('x'+str(person+1)+'-'+str(table+1))
        clauses.append(y)
    for person in range(int(num[0])):
        for table in range(int(num[1])):
            for k in range(table+1,int(num[1])):
                y = []
                y.append('~x'+str(person+1)+'-'+str(table+1))
                y.append('~x' + str(person + 1) +'-'+ str(k + 1))
                clauses.append(y)
    for line in contents[1:]:
        words = line.strip().split(' ')
        if words[2] == 'F':
            for table in range(int(num[1])):
                for k in range(table + 1, int(num[1])):
                    if table != k:
                        y= []
                        y.append('~x' + str(words[0]) + '-'+str(table + 1))
                        y.append('~x' + str(words[1]) +'-'+ str(k + 1))
                        clauses.append(y)
                        y = []
                        y.append('~x' + str(words[0]) +'-'+ str(k + 1))
                        y.append('~x' + str(words[1]) +'-'+ str(table + 1))
                        clauses.append(y)
        elif words[2] == 'E':
            for table in range(int(num[1])):
                y = []
                y.append('~x'+str(words[0]) +'-'+ str(table+1))
                y.append('~x' + str(words[1]) +'-'+ str(table + 1))
                clauses.append(y)
    clauses_pl = copy.deepcopy(clauses)

def PL_resolution():
    new = []
    while True:
        for i in range(len(clauses_pl)):
            for j in range(i+1,len(clauses_pl)):
                resolvents = PL_resolve(clauses_pl[i],clauses_pl[j])
                #print resolvents
                if [] in resolvents:
                    return False
                for item in resolvents:
                    if item not in new:
                        new.append(item)
        if set(tuple(x) for x in new).issubset(set(tuple(x) for x in clauses_pl)):
            return True
        for item in new:
            if item not in clauses_pl:
                clauses_pl.append(item)

def PL_resolve(clause1,clause2):
    resolvent = []
    #print clause1,clause2
    for term in clause1:
        if term[0] == '~':
            compare_str = term[1:]
        else:
            compare_str = '~'+term
        if compare_str in clause2:
            no_term1 = [x for x in clause1 if x!=term]
            no_term2 = [x for x in clause2 if x!=compare_str]
            resolvent.append(no_term1+no_term2)
    return resolvent

def get_model():
    model = {}
    for person in range(num_tables):
        for table in range(num_people):
            model['x'+str(person+1)+'-'+str(table+1)] = bool(random.getrandbits(1))
    return model

'''def pl_true(clause,model):
    for literal in clause:
        if literal[0] == '~':
            if model[literal[1:]] == False:
                return True
        else:
            if model[literal] == True:
                return True
    return False'''

def pl_true(clause,model):
    for literal in clause:
        if literal[0] == '~':
            if literal[1:] in model:
                if model[literal[1:]] == False:
                    return True
            else:
                return None
        else:
            if literal in model:
                if model[literal] == True:
                    return True
            else:
                return None

    return False


def prop_symbols(clause):
    symbols = []
    for literal in clause:
        symbols.append(literal[1:] if literal[0] == '~' else literal)
    return symbols

def WalkSAT():
    model = get_model()
    while True:
        satisfied,unsatisfied = [],[]
        for clause in clauses:
            (satisfied if pl_true(clause,model) else unsatisfied).append(clause)
        if not unsatisfied:
            return model
        clause = random.choice(unsatisfied)
        if random.uniform(0.0,0.1)<0.5:
            symbol = random.choice(prop_symbols(clause))
        else:
            maxclause = {}
            symbol_list = prop_symbols(clause)
            for literal in symbol_list:
                new_model = copy.deepcopy(model)
                new_model[literal] = not new_model[literal]
                count = 0
                for c in clauses:
                    if pl_true(c,new_model) == True:
                        count += 1
                maxclause[literal] = count
            symbol = max(maxclause.iteritems(),key = operator.itemgetter(1))[0]
        model[symbol] = not model[symbol]
    return None


def DPLL_Satisfiable():
    symbols = list(set((sym for clause in clauses for sym in prop_symbols(clause))))
    return DPLL(clauses,symbols,{})

def find_pure_symbol(symbols,clauses):
    flagp,flagn = False,False
    for s in symbols:
        for clause in clauses:
            if not flagp and s in clause:
                flagp = True
            if not flagn and '~'+s in clause:
                flagn = True
        if flagp!=flagn:
            return s,flagp
    return None,None

def DPLL(clauses,symbols,model):
    blank_clauses = []
    for clause in clauses:
        val = pl_true(clause,model)
        if val is False:
            return False
        if val is not True:
            blank_clauses.append(clause)
    if not blank_clauses:
        return model
    P,value = find_pure_symbol(symbols,blank_clauses)
    if P:
        model[P] = value
        symbols.remove(P)
        return DPLL(clauses,symbols,model)
    P, value = find_unit_clause(clauses, model)
    if P:
        model[P] = value
        symbols.remove(P)
        return DPLL(clauses,symbols,model)
    symbols1 = copy.deepcopy(symbols)
    P ,symbols= symbols[0],symbols[1:]
    #Rest = symbols[1:]
    a = {}
    b = {}
    a[P] = True
    b[P] = False
    model1 = copy.deepcopy(model)
    model.update(a)
    model1.update(b)
    return (DPLL(clauses,symbols,model)or DPLL(clauses,symbols1,model1))



def find_unit_clause(clauses,model):
    #print model
    for clause in clauses:
        #print str('a'+str(clause))
        P, value = abc(clause,model)
        #print str('b'+str(P)+str(value))
        if P:
            return P,value
    return None,None


def abc(clause,model):
    P,val = None,None
    for literal in clause:
        symbol,value = ret_sym_value(literal)
        #print symbol,value,model
        if symbol in model:
            if model[symbol] == value:
                return None,None
        elif P:
            #print 'h'
            return None,None
        else:
            #print 'j'
            P,val = symbol,value
    return P,val


def ret_sym_value(literal):
    if literal[0] == '~':
        return literal[1:],False
    else:
        return literal,True


def print_op(model):
    dict = {}
    for k,v in model.iteritems():
        if v:
            val = k[1:].split('-')
            dict[int(val[0])] = int(val[1])
    sorted_model = OrderedDict(sorted(dict.items(), key=lambda x: x[0]))
    return sorted_model










def main():
    file_op = []
    readfile_and_process()
    '''if PL_resolution():
        print 'yes'
        model = WalkSAT()
        print_op(model)
        #print model
    else:
        print 'no'
    #model = WalkSAT()
    #print_op(model)
    #'''
    model = DPLL_Satisfiable()
    if model:
        file_op.append('yes\n')
        sorted_model = print_op(model)
        for k, v in sorted_model.iteritems():
            str1 = str(k)+' '+str(v)+'\n'
            file_op.append(str1)
    else:
        file_op.append('no')

    with open("output.txt", "w+") as f:
        f.write("".join(file_op))


if __name__ == '__main__':
    main()