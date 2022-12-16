import gettext

from src.config import APP_NAME_WITHOUT_SPACES, LOCALE_FOLDER_NAME, LOCALE_FOLDER_PATH


gettext_object = gettext.translation(APP_NAME_WITHOUT_SPACES, 
                                     LOCALE_FOLDER_PATH, 
                                     fallback=True)
_ = gettext_object.gettext
