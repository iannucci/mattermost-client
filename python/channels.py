import json
from mattermostdriver import Driver

file_path = 'config.json'
config_data = {}
try:
	with open(file_path, 'r') as f:
		config_data = json.load(f)
	print("Configuration data loaded successfully:")
except FileNotFoundError:
	print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError:
	print(f"Error: Could not decode JSON from '{file_path}'. Check file format.")
except Exception as e:
	print(f"An unexpected error occurred: {e}")

login_dict = {
    'url': config_data['hostname'],
    'token': config_data['pat'],
    'scheme': config_data['scheme'],
    'port': config_data['port'],
    'basepath': config_data['basepath']
}

mattermost_api = Driver(login_dict)
mattermost_api.login()

testuser_data = {
  "email": "",
  "username": "",
  "first_name": "",
  "last_name": "",
  "nickname": "",
  "password": "",
}

def create_user(user_data=testuser_data):
	return mattermost_api.users.create_user(options=user_data)

def get_user_id_by_name(user_name):
	user_data = mattermost_api.users.get_user_by_username(user_name)
	if not user_data:
		print(f'User {user_name} not found.')
		return None
	return user_data['id']

def print_user(user_id):
	user_data = mattermost_api.users.get_user(user_id)
	if not user_data:
		print(f'User {user_name} not found.')
		return None
	# print(user_data)
	print(f'User ID: {user_data["id"]}')
	print(f'First name: {user_data["first_name"]}')
	print(f'Last name: {user_data["last_name"]}')
	print(f'Nickname: {user_data["nickname"]}')

def change_username(user_id, new_username):
	user_data = mattermost_api.users.get_user(user_id)
	if not user_data:
		print(f'User {user_id} not found.')
		return None
	user_data['username'] = new_username.strip()
	return mattermost_api.users.update_user(user_id, options=user_data)	

def cleanup_user(user_id, first_name, last_name):
	''' Adds first and last name to user and sets the nickname to first name + uppercase callsign '''
	user_data = mattermost_api.users.get_user(user_id)
	if not user_data:
		print(f'User {user_id} not found.')
		return None
	username = user_data['username'].strip()
	user_data['first_name'] = first_name.strip()
	user_data['last_name'] = last_name.strip()
	user_data['nickname'] = f'{first_name} {username.upper()}'
	return mattermost_api.users.update_user(user_id, options=user_data)

user = ''
first = ''
last = ''

print_user(get_user_id_by_name(user))
# cleanup_user(get_user_id_by_name(user), first, last)
# print_user(get_user_id_by_name(user))
