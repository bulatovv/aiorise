from .codegen import gen_func, get_by_ref, CodeBlocks, unroll

import json

def pascal_to_snake(name: str) -> str:
    return ''.join([
        '_' + char.lower() if char.isupper() else char
        for char in name
    ]).removeprefix('_')


def gen_api_request(name: str, meta: dict, returns_result: bool) -> tuple[str, CodeBlocks]:
    send_args = [('_type', f"'{name}'")] + [
        (name, name) for name in meta['properties'].keys()
        if name != 'rid'
    ]

    send_args_dict = "{" + ','.join([f"'{key}': {value}" for key, value in send_args]) + "}"
    
    if returns_result:
        resp_type = name.removesuffix('Request') + 'Response'
        func_body = [
            f"return {resp_type}.model_validate(await self._connection.send({send_args_dict}))"
        ]
    else:
        resp_type = 'None'
        func_body = [
            f"await self._connection.send({send_args_dict}, False)"
        ]

    func = gen_func(
        pascal_to_snake(name).removesuffix('_request'),
        [('self', 'HaveApiConnection', '')],
        ['rid'],
        meta,
        resp_type,
        func_body
    )

    return func

def gen_source_code(schema: dict) -> CodeBlocks:
    imports = [
        'from aiorise.api.response_types import *',
        'from aiorise.api.protocols import HaveApiConnection'
    ]

    response_types = [
        obj['$ref'] 
        for obj in schema['channels']['/web/webapi']['subscribe']['message']['payload']['oneOf']
        if obj['$ref'].endswith('Response')
    ]

    api_methods = [
        gen_api_request(
            obj['$ref'].split('/')[-1], 
            get_by_ref(schema, obj['$ref']),
            obj['$ref'].removesuffix('Request') + 'Response' in response_types
        )
        for obj in schema['channels']['/web/webapi']['publish']['message']['payload']['oneOf']
        if obj['$ref'].endswith('Request')
    ]

    cls_def = [
        'class HighriseWebApiMethods:', [
            *api_methods
        ]
    ]

    return [
        *imports,
        *cls_def
    ]

if __name__ == '__main__':
    with open('api.json', 'r') as file:
        schema = json.load(file)

    code = gen_source_code(schema)
    print(unroll(code))
