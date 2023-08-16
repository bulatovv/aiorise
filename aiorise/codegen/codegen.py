import json
from functools import reduce


CodeBlocks = list['CodeBlocks | str']

def get_by_ref(data: dict, ref: str):
    return reduce(lambda d, key: d[key], ref.split("/")[1:], data)

def gen_type_hint(meta: dict, required: bool) -> str:
    def map_type(meta: dict) -> str:
        match meta:
            case {"oneOf": [*variants], **rest}:
                return f"{' | '.join(map(map_type, variants))}"
            case {"enum": [*variants], **rest}:
                return f"Literal[{', '.join(map(repr, variants))}]"
            case {
                "type": "array", "prefixItems": [*variants],
                "min_items": min_items, "max_items": max_items, **rest
            } if min_items == max_items:
                typed = [map_type(variant) for variant in variants]
                not_typed = ["Any" for _ in range(min_items - len(variants))]
                return f"tuple[{', '.join(typed + not_typed)}]"
            case {"type": "array", "items": {**items_meta}, **rest}:
                return f"list[{map_type(items_meta)}]"
            case {"type": "integer", **rest}:
                return "int"
            case {"type": "string", **rest}:
                return "str"
            case {"type": "boolean", **rest}:
                return "bool"
            case {"type": "number", **rest}:
                return "float"
            case {"$ref": ref, **rest}:
                return ref.split("/")[-1]
            case _:
                raise ValueError()

    type_hint = map_type(meta)
    if not required:
        type_hint = f"{type_hint} | None"

    return type_hint

def gen_default_value(meta: dict, required: bool) -> str:
    if not required:
        return " = None"

    return ''

def gen_class(name: str, meta: dict) -> tuple[str, CodeBlocks]:
    cls_def_start = f"class {name}(BaseModel):"
    docstring = f'"""{meta["description"]}"""' if meta.get("description") else ''
    
    cls_body = [
        f'{name}: ' 
        + gen_type_hint(prop_meta, name in meta.get("required", []))
        + gen_default_value(prop_meta, name in meta.get("required", []))
        for name, prop_meta in meta["properties"].items()
    ]

    return (
        cls_def_start, [
            docstring,
            *cls_body
        ]
    )

def gen_func(
    name: str, 
    additional_args: list[tuple[str, str, str]], 
    ignore_args: list[str],
    meta: dict, 
    return_type: str, 
    body: list[str] = ['...']
) -> tuple[str, CodeBlocks]:
    args = additional_args + [
        (
            name, 
            gen_type_hint(prop_meta, name in meta.get("required", [])), 
            gen_default_value(prop_meta, name in meta.get("required", []))
        )
        for name, prop_meta in meta["properties"].items()
        if name not in ignore_args
    ]

    func_sig = f"async def {name}({', '.join([f'{name}: {type_hint}{default_value}' for name, type_hint, default_value in args])}) -> {return_type}:"
    docstring = f'"""{meta["description"]}"""' if meta.get("description") else ''

    return (
        func_sig, [
            docstring,
            *body
        ]
    )


def unroll(blocks: CodeBlocks, indent: int = 0) -> str:
    return '\n'.join([
        ' ' * indent * 4 + block if isinstance(block, str) 
            else unroll(block, indent + 1)
        for block in blocks
    ])

