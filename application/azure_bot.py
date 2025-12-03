import asyncio
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings)
from botbuilder.schema import Activity
from botbuilder.core import ActivityHandler, TurnContext
from application.utils import printing
from .config import APP_ID, APP_PASSWORD, TENANT_ID, DF_AGENT_ID, DF_LOCATION, RESPONSE

SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD, TENANT_ID)
ADAPTER = BotFrameworkAdapter(SETTINGS)


class DialogflowBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_text = turn_context.activity.text
        session_id = turn_context.activity.conversation.id
        df_response = f'{RESPONSE}:: (user_text: {user_text}) - (session_id: {session_id}) '
        printing(f"Respuesta de Dialogflow: '{df_response}'")
        await turn_context.send_activity(df_response)

BOT = DialogflowBot()