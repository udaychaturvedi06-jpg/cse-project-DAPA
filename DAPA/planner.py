

def percent_to_grade_point(p):
    if p >= 90: return 10
    if p >= 80: return 9
    if p >= 70: return 8
    if p >= 60: return 7
    if p >= 50: return 6
    if p >= 40: return 4
    return 0

class Planner:
    def __init__(self, dm):
        self.dm = dm

    def compute_course_converted_marks(self, code):
        course = self.dm.get_course(code)
        marks = self.dm.get_marks(code) or {}
        if not course: return None
        class_max = course.get('class_max',10); lab_max = course.get('lab_max',25)
        mid_max = course.get('mid_max',50); final_max = course.get('final_max',100)
       
        a = marks.get('assignment'); q = marks.get('quiz'); p = marks.get('presentation')
       
        parts = [v for v in [a,q,p] if v is not None]
        class_obt = sum(parts)/len(parts) if parts else 0.0
        att_obt = marks.get('attendance_marks') or 0.0
        mid_conv = (marks.get('mid_obtained')/mid_max)*30.0 if marks.get('mid_obtained') is not None else 0.0
        final_conv = (marks.get('final_obtained')/final_max)*30.0 if marks.get('final_obtained') is not None else 0.0
        lab_obt = 0.0  
        total = class_obt + lab_obt + att_obt + mid_conv + final_conv
        gp = percent_to_grade_point(total)
        return {'course': code, 'name': course.get('name'), 'credits': course.get('credits'),
                'class_obt': round(class_obt,2), 'attendance_obt': round(att_obt,2),
                'mid_conv': round(mid_conv,2), 'final_conv': round(final_conv,2),
                'total': round(total,2), 'grade_point': gp}

    def compute_cgpa(self):
        courses = self.dm.get_courses()
        total_points = 0.0; total_credits = 0.0; details = {}
        for code in courses:
            conv = self.compute_course_converted_marks(code)
            if conv is None: continue
            gp = conv['grade_point']; cr = float(conv.get('credits',1))
            total_points += gp * cr; total_credits += cr
            details[code] = conv
        cgpa = round(total_points/total_credits,2) if total_credits else 0.0
        return {'cgpa': cgpa, 'details': details}

    def what_if(self, overrides):
        import copy
        orig_marks = copy.deepcopy(self.dm.data.get('marks', {}))
        
        for code, changes in (overrides or {}).items():
            temp = orig_marks.get(code, {}).copy() if orig_marks.get(code) else {}
            temp.update(changes); orig_marks[code] = temp
       
        class TempDM:
            def __init__(self, courses, marks):
                self._courses = courses; self._marks = marks
            def get_courses(self): return self._courses
            def get_course(self, code): return self._courses.get(code)
            def get_marks(self, code): return self._marks.get(code, {})
        tempdm = TempDM(self.dm.get_courses(), orig_marks)
        
        temp_planner = Planner(tempdm)
        return temp_planner.compute_cgpa()

    def generate_study_plan(self, days=7, hours_per_day=4):
        
        cg = self.compute_cgpa(); weights = {}; total_w = 0.0
        for code, course in self.dm.get_courses().items():
            detail = cg['details'].get(code, {})
            percent = detail.get('total', 50)
            shortage = max(0, 60 - percent) / 60.0
            w = float(course.get('credits',1)) * float(course.get('difficulty',3)) * (1 + shortage)
            weights[code] = w; total_w += w
        plan = {}
        for d in range(1, days+1):
            allocations = {}
            for code, w in weights.items():
                frac = w/total_w if total_w else 1.0/len(weights)
                hours = round(max(0.25, hours_per_day * frac), 2)
                allocations[code] = hours
            plan[d] = allocations
        return plan
