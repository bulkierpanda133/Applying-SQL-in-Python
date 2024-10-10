import mysql.connector

# Establish connection to the database
def sql_connector():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="panda1234",
        database="fitness_center_database"
    )

# Function to add a member
def add_member(id, name, age):
    query = "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)"
    
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        cursor.execute(query, (id, name, age))
        conn.commit()
        print(f"Member '{name}' added successfully!")
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Error code for duplicate entry
            print(f"Error: Member ID '{id}' already exists.")
        else:
            print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# Function to add a workout session for a specific member
def add_workout_session(member_id, session_date, session_time, activity):
    query = "INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity) VALUES (%s, %s, %s, %s)"
    
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        cursor.execute(query, (member_id, session_date, session_time, activity))
        conn.commit()
        print(f"Workout session for member ID {member_id} added successfully!")
    except mysql.connector.Error as err:
        if err.errno == 1452:  # Foreign key constraint failed
            print(f"Error: Member ID '{member_id}' does not exist.")
        else:
            print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# Function to update the age of a member
def update_member_age(member_id, new_age):
    query_check = "SELECT * FROM Members WHERE id = %s"
    query_update = "UPDATE Members SET age = %s WHERE id = %s"
    
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        # Check if the member exists
        cursor.execute(query_check, (member_id,))
        if cursor.fetchone() is None:
            print(f"Error: Member ID '{member_id}' does not exist.")
            return
        
        # Update age
        cursor.execute(query_update, (new_age, member_id))
        conn.commit()
        print(f"Member ID {member_id} age updated to {new_age}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# Function to delete a workout session
def delete_workout_session(session_id):
    query_check = "SELECT * FROM WorkoutSessions WHERE session_id = %s"
    query_delete = "DELETE FROM WorkoutSessions WHERE session_id = %s"
    
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        # Check if the session exists
        cursor.execute(query_check, (session_id,))
        if cursor.fetchone() is None:
            print(f"Error: Workout session ID '{session_id}' does not exist.")
            return
        
        # Delete the workout session
        cursor.execute(query_delete, (session_id,))
        conn.commit()
        print(f"Workout session ID {session_id} deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_members_in_age_range(start_age, end_age):
    query = "SELECT id, name, age FROM Members WHERE age BETWEEN %s AND %s"
    
    try:
        conn = sql_connector()  # Establishing the connection to the database
        cursor = conn.cursor()

        # Executing the SQL query to find members in the specified age range
        print(f"Executing query: {query}")
        cursor.execute(query, (start_age, end_age))

        # Fetch all rows from the query result
        results = cursor.fetchall()
        
        if results:
            print("Members aged between", start_age, "and", end_age, ":")
            for row in results:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
        else:
            print(f"No members found between the ages of {start_age} and {end_age}.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()  # Closing the cursor
        conn.close()  # Closing the connection to the database

        
if __name__ == "__main__":
     add_member()
     add_workout_session()
     update_member_age()
     delete_workout_session()
     get_members_in_age_range()