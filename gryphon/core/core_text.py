class Text:
    install_end_message_1 = """To enter the folder of the created project and activate the virtual 
                environment you can use the following commands:"""

    install_end_message_2 = "Once you've done this you will be able to add libraries and templates to your project."
    
    install_end_message_4 = """To enter the folder of the created project, use the command:"""
    
    install_end_message_3 = """Then run Gryphon again to add templates and libraries to the project. 
    
                You can also type
                    >> pipenv shell
                    to activate and enter the virtual environment."""

    handover_end_message = "Handover package successfully generated:"

    feedback_email_template = """Hello Gryphon team!

    <<Type your message/feedback here>>

Best regards,

"""

    access_request_email_template = """Hi,

Please may I be given access to the GitHub repository for the following Gryphon template:
    
{template_url}

Thanks and best regards,

"""

    bug_report_email_template = """Hello Gryphon team!

Please find details regarding the bug below:

    [[Please explain how you arrived at this bug]]

{traceback}

Best regards,

"""

    project_use_description_template = """Hi Gryphon team,

I intend to use Gryphon on the project / initiative: [Case Code if available. Otherwise, name of key Partner(s) on project]

Description of use: [Brief overview of the use-case and technical / analytical methodology]

Expected project duration: [When do you expect this project to finish?]

(Note: This information helps the Gryphon team understand how the tool is used and the value it brings to the firm, which enables continued support and improvements to the tool) 
"""