def execute_callable(func, params):
    """Helper to execute a function with optional context handling"""
    if params.get('use_context', False):
        with func(*params.get('init_args', [])) as context_func:
            return context_func(**params.get('kwargs', {}))
    else:
        return func(*params.get('init_args', []))(**params.get('kwargs', {}))