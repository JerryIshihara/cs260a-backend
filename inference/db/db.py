import sqlite3
connection = sqlite3.connect("tutorial.db")
cursor = connection.cursor()

connection.execute("CREATE TABLE IF NOT EXISTS users(id, aws_user_id)")
connection.execute("CREATE TABLE IF NOT EXISTS pricing(id, user_id, plan, create_at)")
connection.execute("CREATE TABLE IF NOT EXISTS video_pose_classification(id, user_id, aws_key, file_location)")
connection.execute("CREATE TABLE IF NOT EXISTS video_comment(aws_key, user_id, comment, created_at)")

# -------------------------video_pose_classification-----------------------------
# check if inferencing is being made (video_pose_classification)
def check_video_pose_classification_exists(id):
    cursor.execute("SELECT id FROM video_pose_classification WHERE id = ?", (id,))
    db_result = cursor.fetchall()
    return len(db_result) > 0

def insert_video_pose_classification_inference_entry(id, file_location):
    cursor.execute(f"INSERT INTO Student video_pose_classification('{id}','{0}','{''}, {file_location}')")

def query_video_pose_classification_inference_location(id):
    cursor.execute("SELECT file_location FROM video_pose_classification WHERE id = ?", (id,))
    db_result = cursor.fetchall()
    return db_result[0]

# ----------------------speed_inference-----------------------------------
