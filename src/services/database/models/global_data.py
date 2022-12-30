from sqlalchemy import select
from src.database.models import GlobalData, session
from src.config import PRIMARY_SETTINGS, SettingsEnum


def get_settings() -> dict:
    """
        Method for get user settings
    """
    result = session.query(GlobalData).first()

    if not result:
        return create_settings().data

    else:
        return result.data


def create_settings() -> GlobalData:
    global_data = GlobalData(data=PRIMARY_SETTINGS)
    session.add(global_data)
    session.commit()
    return global_data


def set_setting(setting: SettingsEnum, value):
    settings = session.query(GlobalData).first()
    settings.data[setting.value] = value
    session.commit()

