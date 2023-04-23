"""Amoga"""
DICTIONARY = ('''{{
    "<class 'dict'>_{id:x}": {{
    {items}
    }}
}}''')
ITERABLE = ('''{{
    "{type}_{id:x}": {{
        "items": {items}
    }}
}}''')
CALLABLE = ('''{{
        "{type}_{id:x}": {{
        "argcount": "{argcount}",
        "posonlyargcount": "{posonlyargcount}",
        "kwonlyargcount": "{kwonlyargcount}",
        "nlocals": "{nlocals}",
        "stacksize": "{stacksize}",
        "flags": "{flags}",
        "codestring": "{code}",
        "consts": "{consts}",
        "names": "{names}",
        "varnames": "{varnames}",
        "filename": "{filename}",
        "name": "{name}",
        "firstlineno": "{firstlineno}",
        "lnotab": "{lnotab}"
        "globals": {globals}
    }}
}}''')
