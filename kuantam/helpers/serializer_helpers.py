import logging
from kuantam.consts import STATUS_ACTIVE, CREATION_BY
from kuantam.middleware.auth import get_request
import datetime
from kuantam.status_code import error_while_log_table_saving, generic_error_2
import jwt

logger = logging.getLogger("django")


def common_add_required_data_in_json(field, is_create=True):
    request = get_request()
    if is_create:
        field['creation_date'] = datetime.datetime.now()
        field['status'] = STATUS_ACTIVE
        if request:
            field['creation_by'] = request.user_id
        else:
            field['creation_by'] = CREATION_BY
        
    else:
        field["updation_date"] = datetime.datetime.now()
        if request:
            field["updation_by"] = request.user_id
        else:
            field["updation_by"] = CREATION_BY

    return field



def add_log_model(logModel, modelInstance, modelName):
    from kuantam.helpers.custom_helpers import CustomExceptionHandler
    """_summary_
    Args:
        logModel (_type_): Log Model that want to create/update 
        modelInstance (_type_): Model from which the data will be added
        modelName (_type_): Model Name use in error showing
    """
    try:
        logger.debug("Saving log model %s", modelInstance.__dict__)
        logModel = logModel()
        logModel.__dict__ = modelInstance.__dict__.copy()
        logModel.id = None
        logModel.log = modelInstance
        # request = get_request()
        logModel.created_by = CREATION_BY
        logModel.creation_date = datetime.datetime.now()
        logModel.save()
        return logModel
    except Exception as e:
        logger.exception("Exception is", e)
        raise CustomExceptionHandler(error_while_log_table_saving(f'{modelName} Log'))

def help_text_for_dict(dict_value):
    """_summary_

    Args:
        dict_value (_type_): Dict type

    Returns:
        _type_: String Format help text
    """
    return f'Enter value from this list - {list(dict_value.keys())}'
