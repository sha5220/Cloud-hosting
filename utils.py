import os

def save_website_files(username, website_id, files):
    user_dir = os.path.join('websites', username)
    website_dir = os.path.join(user_dir, str(website_id))

    if not os.path.exists(website_dir):
        os.makedirs(website_dir)

    for file in files:
        file_path = os.path.join(website_dir, file.filename)
        file.save(file_path)
