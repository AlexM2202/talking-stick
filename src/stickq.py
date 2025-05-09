import threading
import discord

class StickQueue:
    def __init__(self):
        """
        Initializes the StickQueue.

        This constructor creates an empty queue and a threading.Lock to protect it.
        """
        self.queue = []
        self.lock = threading.Lock()
    
<<<<<<< HEAD
    def add(self, user: discord.User):
=======
    def add(self, user: discord.User, interaction: discord.Interaction):
>>>>>>> dev
        """
        Adds a user to the queue.

        Parameters:
            user (discord.User): The user to add.
        """
        with self.lock:
<<<<<<< HEAD
            self.queue.append(user)
=======
            self.queue.append({"user": user, "interaction": interaction})
>>>>>>> dev
    
    def pop(self):
        """
        Removes and returns the user at the front of the queue.

        Returns:
            discord.User: The user at the front of the queue.
        """
        with self.lock:
            return self.queue.pop(0)
    
    def peek(self):
        """
        Returns the user at the front of the queue without removing them.
        
        Returns:
            discord.User: The user at the front of the queue.
        """
        with self.lock:
            return self.queue[0]
        
    def is_empty(self):
        """
        Checks if the queue is empty.

        This method acquires a lock to ensure thread-safety while checking
        the length of the queue.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        with self.lock:
            return True if len(self.queue) == 0 else False
    
    def size(self):
        """
        Returns the number of users in the queue.

        This method acquires a lock to ensure thread-safety while checking
        the length of the queue.

        Returns:
            int: The number of users in the queue.
        """
        with self.lock:
            return len(self.queue)

    def get_location(self, user: discord.User):
        """
        Returns the location of the given user in the queue.

        Parameters:
            user (discord.User): The user to find the location of.

        Returns:
            int: The location of the user in the queue.
        """
        with self.lock:
<<<<<<< HEAD
            return self.queue.index(user)
=======
            for i in self.queue:
                if i["user"] == user:
                    return self.queue.index(i)
>>>>>>> dev

    def remove(self, user: discord.User):
        """
        Removes the given user from the queue.

        Parameters:
            user (discord.User): The user to remove.
        """
        with self.lock:
<<<<<<< HEAD
            self.queue.remove(user)
=======
            for i in self.queue:
                if i["user"] == user:
                    self.queue.remove(i)
>>>>>>> dev
            
    def clear(self):
        """
        Clears the queue.

        This method acquires a lock to ensure thread-safety while clearing
        the queue.
        """
        with self.lock:
            self.queue.clear()