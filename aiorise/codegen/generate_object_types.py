from .codegen import gen_class, unroll, CodeBlocks

import json

def gen_source_code(schema: dict) -> CodeBlocks:
    imports = [
        'from pydantic import BaseModel, Field',
        'from typing import Literal, Any',
    ]


    pub_components = [
        obj['$ref'].split('/')[-1]
        for obj in schema['channels']['/web/webapi']['publish']['message']['payload']['oneOf']
    ]

    sub_components = [
        obj['$ref'].split('/')[-1]
        for obj in schema['channels']['/web/webapi']['subscribe']['message']['payload']['oneOf']
    ]


    object_classes = [
        gen_class(obj_name, obj_schema)
        for obj_name, obj_schema in schema['components']['schemas'].items()
        if obj_name not in [*pub_components, *sub_components]
    ]

    return [
        *imports,
        *[line for object_class in object_classes for line in object_class]
    ]




if __name__ == '__main__':
    with open('api.json', 'r') as file:
        schema = json.load(file)

    code = gen_source_code(schema)
    print(unroll(code))
