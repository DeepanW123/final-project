import datetime

class Habit:

    all_habits = []

    def __init__(self, name):
        self.name = name
        self.start_date = datetime.date.today()
        self.days_completed = 10
        self.completed_today = False
        self.last_completed = None
        self.checkbox_rect = None
        Habit.all_habits.append(self)

    def complete_today(self):
        if self.completed_today:
            self.days_completed += 1
            self.last_completed = datetime.date.today()
            self.completed_today = True

    def reset_day(self):
        self.completed_today = False

    def is_fully_grown(self):
        return self.days_completed >= 90
    
    def completed(self):
        Habit.all_habits.remove(self)