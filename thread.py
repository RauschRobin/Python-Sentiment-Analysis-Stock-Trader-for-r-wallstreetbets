'''
This class represents a new reddit post. Each post is an instance of thread. The thread only consists of its title.
'''
class Thread:
    def __init__(self, title):
        '''
        This is the constructor. It sets the title of the thread.

        Parameters:
        title: string

        Returns:
        Nothing
        '''
        self.title = title