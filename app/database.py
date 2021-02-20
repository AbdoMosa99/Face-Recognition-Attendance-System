from app import models

def addStudent(id, name, gender, email, university, faculty, courses, face_enc):
    faculty = Faculty.query.filter(Faculty.name == faculty).first()
    if not faculty:
        return None
    
    university = University.query.filter(University.name == university).first()
    if not university:
        return None
    
    fac_uni = UniversityHasFaculties.query.filter(and_(UniversityHasFaculties.university_id == university.id, UniversityHasFaculties.faculty_id == faculty.id)).first()
    if not fac_uni:
        return None
    
    encoding = FaceEncoding(encoding=face_enc)
    db.session.add(encoding)
    db.session.flush()
    
    student = Student(id=id, name=name, gender=gender, email=email, face_enc_id=encoding.id, fac_uni_id=fac_uni.id)
    db.session.add(student)
    db.session.flush()
    
    for course_code in courses:
        course = Course.query.filter(Course.code == course_code).first()
        if not course:
            continue
        
        student_courses = StudentEnrollment(student_id=student.id, course_id=course.id)
        db.session.add(student_courses)
    
    db.session.commit()
    addLog(f"Student {name} with ID {id} was added Successfully")
    return student.id
    
def addFaculty(fac, uni):
    university = University.query.filter(University.name == uni).first()
    if not university:
        university = University(name=uni)
        db.session.add(university)
        
    faculty = Faculty.query.filter(Faculty.name == fac).first()
    if not faculty:
        faculty = Faculty(name=fac)
        db.session.add(faculty)
        
    uni_fac = UniversityHasFaculties.query.filter(and_(university.id == UniversityHasFaculties.university_id, faculty.id == UniversityHasFaculties.faculty_id)).first()
    if not uni_fac:
        uni_fac = UniversityHasFaculties(university_id=university.id, faculty_id=faculty.id)
        db.session.add(uni_fac)
                                                  
    db.session.commit()
    addLog(f"Faculty {fac}, {uni} was added Successfully")
    return uni_fac.id
        
def addDoctor(name):
    doctor = Doctor.query.filter(Doctor.name == name).first()
    if not doctor:
        doctor = Doctor(name=name)
        db.session.add(doctor)
    
    db.session.commit()
    addLog(f"Doctor {name} with ID {doctor.id} was added Successfully")
    return doctor.id

def addCourse(code, name, semester, n_lectures, doctorName):
    doctor = Doctor.query.filter(Doctor.name == doctorName).first()
    if not doctor: 
        return None
    
    course = Course(code=code, name=name, semester=semester, n_lectures=n_lectures, doctor_id=doctor.id)
    db.session.add(course)

    db.session.commit()
    addLog(f"Course {name} with code {code} was added Successfully")
    return course.id

def addAttendance(lecture_number, course_code, student_id):
    course = Course.query.filter(Course.code == course_code).first()
    if not course:
        return None
    
    attendance = Attendance(time=datetime.now(), lecture_number=lecture_number,student_id=student_id, course_id=course.id)
    db.session.add(attendance)

    db.session.commit()
    addLog(f"Student with id {student_id} have attended lecture {lecture_number} in {course_code}")
    return attendance.id

def addLog(activity):
    log = Log(time=datetime.now(), activity=activity)
    db.session.add(log)
    db.session.commit()
    
    
# Update Functions

def updateStudent(name, gender, email, university, faculty, courses, id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return None
    
    student.name = name
    student.gender = gender
    student.email = email
    student.courses = courses

    faculty = Faculty.query.filter(Faculty.name == faculty).first()
    if not faculty:
        return None
        
    university = University.query.filter(University.name == university).first()
    if not university:
        return None
    
    fac_uni = UniversityHasFaculties.query.filter(and_(UniversityHasFaculties.university_id == university.id, UniversityHasFaculties.faculty_id == faculty.id)).first()
    if not fac_uni:
        return None
    
    student.fac_uni_id = fac_uni.id
    addLog(f"User {name} with ID {id} was updated Successfully")

    db.session.commit()
    return id

def updateCourse(code, name, semester, n_lectures, doctorName, id):
    course = Course.query.filter(Course.id == id).first()
    doctor = Doctor.query.filter(Doctor.name == doctorName).first()
    
    course.code = code
    course.name = name
    course.semester = semester
    course.n_lectures = n_lectures
    course.doctor_id = doctor.id
    addLog(f"Course {name}:{code} with ID {id} was updated Successfully")

    db.session.commit()

# Deleting Functions

def deleteStudent(id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return None

    FaceEncoding.query.filter(FaceEncoding.id == student.face_enc_id).delete()
    Student.query.filter(Student.id == id).delete()
    addLog(f"Student with ID {id} was deleted Successfully")

    db.session.commit()
    return id

def deleteFaculty(id):
    uni_fac = UniversityHasFaculties.query.filter(UniversityHasFaculties.id == id).delete()
    addLog(f"Faculty with ID {id} was deleted Successfully")
    db.session.commit()
    return id

def deleteCourse(id):
    Course.query.filter(Course.id == id).delete()
    addLog(f"Course with ID {id} was deleted Successfully")
    db.session.commit()
    return id

def deleteDoctor(id):  
    Doctor.query.filter(Doctor.id == id).delete()
    addLog(f"Doctor with ID {id} was deleted Successfully")
    db.session.commit()
    return id
    
# Getting Functions


def getStudents():
    studentObjs = Student.query.all()
    students = []
    
    for studentObj in studentObjs:        
        fac_uni = UniversityHasFaculties.query.filter(UniversityHasFaculties.id == studentObj.fac_uni_id).first()
        faculty = Faculty.query.filter(Faculty.id == fac_uni.faculty_id).first()
        university = University.query.filter(University.id == fac_uni.university_id).first()
        
        student = {}
        student["id"] = studentObj.id
        student["name"] = studentObj.name
        student["gender"] = studentObj.gender
        student["email"] = studentObj.email
        student["university"] = university.name
        student["faculty"] = faculty.name
        # student["courses"] = studentObj.courses
        
        students.append(student)
    return students

def getFaculties():
    fac_uni_objs = UniversityHasFaculties.query.all()
    faculties = []
    
    for fac_uni_obj in fac_uni_objs:        
        faculty = Faculty.query.filter(Faculty.id == fac_uni_obj.faculty_id).first()
        university = University.query.filter(University.id == fac_uni_obj.university_id).first()
        
        fac_uni = {}
        fac_uni["id"] = fac_uni_obj.id
        fac_uni["faculty"] = faculty.name
        fac_uni["university"] = university.name
        
        faculties.append(fac_uni)
        
    return faculties

def getDoctors():
    doctor_objs = Doctor.query.all()
    doctors = []
    
    for doctor_obj in doctor_objs:        
        doctor = {}
        doctor["id"] = doctor_obj.id
        doctor["name"] = doctor_obj.name
        
        doctors.append(doctor)
        
    return doctors
    
def getCourses():
    course_objs = Course.query.all()
    courses = []
    
    for course_obj in course_objs:
        doctor = Doctor.query.filter(Doctor.id == course_obj.doctor_id).first()
        
        course = {}
        course["id"] = course_obj.id
        course["name"] = course_obj.name
        course["semester"] = course_obj.semester
        course["n_lectures"] = course_obj.n_lectures
        course["doctor"] = doctor.name
        
        courses.append(course)
        
    return courses

def getAttendance():
    attendace_objs = Attendance.query.all()
    attendances = []
    
    for attendace_obj in attendace_objs:
        student = Student.query.filter(Student.id == attendace_obj.student_id).first()
        course = Course.query.filter(Course.id == attendace_obj.course_id).first()
        
        attendance = {}
        attendance["id"] = attendace_obj.id
        attendance["time"] = str(attendace_obj.time)
        attendance["student"] = student.name
        attendance["course"] = course.name
        attendance["lecture_number"] = attendace_obj.lecture_number
        
        attendances.append(attendance)
        
    return attendances
        
def getLogs():
    log_objs = Log.query.all()
    logs = []
    
    for log_obj in log_objs:
        log = {}
        log["time"] = log_obj.time
        log["activity"] = log_obj.activity
        
        logs.append(log)
        
    return logs
