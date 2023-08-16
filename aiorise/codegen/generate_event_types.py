from .codegen import get_by_ref, gen_class, unroll, CodeBlocks

import json

def gen_event_class(name: str, schema: dict) -> tuple[str, CodeBlocks]:
    generated_cls = gen_class(name, schema)
    
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


    event_schemas = [
        (obj['$ref'].split('/')[-1], get_by_ref(schema, obj['$ref']))
        for obj in schema['channels']['/web/webapi']['subscribe']['message']['payload']['oneOf']
        if obj['$ref'].endswith('Event')
    ]

    
    events_union_type = f"AnyEvent = {'|'.join(name for name, _ in event_schemas)}"
    

    event_classes = [
        gen_event_class(name, schema)
        for name, schema in event_schemas
    ]
   

    return [
        *imports,
        *[line for event_class in event_classes for line in event_class],
        events_union_type
    ]



if __name__ == '__main__':
    with open('api.json', 'r') as file:
        schema = json.load(file)

    code = gen_source_code(schema)
    print(unroll(code))


