def etl(extract, transform, load):
    if isinstance(extract, dict):
        for e, params in extract.items():
            if params['use_context']:
                with e(*params['init_args']) as extractor:
                    extractor(**params['kwargs'])
            else:
                e(*params['init_args'])(**params['kwargs'])
    else:
        extract()
    if isinstance(transform, dict):
        for t, kwargs in transform.items():
            t(**kwargs)
    else:
        transform()
    if isinstance(load, dict):
        for l, kwargs in load.items():
            l(**kwargs)
    else:
        load()