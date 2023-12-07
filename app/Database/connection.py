from errno import errorcode
import mysql.connector
from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()
# Load the stored environment variables

# Obtain connection string information from the 

config = {
  'host': "dataresto.mysql.database.azure.com",
  'user': "alan",
  'password':"Greeselalutcu123",
  'database': "dataresto",
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/DigiCertGlobalRootG2.crt.pem'
}

# Construct connection string
def connectDB():
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


