import datetime

class Habit: #Object class for a habit
    def __init__(self, name):
        self.name = name
        self.start_date = datetime.date.today()
        self.days_completed = 0
        self.completed_today = False
        self.last_completed = None
        self.checkbox_rect = None

    def complete_today(self, test_delta = datetime.timedelta(days=0)):
        """marks the habit to be completed, returns a score"""
        self.days_completed += 1
        self.last_completed = datetime.date.today() + test_delta
        self.completed_today = True

        if self.days_completed == 90:
            return 5

        if self.days_completed == 7:
            return 10
        elif self.days_completed % 7 == 0 or self.days_completed% 10 == 0:
            return 5
        else:
            return 1

    def reset(self):
        """resets the habit"""
        self.completed_today = False

    def is_fully_grown(self):
        """checks if the habit is donw for over 90 days"""
        return self.days_completed >= 90

    def is_completed_today(self):
        """checks if the habit is completed today"""
        return self.completed_today 

class Player: #Object class for a player
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.habits = []  # List of Habit objects
        self.last_played = datetime.date.today()
        self.score = 0

    def add_habit(self, habit):
        """adds a habit"""
        self.habits.append(habit)

    def remove_habit(self, habit):
        """removes a habit"""
        if habit in self.habits:
            self.habits.remove(habit)
    
    def reset_habit(self):
        """Resets all habits of that player"""
        for habit in self.habits:
            habit.reset()   

    def add_score(self,score, habit):
        """adds score and removes the habit if fully grown"""
        self.score += score

        if habit.is_fully_grown():
            self.remove_habit()
