from sqlServerDB import SQLServer

# TEMPLATE FOR INITIAL PROMPT 
class Prompts:

    def __init__(self, sqlserver: SQLServer):
        self.sqlServer = sqlserver

    def ini_prompt(self):    

        query = "Show OrdeQty, the Name and the ListPrice of the order made by CustomerID 635"
        tableNames =self.sqlServer.getTablesInfo(self.sqlServer)

        initialPrompt = f'''As the intermediary between the user and the database, your primary objective is to generate a comma-separated list of Relevant Table Names based on the question provided by the user and the provided List of Tables below.

        Question: {query}

        List of Tables: {tableNames}

        Relevant Table Names:SalesLT.SalesOrderHeader,SalesLT.SalesOrderDetail,SalesLT.Product'''

        firstGetTablesTemplate = [
                {"role": "system", "content":initialPrompt},
                {"role": "system", "content":"Only respond with the Relevant Table Names, do not include any query in the response to the user. "},
                {"role": "user", "content": "Show the CompanyName for James D. Kramer"},
                {"role": "assistant", "content": "Relevant Table Names:SalesLT.Customer"},
                {"role": "user", "content": "Show all the addresses listed for 'Modular Cycle Systems'"},
                {"role": "assistant", "content": "Relevant Table Names:SalesLT.Customer,SalesLT.CustomerAddress,SalesLT.Address"},
            ]

        return firstGetTablesTemplate   
    
    