class ActivityLevel:
    Low = 'Low'
    Medium = 'Medium'
    High = 'High'

class Gender:
    Male = 'Male'
    Female = 'Female'

class Taste:
    Vegetarian = 'Vegetarian'
    Vegan = 'Vegan'
    Omnivorous = 'Omnivorous'

class User(object):
    def __init__(self, gender : Gender , age, weight, height, taste : Taste , activityLevel : ActivityLevel, email):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.taste = taste
        self.activityLevel = activityLevel
        self.email = email