from gryphon.wizard.wizard_text import Text
from .constants import *


def wizard_add(lib_name):
    child = pexpect.spawn(command='gryphon')

    # » Install Python libraries/packages
    child.expect(WELCOME_MESSAGE)
    child.send(KEY_DOWN * 2)
    child.sendcontrol('m')

    # » ○ >> Type the library name manually
    child.expect(Text.add_prompt_categories_question)
    child.send(KEY_DOWN * 8)
    child.sendcontrol('m')

    child.expect(Text.add_prompt_type_library)
    child.send(lib_name)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()