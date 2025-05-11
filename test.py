from objects import Player
import pickle

user1 = Player("deepan", "1234")

filename = f"users/{user1.username}.pkl"
with open(filename, "wb") as file:
    pickle.dump(user1, file)