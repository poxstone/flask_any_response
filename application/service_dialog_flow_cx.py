import os
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument


def extract_text_from_dialogflow_response(response: dialogflow.DetectIntentResponse) -> str:
    messages = response.query_result.response_messages
    
    extracted_texts = []

    for message in messages:
        if message.text:
            extracted_texts.extend(message.text.text)
    
    final_text = "\n".join(extracted_texts)

    if not final_text:
        return "El agente no devolvió una respuesta de texto (posiblemente un custom payload)."
        
    return final_text


def detect_intent_text(project_id, location, agent_id, session_id, text, language_code):
    client_options = None
    location == 'us-central1' if not location else location
    api_endpoint = f"{location}-dialogflow.googleapis.com:443"
    client_options = {"api_endpoint": api_endpoint}

    session_client = dialogflow.SessionsClient(client_options=client_options)
    
    session_path = session_client.session_path(
        project=project_id, 
        location=location, 
        agent=agent_id, 
        session=session_id
    )

    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input, language_code=language_code)
    
    request = dialogflow.DetectIntentRequest(
        session=session_path, 
        query_input=query_input
    )

    try:
        response = session_client.detect_intent(request=request)
        
        print("=" * 20)
        print(f"Texto enviado: {response.query_result.text}")
        
        # Iterar sobre los mensajes de respuesta del agente
        for message in response.query_result.response_messages:
            if message.text:
                print(f"Respuesta del Agente: {message.text.text[0]}")
        
        return response
    except InvalidArgument as e:
        print(f"Error en la petición: {e}")

