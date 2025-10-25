import re
from datetime import date
import tabulate
import collections
import qrcode
import os
import PIL

GENERATIONS = [
    (1900, 1939, "pre-war generation"),
    (1940, 1945, "war generation"),
    (1946, 1964, "baby boomers"),
    (1965, 1979, "generation X"),
    (1980, 1995, "millennials"),
    (1996, 2010, "generation Z"),
    (2011, 2100, "generation Alpha")
]

FEMALE_names = {
    (1900, 1909): ["Maria", "Anna", "Elisa", "Julia", "Joanna"],
    (1910, 1919): ["Maria", "Anna", "Elisa", "Julia", "Elisabeth"],
    (1920, 1929): ["Maria", "Anna", "Yvonne", "Jeanne", "Elisa"],
    (1930, 1939): ["Maria", "Anna", "Yvonne", "Jeanne", "Marie"],
    (1940, 1949): ["Maria", "Marie", "Annie", "Yvonne", "Jeannine"],
    (1950, 1959): ["Maria", "Marie", "Annie", "Rita", "Monique"],
    (1960, 1969): ["Maria", "Martine", "Marie", "Ann", "Carine"],
    (1970, 1979): ["Kristel", "Ann", "Nancy", "Sandra", "Veerle"],
    (1980, 1989): ["Kim", "An", "Nathalie", "Wendy", "Inge"],
    (1990, 1999): ["Sarah", "Laura", "An", "Elke", "Sofie"],
    (2000, 2009): ["Emma", "Laura", "Lore", "Marie", "Lisa"],
    (2010, 2019): ["Emma", "Marie", "Elise", "Julie", "Noor"],
    (2020, 2100): ["Olivia", "Emma", "Louise", "Mila", "Nora"]
}

MALE_names = {
    (1900, 1909): ["Jan", "Jozef", "Petrus", "Frans", "August"],
    (1910, 1919): ["Jozef", "Jan", "Albert", "Frans", "August"],
    (1920, 1929): ["Jozef", "Jan", "Albert", "Marcel", "Roger"],
    (1930, 1939): ["Jozef", "Jan", "Roger", "André", "Marcel"],
    (1940, 1949): ["Jozef", "Jan", "Luc", "Marc", "André"],
    (1950, 1959): ["Marc", "Luc", "Jan", "Patrick", "Johan"],
    (1960, 1969): ["Marc", "Luc", "Patrick", "Dirk", "Johan"],
    (1970, 1979): ["Kristof", "Bart", "Tom", "Steven", "Peter"],
    (1980, 1989): ["Kevin", "Tom", "Bart", "Steven", "David"],
    (1990, 1999): ["Thomas", "Nicolas", "Kevin", "Tim", "Jonas"],
    (2000, 2009): ["Thomas", "Lucas", "Lars", "Seppe", "Wout"],
    (2010, 2019): ["Lucas", "Noah", "Liam", "Arthur", "Milan"],
    (2020, 2100): ["Noah", "Arthur", "Liam", "Louis", "Lucas"]
}

pattern = r'^(.{2})\.(.{2})\.(.{2})-(.{3})\.(.{2})$'

def is_valid_number(register_number):
    new = re.match(pattern, register_number)
    if not new:
        return False
    year , month, day, xxx , cc = new.groups()


    if not (year.isdigit() and month.isdigit() and day.isdigit() and xxx.isdigit() and cc.isdigit()):
        return False
    

    year,month,day,xxx,cc = int(year),int(month),int(day),int(xxx),int(cc)

    newNum = f'{year:02d}{month:02d}{day:02d}{xxx:03d}'

    num1900 = int(newNum)
    num2000 = int("2"+newNum)
    check_1900 = 97 - (num1900%97)
    check_2000 = 97 - (num2000%97)
    if cc == check_1900:
        year = 1900+year
    elif cc == check_2000:
        year = 2000+year
    else:
        return False
    

    try:
        DateOfBirth = date(year,month,day)
    except ValueError:
        return False
    if DateOfBirth>date.today():
        return False
    return True 

def check_number(register_number):
    
    new_list = list(register_number)

    count = 0
    
    for i in new_list:
        if i.isdigit():
            count += 1
    
    if count != 11 :
        return "invalid register number - invalid length"

    new = re.match(pattern, register_number)
    
    if not new:
        return "invalid register number - incorrect formatting"

    year , month, day, xxx , cc = new.groups()

    if not (year.isdigit() and month.isdigit() and day.isdigit() and xxx.isdigit() and cc.isdigit()):
        return "invalid register number - non-numeric characters"
    
    year,month,day,xxx,cc = int(year),int(month),int(day),int(xxx),int(cc)

    newNum = f'{year:02d}{month:02d}{day:02d}{xxx:03d}'
    num1900 = int(newNum)
    num2000 = int("2"+newNum)
    check_1900 = 97 - (num1900%97)
    check_2000 = 97 - (num2000%97)


    if cc == check_1900:
        year = 1900+year
    elif cc == check_2000:
        year = 2000+year
    else:
        return "invalid register number - check digits"
    

    try:
        DateOfBirth = date(year,month,day)
    except ValueError:
        return "invalid register number - invalid date"
    

    if DateOfBirth > date.today():
        return "invalid register number - future birth date"
    

    time_of_registration = ""

    if xxx >=1 and xxx <=100:
        time_of_registration = "(early)"
    elif xxx >= 900 and xxx <= 999:
        time_of_registration = "(late)"

    Gen = ""

    for a , b , c in GENERATIONS:
        if year >= a and year <= b:
            Gen = c
            break


    if not is_valid_number(register_number):
        return "invalid register number - check digits"
    if time_of_registration:
        return  f'valid register number {time_of_registration} - {Gen}'
    else :
        return f'valid register number - {Gen}'

def structured_info(register_number):

    new = re.match(pattern, register_number)

    year , month, day, xxx , cc = new.groups()
    
    year,month,day,xxx,cc = int(year),int(month),int(day),int(xxx),int(cc)

    newNum = f'{year:02d}{month:02d}{day:02d}{xxx:03d}'
    num1900 = int(newNum)
    num2000 = int("2"+newNum)
    check_1900 = 97 - (num1900%97)
    check_2000 = 97 - (num2000%97)


    if cc == check_1900:
        year = 1900+year
    elif cc == check_2000:
        year = 2000+year

    DateOfBirth = date(year,month,day)

    Gen = ""

    for a , b , c in GENERATIONS:
        if year >= a and year <= b:
            Gen = c
            break

    gender = ""
    if xxx % 2 == 0:
        gender = "Female"
    else :
        gender = "Male"
    
    age = date.today()-DateOfBirth
    AgeInYears = int(age.days/365)

    table = [
        ['Date of Birth',DateOfBirth.strftime("%B %d, %Y")],
        ['Gender', gender],
        ['Age',AgeInYears],
        ['Generation',Gen]
        ]
    print(tabulate.tabulate(table, tablefmt='grid'))


def generate_qr(register_number):

    picture = qrcode.make(register_number)
    file = f'{register_number}.png'
    picture.save(file)
    print("image saved")

def get_names(year, gender):
    if gender.lower() == 'female':
        for start, end in FEMALE_names:
            if year >= start and year<= end:
                return print(FEMALE_names[(start, end)])
    else:
        for start, end in MALE_names:
            if year >= start and year<= end:
                return print(MALE_names[(start, end)])



if __name__ == "__main__":
    register_number = input()
    print(check_number(register_number))
    A = input()
    if A == "table" or A == "TABLE":
        print(structured_info(register_number))
    elif A == "qr" or A == "QR" or A == "qr-code":
        print(generate_qr(register_number))
    elif A == "name" or A == "NAME" or A == "names":
        new = re.match(pattern, register_number)
        year , month, day, xxx , cc = new.groups()
        year,month,day,xxx,cc = int(year),int(month),int(day),int(xxx),int(cc)
        newNum = f'{year:02d}{month:02d}{day:02d}{xxx:03d}'
        num1900 = int(newNum)
        num2000 = int("2"+newNum)
        check_1900 = 97 - (num1900%97)
        check_2000 = 97 - (num2000%97)
        if cc == check_1900:
            year = 1900+year
        elif cc == check_2000:
            year = 2000+year
        gender = ""
        if xxx % 2 == 0:
            gender = "female"
        else :
            gender = "male"
        print(get_names(year,gender))
