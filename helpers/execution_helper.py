def executer(executables:dict):
    for func, params in executables.items():
        if isinstance(params.get('init_args'), list):
            if params.get('use_context'):
                with func(*params['init_args']) as f:
                    f(**params['kwargs'])
            else:
                func(*params['init_args'])(**params['kwargs'])
        else:
            func(**params)