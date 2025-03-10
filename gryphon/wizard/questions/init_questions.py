import questionary
from questionary import Choice, Separator

from .common_functions import base_question, base_text_prompt, get_back_choice, logger
from ..functions import wrap_text
from ..wizard_text import Text
from ...constants import (
    YES, NO, SYSTEM_DEFAULT, READ_MORE,
    CHANGE_LOCATION, NB_EXTENSIONS, LOCAL_TEMPLATE,
    NB_STRIP_OUT, PRE_COMMIT_HOOKS, ADDON_NAME_MAPPING
)


class InitQuestions:

    @staticmethod
    @base_question
    def ask_which_template(metadata):
        options = [
            Choice(
                title=f"{template.display_name} "
                      + (f"(local template)" if template.registry_type == LOCAL_TEMPLATE else ""),
                value=name
            )
            for name, template in metadata.items()
        ]
        options = sorted(options, key=lambda x: x.title)
        options.extend([
            Separator(Text.menu_separator),
            get_back_choice()
        ])

        template = questionary.select(
            message=Text.init_prompt_template_question,
            choices=options
        ).unsafe_ask()

        return template

    @staticmethod
    @base_text_prompt
    def ask_init_location(template=None):
        
        if template is not None:
        
            yellow_text = ''
            if template.description:
                yellow_text = f"\t{template.description}\n"
                
            text, n_lines = wrap_text(yellow_text)
            logger.warning(text)
        
        return questionary.text(message=Text.init_prompt_location_question).unsafe_ask()

    @staticmethod
    @base_question
    def ask_extra_arguments(arguments: list):
        extra_questions = [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]
        return questionary.unsafe_prompt(extra_questions)

    @staticmethod
    @base_question
    def ask_project_info(template):

        message = (
            Text.init_ask_project_info
        )

        n_lines = len(message.split('\n'))

        options = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]
        
        return questionary.select(
            message=message,
            choices=options
        ).unsafe_ask(), n_lines
    
    
    @staticmethod
    @base_question
    def confirm_init(template, location, read_more_option=False, addons: list = None, **kwargs):

        yellow_text = ''
        # Already shown during 'ask_init_location'
        # if template.description:
        #    yellow_text = f"\t{template.description}\n"

        if addons is not None and len(addons):
            addon_string = ', '.join(map(ADDON_NAME_MAPPING.get, addons))
            yellow_text = yellow_text + f"\n\tThe following addons will be added to the project: {addon_string}\n"

        text, n_lines = wrap_text(yellow_text)
        logger.warning(text)

        message = (
            Text.init_confirm_1
            .replace("{template_name}", template.display_name)
            .replace("{location}", str(location))
        )

        if kwargs:
            message = message + Text.init_confirm_2.replace("{arguments}", kwargs)

        n_lines += len(message.split('\n'))

        options = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]

        if read_more_option:
            options.append(
                Choice(
                    title="Read more",
                    value=READ_MORE
                )
            )

        options.append(
            Choice(
                title="Change project location",
                value=CHANGE_LOCATION
            )
        )
        return questionary.select(
            message=message,
            choices=options
        ).unsafe_ask(), n_lines

    @staticmethod
    @base_text_prompt
    def ask_just_location():
        return (
            questionary
            .text(message=Text.init_prompt_location_question)
            .unsafe_ask()
        )

    @staticmethod
    @base_question
    def ask_python_version(versions):

        choices = [
            Choice(
                title=Text.settings_python_use_system_default,
                value=SYSTEM_DEFAULT
            )
        ]
        choices.extend([
            Choice(
                title=v,
                value=v
            )
            for v in versions
        ])

        choices.extend([
            Separator(),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.settings_ask_python_version,
            choices=choices,
            use_indicator=True
        ).unsafe_ask()

    @staticmethod
    @base_text_prompt
    def ask_addons(add_ons = [{"addon_name": NB_STRIP_OUT, "checked": False}, 
                              {"addon_name": PRE_COMMIT_HOOKS, "checked": False}]):
    
        choices = []
        
        for add_on in add_ons:
            choices.append(
                Choice(
                    title = ADDON_NAME_MAPPING[add_on["addon_name"]],
                    value = add_on["addon_name"],
                    checked = add_on["checked"]
                )
            )
            
        return questionary.checkbox(
            message=Text.init_prompt_addons,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_init_from_existing():
        return questionary.confirm(message=Text.init_prompt_init_from_existing).unsafe_ask()
