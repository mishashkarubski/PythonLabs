"""Amoga"""
FUNCTION_TEMPLATE = ("""{{
    {name}: {{
        argcount: {argcount},
        posonlyargcount: {posonlyargcount},
        kwonlyargcount: {kwonlyargcount},
        nlocals: {nlocals},
        stacksize: {stacksize},
        flags: {flags},
        codestring: {code},
        consts: {consts},
        names: {names},
        varnames: {varnames},
        filename: {filename},
        name: {name},
        firstlineno: {firstlineno},
        lnotab: {lnotab},
    }}
}}""")