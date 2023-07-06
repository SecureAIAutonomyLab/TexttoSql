import csv
from io import StringIO
import pyodbc
import sqlalchemy as sa 
from sqlalchemy.engine import URL

class SQLServer:

    def __init__(self, server: str, database: str, user:str, password:str, driver:str, encrypt:str ="no",engine:str =""):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.encrypt = encrypt
        self.engine = engine 

    def connectSQLAlchemy(self):
        try:
            connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};ENCRYPT={self.encrypt}"
            connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
            self.engine  = sa.create_engine(connection_url, pool_pre_ping=True)
            return True
        except Exception as e:
            return str(e)
   
    def execRawQuery(self, query:str):
        try:
            print("SQL Query:" + query)
            result = self.engine.execute(query)
            if result.rowcount == 0:
                print("NO RESULTS FOUND")
            else: 
                print("RESULTS:\n")
                for record in result:
                    print("\n", record)
            return result
        except Exception as e:
            return str(e)

    def getTablesInfo(self, sqlserver:str = "", getRows:bool = False, getTables:str=""):
        # Test the connection by executing a query
        if sqlserver != "": 
            sqlserver = sqlserver
        tables = []
        with sqlserver.engine.connect() as connection:
            metadata = sa.MetaData(bind=self.engine)
            metadata.reflect(schema='SalesLT')
                
            if getTables == "":
                # Iterate over all tables
                for table_name, table in metadata.tables.items(): 
                # Generate the CREATE TABLE script
                    table_info = str(sa.schema.CreateTable(table))
                    if getRows:
                        table_info += f"\n{sqlserver.getRows(table)}\n"
                    tables.append(table_info)
            else: 
                for table_name, table in metadata.tables.items(): 
                    if table_name in getTables: 
                        # Generate the CREATE TABLE script
                        table_info = str(sa.schema.CreateTable(table))
                        if getRows:
                            table_info += f"\n{sqlserver.getRows(table)}\n"
                        tables.append(table_info)
                
        finalTableInfo = "\n\n".join(str(v) for v in tables)
        return finalTableInfo
    
    def getRows(self, table:str) -> str:

        command = sa.select(table).limit('3')
        columnsNames = "\t".join([col.name for col in table.columns])
        try:
            # get the sample rows
            with self.engine.connect() as connection:
                sample_rows_result = connection.execute(command)  
                # shorten values in the sample rows
                sample_rows = list(
                    map(lambda ls: [str(i)[:100] for i in ls], sample_rows_result)
                )

            # save the sample rows in string format
            sample_rows_str = "\n".join(["\t".join(row) for row in sample_rows])

        except Exception as e:
            print("Error: getting rows")

        return (
            f"{'3'} rows from {table.name} table:\n"
            f"{columnsNames}\n"
            f"{sample_rows_str}"
        )
        




