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
import logging
def enable_debug_logging():
    # Airflow uses these loggers for tasks
    logger_names = [
        "airflow", 
        "airflow.task", 
        "airflow.task_runner", 
        "airflow.models.taskinstance"
    ]

    for name in logger_names:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

        # Optional: print to confirm
        logger.debug(f"Logger {name} set to DEBUG")