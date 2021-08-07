def convert(model, converter):
    tmp_model = Model()
    for attr in model.__names__:
        if attr in converter.keys():
            value = converter(getattr(model, attr))
            tmp_model.register(attr, value)
        else:
            value = getattr(model, attr)
            tmp_model.register(attr, value)
    return tmp_model