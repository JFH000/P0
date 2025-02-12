import re

def leer_archivo_como_string(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        return f"Error: El archivo '{nombre_archivo}' no fue encontrado."
    except Exception as e:
        return f"Error: {str(e)}"

def tokenize_string(s: str):
    """
    Recibe un string y lo divide en una lista de palabras separando por espacios, tabuladores, saltos de línea,
    paréntesis, corchetes, barras verticales y comas.
    """
    # Usamos una expresión regular para dividir por espacios, tabuladores, saltos de línea y capturar (, [, |, y comas
    tokens = re.findall(r'and|[\w#]+|[(),\[\]|:=.]', s)
    
    return tokens

def create_grammar():
    noTerminals = [
        "S", "INSTRUCTION", "COMMAND", "J_COMMAND", "G_COMMAMD", "NATURAL",
        "CREATE_VARIABLES", "STRINGS", "STRING", "PROCEDURE", "LAMBDA", "STRING",
        "PROCEDURE", "PARAM", "BLOCK", "PROCEDURE_CALL", "PARAMS", "INSTRUCTIONS",
        "INSTRUCTION", "VARIABLE_ASSIGNMENT", "PROCEDURE_CALL", "CONDITIONAL",
        "LOOP", "COSNTANT", "VALUE", "GOTO", "N", "MOVE", "TURN", "FACE", "PUT",
        "PICK", "JUMP", "NOP", "TOTHE", "INDIR", "OFTYPE", "X", "CONDITIONAL",
        "LOOP", "REPEAT_TIMES", "CONDITION", "FACING", "CANPUT", "CANPICK",
        "CANMOVE", "CANJUMP", "NOT"]
    
    variables = {}
    procs = {}
    constant = {}
    
    terminals = [
        "|", ";", "M", "R", "C", "B", "c", "b", "P", "J", "G", "(", ")",
        variables, "proc", "and", ":", procs, constant, ".", "[", "]",
        "goto", "with", "move", "turn", "face", "put", "pick", "jump", "nop",
        "toThe", "inDir", "ofType", "if", "then", "else", "while", "do",
        "for", "repeat", "facing", "canPut", "canPick", "canMove", "canJump",
        "not", "#front", "#right", "#left", "#back", "#north", "#south", "#west",
        "#east", "#balloons", "#chips"]
    
    initialElement = 'S'
    
    productionRules = {
        'INSTRUCTION': [['COMMAND', ';']],
        'COMMAND': [['M'], ['R'], ['C'], ['B'], ['c'], ['b'], ['P'], ['J_COMMAND'], ['G_COMMAND']],
        'J_COMMAND': [['J', '(', 'NATURAL', ')']],
        'G_COMMAND': [['G', '(', 'NATURAL', ',', 'NATURAL', ')']],
        'NATURAL': [['integer']],
        'CREATE_VARIABLES': [['|', 'STRINGS', '|']],
        'STRINGS': [['STRING', 'STRING_NEXT']],
        'STRING': [['string']],
        'STRING_NEXT': [[',', 'STRING', 'STRING_NEXT'], ['LAMBDA']],
        'PROCEDURE': [['proc', 'STRING', 'PARAMS', 'BLOCK']],
        'PARAMS': [[':', 'PARAM', 'PARAM_NEXT'], ['LAMBDA']],
        'PARAM_NEXT': [['and', ':', 'PARAM', 'PARAM_NEXT'], ['LAMBDA']],
        'PROCEDURE_CALL': [['{', 'procs', '}', 'PARAMS', '.']],
        'BLOCK': [['[', 'INSTRUCTIONS', ']']],
        'INSTRUCTIONS': [['INSTRUCTION', 'INSTRUCTION'], ['LAMBDA']],
        'INSTRUCTION': [
            ['CREATE_VARIABLES'], ['VARIABLE_ASSIGNMENT'], ['PROCEDURE_CALL'],
            ['CONDITIONAL'], ['LOOP'], ['CONSTANT'], ['GOTO'], ['MOVE'],
            ['TURN'], ['FACE'], ['PUT'], ['PICK'], ['JUMP'], ['NOP']
        ],
        'VARIABLE_ASSIGNMENT': [['{', 'variables', '}', ':', '=', 'VALUE', '.']],
        'VALUE': [['NATURAL'], ['STRING']],
        'CONSTANT': [['{', 'constant', '}']],
        'GOTO': [['goto:', 'N', 'with:', 'N', '.']],
        'N': [['VARIABLE'], ['NATURAL']],
        'D': [['#front'], ['#right'], ['#left'], ['#back']],
        'O': [['#north'], ['#south'], ['#west'], ['#east']],
        'X': [['#balloons'], ['#chips']],
        'VARIABLE': [['{', 'variables', '}']],
        'TOTHE': [['toThe', ':', 'D']],
        'INDIR': [['inDir', ':', 'O']],
        'OFTYPE': [['ofType', ':', 'X']],
        'MOVE': [['move', ':', 'N', '.'], ['move', ':', 'N', 'TOTHE', '.'], ['move', ':', 'N', 'INDIR', '.']],
        'TURN': [['turn', ':', 'D', '.']],
        'FACE': [['face', ':', 'O', '.']],
        'PUT': [['put', ':', 'N', 'OFTYPE', '.']],
        'PICK': [['pick', ':', 'N', 'OFTYPE', '.']],
        'JUMP': [['jump', ':', 'N', 'TOTHE', '.'], ['jump', ':', 'N', 'INDIR', '.']],
        'NOP': [['nop', '.']],
        'CONDITIONAL': [['if', ':', 'CONDITION', 'then', ':', 'BLOCK', 'else', ':', 'BLOCK']],
        'LOOP': [['while', ':', 'CONDITION', 'do', ':', 'BLOCK']],
        'REPEAT_TIMES': [['for', ':', 'N', 'repeat', ':', 'BLOCK']],
        'CONDITION': [['FACING'], ['CANPUT'], ['CANPICK'], ['CANMOVE'], ['CANJUMP'], ['NOT']],
        'FACING': [['facing', ':', 'O', '.']],
        'CANPUT': [['canPut', ':', 'N', 'OFTYPE', '.']],
        'CANPICK': [['canPick', ':', 'N', 'OFTYPE', '.']],
        'CANMOVE': [['canMove', ':', 'N', 'INDIR', '.'], ['canMove', ':', 'N', 'TOTHE', '.']],
        'CANJUMP': [['canJump', ':', 'N', 'INDIR', '.'], ['canJump', ':', 'TOTHE', '.']],
        'NOT': [['not', ':', 'CONDITION']],
        'S': [
            ['CREATE_VARIABLES', 'S'], ['PROCEDURE', 'S'], ['VARIABLE', 'S'],
            ['PROCEDURE_CALL', 'S'], ['LAMBDA']
        ]
    }
    g = {'noTerminals':noTerminals, 'terminals':terminals, 'initialElement':initialElement, 'productionRules':productionRules}
    
    return g

def igualdadRara(token, rule):
    if token == rule: return True
    else:
        if rule == 'integer':
            if token.isnumeric():
                return True
            
        if rule == 'string':
            return True
        
    return False

def parse(tokens: list, grammar: dict):
    noTerminals = grammar.get('noTerminals')
    terminals = grammar.get('terminals')
    initialElement = grammar.get('initialElement')
    productionRules = grammar.get('productionRules')
    try_rule(grammar, initialElement, tokens)
    pass

def try_rule(grammar: dict, element, tokens, acum_tokens = 0):
    productionRules = grammar.get('productionRules').get(element)
    for rule in productionRules:
        acum_acum_tokens = 0
        for mini_rule in rule:
            if mini_rule in grammar.get('noTerminals'):
                try_rule(grammar, mini_rule, tokens, acum_tokens)
            elif mini_rule in grammar.get('terminals'):
                if igualdadRara(tokens[acum_tokens], mini_rule):
                    acum_tokens += 1
                    acum_acum_tokens -= 1
                    pass
                else:
                    acum_tokens += acum_acum_tokens
                    break
                    
                    
                pass
            pass
        pass
    pass

def main():
    file = "in.txt"
    tokens = tokenize_string(leer_archivo_como_string(file))
    grammar = create_grammar()
    return parse(tokens, grammar)
    
    print(token_list)

if __name__ == "__main__":
    main()
