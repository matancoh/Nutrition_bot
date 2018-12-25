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
    Omnivorous = 'normal'

class User(object):
    def __init__(self, gender, age, weight, height, taste , activityLevel , email):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.taste = taste
        self.activityLevel = activityLevel
        self.email = email