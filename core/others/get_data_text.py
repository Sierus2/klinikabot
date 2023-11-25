def dict_line(dicts):
    result = []

    def list_dict(dicts):
        for key, value in dicts.items():
            if isinstance(value, dict):
                list_dict(value)
            else:
                result.append(f'{key.capitalize()}: {value}')

    list_dict(dicts)
    return ';\r\n'.join(result)
