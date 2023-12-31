from .codegen import get_by_ref, gen_class, unroll, CodeBlocks

import json

def gen_request_class(name: str, schema: dict) -> tuple[str, CodeBlocks]:
    generated_cls = gen_class(name, ["rid"], schema)
    
    generated_cls[1].insert(
        1, f'type: Literal["{name}"] = Field(alias="_type")'
    )
    
    return generated_cls


def gen_source_code(schema: dict) -> CodeBlocks:
    imports = [
        'from pydantic import BaseModel, Field',
        'from typing import Literal, Any',
        'from aiorise.objects.object_types import *',
    ]

    request_schemas = [
        (obj['$ref'].split('/')[-1], get_by_ref(schema, obj['$ref']))
        for obj in schema['channels']['/web/webapi']['publish']['message']['payload']['oneOf']
        if obj['$ref'].endswith('Request')
    ]

    response_classes = [
        gen_request_class(name, schema)
        for name, schema in request_schemas
    ]

    return [
        *imports,
        *[line for response_class in response_classes for line in response_class],
    ]


if __name__ == '__main__':
    with open('api.json', 'r') as file:
        schema = json.load(file)

    code = gen_source_code(schema)
    print(unroll(code))
