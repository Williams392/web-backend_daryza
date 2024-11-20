from django.db import connection
from authentication.models import CustomUser

def set_user_context(user):
    """
    Establece el contexto del usuario en SQL Server para ser usado por los triggers.
    """
    with connection.cursor() as cursor:
        user_id = user.username.strip().encode('utf-8').hex()  
        query = f"SET CONTEXT_INFO 0x{user_id}"
        print(f"Executing SQL: {query}")
        cursor.execute(query)
