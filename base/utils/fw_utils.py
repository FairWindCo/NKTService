def get_request_param_value(request, name, param_obj={}):
    result = (False, param_obj)
    if name in request.POST and request.POST[name]:
        param_obj[name] = request.POST[name]
        result = (True, param_obj)
    elif name in request.GET and request.GET[name]:
        param_obj[name] = request.GET[name]
        result = (True, param_obj)
    return result


def get_request_param_value_bool(request, name, param_obj={}):
    result = False
    if name in request.POST and request.POST[name]:
        param_obj[name] = request.POST[name]
        result = True
    elif name in request.GET and request.GET[name]:
        param_obj[name] = request.GET[name]
        result = True
    return result