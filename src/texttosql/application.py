import sqlalchemy as sa
from gptAPI import GptApi
from sqlServerDB import SQLServer
from prompts import Prompts
from configuration import Config
import json

class Application:

    def __init__(self):
        config = Config("src/texttosql/config.ini")
        driver = config.get("db_connection", "driver")
        server = config.get("db_connection", "server")
        database = config.get("db_connection", "database")
        user = config.get("db_connection", "user")
        password = config.get("db_connection", "password")
        encrypt = config.get("db_connection", "encrypt")
        openai_api_key = config.get("gptAPI", "api_key")
        openai_model = config.get("gptAPI", "model")

        self.sqlserver = SQLServer(server, database, user, password, driver, encrypt)
        self.sqlserver.connectSQLAlchemy()
        self.initalMessages = Prompts(self.sqlserver)
        self.initalMessages = self.initalMessages.ini_prompt()
        self.chatModel = GptApi(openai_api_key, "TEST", openai_model,self.initalMessages)

    def getSchemaDB(self,getRows:str = "", getTables:str = ""): 
        return self.sqlserver.getTablesInfo(sqlserver=self.sqlserver, getRows=getRows, getTables=getTables)

    def workflow(self, message:str, sender:str):
        #1. first get potential tables
        myTables = self.chatModel.getPotentialTables(message, sender)
        #2. Generate tables schema 
        TablesSchema = self.getSchemaDB(getRows = True, getTables=myTables)
        #3. Call the response API
        responseString = self.chatModel.generateResponseSchema(message, sender,TablesSchema)
        try:
            if responseString.endswith('.'):
                response = json.loads(responseString[:-1])
            else:
                response = json.loads(responseString)
        except ValueError:
            return self.workflow("Repeat answer but use valid JSON only.", "SYSTEM")
        print(response)
        recipient = response.get("recipient")
        if recipient.upper() == "USER":
            return response["message"]
        elif recipient.upper() == "SERVER":
            action = response["action"]
            if action.upper() == "QUERY":
                result = self.sqlserver.execRawQuery(response.get("message"))
                return result
            else:
                print('Invalid action')
                print(response)
        else: 
            print(response)
    


       
