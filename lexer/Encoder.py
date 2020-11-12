import json
from .Token import Token
from parser.AST import *

class MainNodeEncoder(json.JSONEncoder):

    '''def default(self, obj):
        if isinstance(obj, Token):
            return {obj.type: obj.val}
        return json.JSONEncoder.default(self, obj)'''

    def default(self, obj):
        if isinstance(obj, MainNode):
            return {'declarations': [obj.declarations], 'statements' : obj.statements}

class TokenEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Token):
            return { obj.type: obj.val }

class TableEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Token):
            return {"val": obj.val, "type":obj.type}
        return json.JSONEncoder.default(self,obj)