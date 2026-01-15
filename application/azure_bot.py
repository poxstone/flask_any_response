from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings)
from botbuilder.core import ActivityHandler, TurnContext
import logging


class DialogflowBot(ActivityHandler):
    _instances = {}
    response = ''
    settings = None
    adapter = None

    def __init__(self, bot_name, teams_app_id, teams_app_password, teams_tenant_id, response):
        self.settings = BotFrameworkAdapterSettings(teams_app_id, teams_app_password, teams_tenant_id)
        self.adapter = BotFrameworkAdapter(self.settings)
        self.response = response

        logging.info(f'_INFO_get_client:: Nueva conexión para {bot_name}.')
        pass

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DialogflowBot, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    async def on_message_activity(self, turn_context: TurnContext):
        user_text = turn_context.activity.text
        session_id = turn_context.activity.conversation.id
        df_response = f'{self.response}:: (user_text: {user_text}) - (session_id: {session_id}) '
        print(f"Respuesta de Dialogflow: '{df_response}'")
        await turn_context.send_activity(df_response)
        pass