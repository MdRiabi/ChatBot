from db import init_db, get_or_create_user,save_message,get_history

init_db()
user_id = get_or_create_user("mohamed")
save_message(user_id, "user", "Bonjour !")
save_message(user_id, "assistant", "Bonjour Mohamed, comment puis-je vous aider ?")