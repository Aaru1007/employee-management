from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.aryan
collection = db.tmp

def index(request):
    return render(request, 'index.html')


def allEmp(request):
    # data = Employee.objects.all()
    data = collection.find()
    context = {'data': data}
    return render(request, 'allEmp.html', context)


def findEmp(request):
    emps = collection.find()
    if request.method == 'POST':
        empFilters = request.POST['empid']
        data = list(collection.find({
            '$or': [
                {'firstname': {'$regex': empFilters, '$options': 'i'}},
                {'lastname': {'$regex': empFilters, '$options': 'i'}},
                {'dept': {'$regex': empFilters, '$options': 'i'}}
            ]
        }))
        context = {'data': data}
    else:
        context = {'data': emps}
    return render(request, 'findEmp.html', context)


def addEmp(request):
    if request.method == 'POST':
        firstname = (request.POST['first']).capitalize()
        lastname = (request.POST['last']).capitalize()
        phone = int(request.POST['phone'])
        jd = request.POST['date']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        dept = request.POST['dept']
        role = request.POST['role']

        collection.insert_one({'id':ObjectId() ,'firstname': firstname, 'lastname': lastname, 'phone': phone, 'jd': jd, 'salary': salary, 'bonus': bonus, 'dept': dept, 'role': role, 'present_day': '0', 'absent_day': '0'})
        
        context = {'data': 1}
        return render(request, 'addEmp.html', context)

    return render(request, 'addEmp.html')

def rmEmp(request):
    emps = collection.find()
    if request.method == 'POST':
        empFilters = request.POST['empid']
        data = list(collection.find({
            '$or': [
                {'firstname': {'$regex': empFilters, '$options': 'i'}},
                {'lastname': {'$regex': empFilters, '$options': 'i'}},
                {'dept': {'$regex': empFilters, '$options': 'i'}}
            ]
        }))
        context = {'data': data}
    else:
        context = {'data': emps}
    return render(request, 'rmEmp.html', context)


def updEmp(request, id):
    data = list(collection.find({'id': ObjectId(id)}))
    context = {'data': data[0]}
    return render(request, 'updateEmp.html', context)


def delEmp(request, id):
    collection.delete_one({'id': ObjectId(id)})
    return redirect(allEmp)


def dataUpEmp(request):
    if request.method == 'POST':
        id = request.POST['id']
        firstName = (request.POST['first']).capitalize()
        lastName = (request.POST['last']).capitalize()
        phone = int(request.POST['phone'])
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        dept = request.POST['dept']
        role = request.POST['role']

        collection.update_one({'id': ObjectId(id)}, {
            '$set': {
                'firstname': firstName,
                'lastname': lastName,
                'phone': phone,
                'salary': salary,
                'bonus': bonus,
                'dept': dept,
                'role': role
            }
        })
        return redirect(updEmp, id=id)


def atdEmp(request):
    data = list(collection.find())
    context = {'data': data}
    return render(request, 'atdEmp.html', context)


def mark_attendance(request, id, status):
    date = datetime.now().strftime('%Y-%m-%d')
    attendance_exists = collection.find_one({'id': ObjectId(id), 'attendance.date': date})

    if attendance_exists:
        return redirect(atdEmp)

    if status == 1:
        collection.update_one({'id': ObjectId(id)}, {
            '$push': {
                'attendance': {
                    'date': date,
                    'status': 'present'
                }
            }
        })
    else:
        collection.update_one({'id': ObjectId(id)}, {
            '$push': {
                'attendance': {
                    'date': date,
                    'status': 'absent'
                }
            }
        })

    # Calculate present and absent days
    attendance_doc = collection.find_one({'id': ObjectId(id)})
    present_days = 0
    absent_days = 0
    for record in attendance_doc.get('attendance', []):
        if record['status'] == 'present':
            present_days += 1
        elif record['status'] == 'absent':
            absent_days += 1
    collection.update_one({'id': ObjectId(id)}, {
        '$set': {
            'present_day': present_days,
            'absent_day': absent_days
        }
    })
    return redirect(atdEmp)
