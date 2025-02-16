import re
import sys

def tokenize_string(s: str):
    return re.findall(r'and|[\w#]+|[(),\[\]|:=.]', s)

def create_grammar() -> dict:
    no_terminals = [
        "S", "INSTRUCTION", "COMMAND", "J_fun", "G_fun", "INTEGER",
        "VARIABLE_DEFINITION", "STRINGS", "STRING", "PROCEDURE_DEFINITION",
        "PARAMS", "NEXT_PARAM", "PARAM", "VALUE", "PROCEDURE_CALL", "BLOCK",
        "INSTRUCTIONS", "INSTRUCTION", "VARIABLE_ASSIGNMENT", "GOTO", "N",
        "D", "O", "X", "VARIABLE", "TOTHE", "INDIR", "OFTYPE", "MOVE", "TURN",
        "FACE", "PUT", "PICK", "JUMP", "NOP", "CONDITIONAL", "LOOP",
        "REPEAT_TIMES", "CONDITION", "FACING", "CANPUT", "CANPICK", "CANMOVE",
        "CANJUMP", "NOT"
    ]
    
    #Estructura para guardar variables y procedimientos creados
    vars = {}
    procs = {}
    
    terminals = [
        "|", "(", ")", "[", "]", ":", ".", ";", "=",
        "M", "R", "C", "B", "c", "b", "P", "J", "G",
        "$$$vars", "$$$procs", "int", "str", "proc", "and", "goTo", "with",
        "#front", "#right", "#left", "#back", "#north", "#south", "#west", "#east",
        "#balloons", "#chips", "toThe", "inDir", "ofType", "move", "turn", "face",
        "put", "pick", "jump", "nop", "if", "then", "else", "while", "do", "for",
        "repeat", "facing", "canPut", "canPick", "canMove", "canJump", "not"
    ]
    
    initial_element = 'S'
    
    production_rules = {
        "S": [ ["BLOCK", "S"], ["VARIABLE_DEFINITION", "S"], ["PROCEDURE_DEFINITION", "S"], ["VARIABLE_ASSIGNMENT", "S"], ["PROCEDURE_CALL", "S"], []],
        "INSTRUCTION_O": [["COMMAND", ";"]],
        "COMMAND": [["M"], ["R"], ["C"], ["B"], ["c"], ["b"], ["P"], ["J_fun"], ["G_fun"], []],
        "J_fun": [["J", "(", "INTEGER", ")"]],
        "G_fun": [["G", "(", "INTEGER", ",", "INTEGER", ")"]],
        "INTEGER": [["int"]],
        "VARIABLE_DEFINITION": [["|", "STRINGS", "|"]],
        "STRINGS": [["STRING", "STRINGS"], []],
        "STRING": [["str"]],
        "PROCEDURE_DEFINITION": [["proc", "PARAMS", "BLOCK"]],
        "PARAMS": [["PARAM", "NEXT_PARAM"],["STRING"], []],
        "NEXT_PARAM": [["and", "PARAM", "NEXT_PARAM"], []],
        "PARAM": [["STRING", ":", "VALUE"]],
        "VALUE": [["INTEGER"], ["STRING"]],
        "PARAMS_CALL": [["PARAM_CALL", "NEXT_PARAM_CALL"], []],
        "NEXT_PARAM_CALL": [["and", "PARAM_CALL", "NEXT_PARAM_CALL"], []],
        "PARAM_CALL": [["STRING", ":", "N"]],
        "BLOCK": [["[", "INSTRUCTIONS", "]"]],
        "INSTRUCTIONS": [["INSTRUCTION", "INSTRUCTIONS"], []],
        "INSTRUCTION": [
            ["VARIABLE_DEFINITION"], ["VARIABLE_ASSIGNMENT"], ["PROCEDURE_CALL"],
            ["CONDITIONAL"], ["LOOP"],["GOTO"], ["MOVE"], ["TURN"],
            ["FACE"], ["PUT"], ["PICK"], ["JUMP"], ["NOP"]
        ],
        "VARIABLE_ASSIGNMENT": [["$$$vars", ":", "=", "VALUE", "."]],
        "GOTO": [["goTo", ":", "N", "with", ":", "N", "."]],
        "N": [["VARIABLE"], ["INTEGER"]],
        "D": [["#front"], ["#right"], ["#left"], ["#back"]],
        "O": [["#north"], ["#south"], ["#west"], ["#east"]],
        "X": [["#balloons"], ["#chips"]],
        "VARIABLE": [["$$$vars"]],
        "TOTHE": [["toThe", ":", "D"]],
        "INDIR": [["inDir", ":", "O"]],
        "OFTYPE": [["ofType", ":", "X"]],
        "MOVE": [["move", ":", "N", "."], ["move", ":", "N", "TOTHE", "."], ["move", ":", "N", "INDIR", "."]],
        "TURN": [["turn", ":", "D", "."]],
        "FACE": [["face", ":", "O", "."]],
        "PUT": [["put", ":", "N", "OFTYPE", "."]],
        "PICK": [["pick", ":", "N", "OFTYPE", "."]],
        "JUMP": [["jump", ":", "N", "TOTHE", "."], ["jump", ":", "N", "INDIR", "."]],
        "NOP": [["nop", "."]],
        "CONDITIONAL": [["if", ":", "CONDITION", "then", ":", "BLOCK", "else", ":", "BLOCK"]],
        "LOOP": [["while", ":", "CONDITION", "do", ":", "BLOCK"]],
        "REPEAT_TIMES": [["for", ":", "N", "repeat", ":", "BLOCK"]],
        "CONDITION": [["FACING"], ["CANPUT"], ["CANPICK"], ["CANMOVE"], ["CANJUMP"], ["NOT"]],
        "FACING": [["facing", ":", "O", "."]],
        "CANPUT": [["canPut", ":", "N", "OFTYPE", "."]],
        "CANPICK": [["canPick", ":", "N", "OFTYPE", "."]],
        "CANMOVE": [["canMove", ":", "N", "INDIR", "."], ["canMove", ":", "N", "TOTHE", "."]],
        "CANJUMP": [["canJump", ":", "N", "INDIR", "."], ["canJump", ":", "TOTHE", "."]],
        "NOT": [["not", ":", "CONDITION"]],
        "PROCEDURE_CALL": [], #Aquí se guardará el no terminal de cada procedimiento creado
    }
    
    g = {
        'no_terminals':no_terminals,
        'terminals':terminals,
        'initial_element':initial_element,
        'production_rules':production_rules,
        'vars': vars,
        'procs':procs
        }
    
    return g

grammar = create_grammar()

def match_token(token: str, expected: str) -> bool:

    if expected == '$$$vars':
        return token in grammar["vars"]
    elif expected == '$$$procs':
        return token in grammar["procs"]
    elif expected == "int":
        return token.isdigit()
    elif expected == "str":
        return token.isalpha()
    else:
        return token == expected
    
def create_vars(tokens):
    for tok in tokens:
        if tok not in grammar["vars"]:
            grammar["vars"][tok] = None
        else:
            return False
    return True

def set_var(name, value):
    if name in grammar["vars"]:
        grammar["vars"][name] = value
        return True
    return False

def create_procedure(tokens):

    name_parts = []
    params = []
    index = 1

    while index < len(tokens) and tokens[index] != "[":
        if ":" in tokens[index]:
            params.append(tokens[index+1])
            index += 1
        else:
            name_parts.append(tokens[index])
        index += 1

    proc_name = name_parts[0]
    proc_full_name = "".join(name_parts)
    
    if proc_name in grammar["procs"]:
        return False

    if index == len(tokens) or tokens[index] != "[":
        return False

    block_start = index
    block_end = len(tokens) - 1

    rule = [proc_name]
    a = True
    for i in range(1, len(name_parts)-1, 2):
        if a:
            rule.append(":")
            rule.append("N")
            a = False
        rule.append(name_parts[i])
        rule.append(name_parts[i+1])
        rule.append(":")
        rule.append("N")
        grammar["terminals"].append(name_parts[i+1])

    rule.append(".")

    grammar["production_rules"]['PROCEDURE_CALL'].append([proc_name.upper()])
    grammar["production_rules"][proc_name.upper()] = [rule]
    grammar["no_terminals"].append(proc_name.upper())
    grammar["terminals"].append(proc_name)

    grammar["procs"][proc_name] = {
        "full_name": proc_full_name,
        "params": params,
        "body": tokens[block_start:block_end+1]  # Guardamos el bloque completo
    }
    
    return True

def start_if(symbol, pos):
    if symbol == 'VARIABLE_DEFINITION': return pos
    if symbol == 'VARIABLE_ASSIGNMENT': return pos
    if symbol == 'PROCEDURE_DEFINITION': return pos
    return None

def end_if(symbol, current_pos, tokens, start_pos):
    end_pos = current_pos - 1
    out = True
    if symbol == 'VARIABLE_DEFINITION':
        out = create_vars(tokens[start_pos + 1: end_pos])
            
    if symbol == 'VARIABLE_ASSIGNMENT':
        out = set_var(tokens[start_pos], tokens[end_pos-1])
        
    if symbol == 'PROCEDURE_DEFINITION':
        out = create_procedure(tokens[start_pos: end_pos+1])
        pass
    
    return out

def parse(symbol: str, tokens: list, pos: int) -> int:
    if pos <len(tokens): start_pos = start_if(symbol, pos)
    
    if symbol in grammar["terminals"]:
        if pos < len(tokens) and match_token(tokens[pos], symbol):
            return pos + 1
        else:
            return None
    
    for production in grammar["production_rules"][symbol]:
        current_pos = pos
        valid = True
        
        if production == []:
            return current_pos

        for sym in production:
            result = parse(sym, tokens, current_pos)
            
            if result is None:
                valid = False
                break
            current_pos = result
            
        if valid and pos <len(tokens):
            res = end_if(symbol, current_pos, tokens, start_pos)
            if not res:
                valid = False
                
        if valid:
            return current_pos
    
    return None

def main():
    filename = input("Filename (enter to use the example): ")
    if filename == '':filename = "in.txt"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
        sys.exit(1)

    tokens = tokenize_string(code)
    result = parse('S', tokens, 0)

    print()
    if result is not None and result == len(tokens):
        print(True)
    else:
        print(False)

if __name__ == "__main__":
    main()
