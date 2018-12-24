class ActivityLevel:
    Low = 'low'
    Medium = 'medium'
    High = 'high'

class Gender:
    Male = 'male'
    Female = 'female'

class Taste:
    Vegetarian = 'vegetarian'
    Vegan = 'vegan'
    Omnivorous = 'omnivorous'

class User(object):
    def __init__(self, gender : Gender , age, weight, height, taste : Taste , activityLevel : ActivityLevel, email):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.taste = taste
        self.activityLevel = activityLevel
        self.email = email