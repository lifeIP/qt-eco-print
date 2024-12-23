SERVICE_FILE_NAME:str = "service_data/"

LIST_OF_VALUES = [
    "last_time_activity", 
    "app_status", 
    "session_id", 
    "file_path", 
    "bot_request", 
    "app_response", 
    "app_request", 
    "bot_response",
    "chat_id"
]

def get_service_data_from_file(prop = 
                               "last_time_activity" or 
                               "app_status" or 
                               "session_id" or
                               "file_path" or 
                               "bot_request" or 
                               "app_response" or
                               "app_request" or
                               "bot_response" or
                               "chat_id"
                               ):
    if prop not in LIST_OF_VALUES: 
        print("not in LIST_OF_VALUES")
        return None

    try:
        line = list()
        with open(SERVICE_FILE_NAME + prop, "r") as f:
            line = f.readline()
        return str(line).rstrip("\n")
    except:
        pass
    return None


def set_service_data_into_file(prop = 
                               "last_time_activity" or 
                               "app_status" or 
                               "session_id" or
                               "file_path" or 
                               "bot_request" or 
                               "app_response" or
                               "app_request" or
                               "bot_response" or
                               "chat_id"
                               , value: str = ""):
    
    if prop not in LIST_OF_VALUES: 
        print("not in LIST_OF_VALUES")
        return
    if len(value) == 0:
        return

    try:
        line = list()
        with open(SERVICE_FILE_NAME + prop, "r") as f:
            line = f.readline()

        line = value + "\n"
        
        with open(SERVICE_FILE_NAME + prop, "w") as f:
            f.writelines(line)
    except:
        pass



