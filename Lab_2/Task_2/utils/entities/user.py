from .storage import Storage


class User:
    def __init__(self, username=None):
        self.__username = username
        self.__container = Storage()

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, new_username):
        self.username = new_username

    @property
    def container(self):
        return self.__container

    def add_keys(self, keys):
        self.container.add(keys)

    def remove_key(self, key):
        self.container.remove(key)

    def list_data(self):
        print(self.container.list())

    def find_key(self, key):
        print(self.container.find(key))

    def grep_keys(self, regex):
        print(self.container.grep(regex))

    def save_data(self):
        self.container.save(self.username)

    def load_data(self):
        self.container.load(self.username)

    def switch(self, new_username):
        self.username = new_username
        self.container.load(new_username)
