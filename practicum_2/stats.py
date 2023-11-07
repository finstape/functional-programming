from functools import reduce

students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92]},
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85]},
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94]},
    {"name": "David", "age": 24, "grades": [88, 87, 90, 78]},
    {"name": "Eve", "age": 19, "grades": [92, 80, 85, 87]},
    {"name": "Frank", "age": 18, "grades": [76, 83, 85, 89]},
    {"name": "Grace", "age": 23, "grades": [95, 96, 93, 92]},
    {"name": "Hannah", "age": 20, "grades": [84, 85, 86, 87]},
    {"name": "Ian", "age": 22, "grades": [75, 76, 77, 78]},
    {"name": "Jill", "age": 21, "grades": [92, 89, 91, 95]},
    {"name": "Kyle", "age": 22, "grades": [88, 80, 84, 86]},
    {"name": "Lana", "age": 20, "grades": [70, 72, 78, 80]},
    {"name": "Mike", "age": 23, "grades": [80, 82, 83, 85]},
    {"name": "Nora", "age": 19, "grades": [90, 92, 94, 96]},
    {"name": "Oscar", "age": 21, "grades": [73, 75, 76, 79]},
    {"name": "Penny", "age": 18, "grades": [83, 84, 86, 88]},
    {"name": "Quinn", "age": 22, "grades": [88, 90, 92, 94]},
    {"name": "Rachel", "age": 24, "grades": [75, 77, 78, 79]},
    {"name": "Steve", "age": 20, "grades": [91, 92, 93, 94]},
    {"name": "Tina", "age": 21, "grades": [82, 85, 87, 89]},
    {"name": "Artur", "age": 25, "grades": [56, 80, 87, 98]}
]

if __name__ == "__main__":

    """ Data filtering """
    age = int(input("Write current age: "))
    students_age = list(filter(lambda student: student["age"] == age, students))

    print(f"\nStudents with age {age}: ")
    for student in students_age:
        print(f"{student['name']}: {student['grades']}")

    """ Data conversion """
    students_with_avg = list(map(lambda student: {**student, "average": sum(student["grades"]) / len(student["grades"])}, students))
    overall_average = reduce(lambda cnt, student: cnt + student["average"], students_with_avg, 0) / len(students_with_avg)

    print("\nAverage grade for each student: ")
    for student in students_with_avg:
        print(f"{student['name']}: {student['average']}")

    print(f"\nAverage grade of all student: {overall_average}")

    """ Data aggregation """
    highest_average = max(map(lambda student: student["average"], students_with_avg))
    top_students = list(filter(lambda student: student["average"] == highest_average, students_with_avg))

    print(f"\nThe highest average grade among all students {highest_average}:")
    for student in top_students:
        print(f"{student['name']}: {student['grades']}")