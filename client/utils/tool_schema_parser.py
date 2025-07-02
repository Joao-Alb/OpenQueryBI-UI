def extract_tool_parameters(tool):
    parameters = []

    if not hasattr(tool, 'args_schema'):
        return parameters

    schema = tool.args_schema
    if isinstance(schema, dict):
        schema_dict = schema
    else:
        schema_dict = schema.schema()

    properties = schema_dict.get('properties', {})
    required = schema_dict.get('required', [])

    for name, info in properties.items():
        param_type = info.get('type', 'string')
        title = info.get('title', name)
        default = info.get('default', None)
        is_required = name in required

        desc = f"{title} ({param_type})"
        desc += " - required" if is_required else " - optional"
        if default is not None:
            desc += f" [default: {default}]"

        parameters.append(desc)

    return parameters