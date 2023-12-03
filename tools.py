#%% 
import glob
import ast 
import docstring_parser


def get_docstring_info(node):
    docstring = ast.get_docstring(node)
    if docstring:
        parsed_docstring = docstring_parser.parse(docstring)
        info = {
            "description": parsed_docstring.short_description,
            "args": {}
        }

        arg_types = {

            "str": "string",
            "int": "number",
            "list": "array"
        }

        for param in parsed_docstring.params:
            info["args"][param.arg_name] = {
                "type": arg_types.get(param.type_name,"my_arg_type_not_found"),
                "description": param.description
            }

        return info
    else:
        return {"description": "", "args": {}}


def function_to_json(node):
    function_info = get_docstring_info(node)
    function_json = {
        "type": "function",
        "function": {
            "name": node.name,
            "description": function_info["description"],
            "parameters": {
                "type": "object",
                "properties": function_info["args"],
                "required": list(function_info["args"].keys())
            }
        }
    }
    return function_json



def fetch_all_tools(tools_path:str):
    tools = []
    if tools_path.endswith('.py'):
        files = [tools_path]
    else:
        files = glob.glob(tools_path)
    for file in files:
        if not file.startswith('function_') and not file.endswith('.py'):
            continue
        
        with open(file) as f:
            tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    tools.append(function_to_json(node))
                    
    return tools