

import json
from datetime import datetime

class DataManager:
    def __init__(self, filename='DAPA/dapa_data.json'):
        self.filename = filename
        self.data = {'courses': {}, 'marks': {}}
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.save()
        return self.data

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_or_update_course(self, code, name, credits, difficulty,
                             class_max=10, lab_max=25, mid_max=50, final_max=100, attendance_max=5):
        self.data.setdefault('courses', {})
        self.data['courses'][code] = {
            'name': name,
            'credits': float(credits),
            'difficulty': int(difficulty),
            'class_max': float(class_max),
            'lab_max': float(lab_max),
            'mid_max': float(mid_max),
            'final_max': float(final_max),
            'attendance_max': float(attendance_max)
        }
        self.data.setdefault('marks', {})
        self.data['marks'].setdefault(code, {
            'assignment': None, 'quiz': None, 'presentation': None,
            'attendance_percent': None, 'attendance_marks': None,
            'mid_obtained': None, 'final_obtained': None
        })
        self.save()

    def get_courses(self):
        return self.data.get('courses', {})

    def get_course(self, code):
        return self.data.get('courses', {}).get(code)

    def get_marks(self, code):
        return self.data.get('marks', {}).get(code)

    def enter_marks(self, code, assignment=None, quiz=None, presentation=None, attendance_percent=None, mid_obtained=None, final_obtained=None):
        if code not in self.data.get('courses', {}):
            raise KeyError('Course not found. Add course first.')
        scheme = self.data['courses'][code]
        marks = self.data.setdefault('marks', {}).setdefault(code, {
            'assignment': None, 'quiz': None, 'presentation': None,
            'attendance_percent': None, 'attendance_marks': None,
            'mid_obtained': None, 'final_obtained': None
        })
        if assignment is not None: marks['assignment'] = float(assignment)
        if quiz is not None: marks['quiz'] = float(quiz)
        if presentation is not None: marks['presentation'] = float(presentation)
        if attendance_percent is not None:
            ap = float(attendance_percent); marks['attendance_percent'] = ap
            am = float(scheme.get('attendance_max', 5.0))
            if ap >= 95: att_marks = am
            elif ap >= 90: att_marks = round(am*4/5,2)
            elif ap >= 85: att_marks = round(am*3/5,2)
            elif ap >= 80: att_marks = round(am*2/5,2)
            elif ap >= 75: att_marks = round(am*1/5,2)
            else: att_marks = 0.0
            marks['attendance_marks'] = att_marks
        if mid_obtained is not None: marks['mid_obtained'] = float(mid_obtained)
        if final_obtained is not None: marks['final_obtained'] = float(final_obtained)
        self.data['marks'][code] = marks
        self.save()
        return marks

    def export_summary(self, out_json='DAPA/dapa_summary.json', out_csv='DAPA/dapa_summary.csv'):
        # write JSON
        with open(out_json, 'w') as f:
            json.dump(self.data, f, indent=2)
        # write CSV
        import csv
        with open(out_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['code','name','credits','assignment','quiz','presentation','attendance_percent','attendance_marks','mid_obtained','final_obtained'])
            for code, c in self.get_courses().items():
                m = self.get_marks(code) or {}
                writer.writerow([code, c.get('name'), c.get('credits'),
                                 m.get('assignment'), m.get('quiz'), m.get('presentation'),
                                 m.get('attendance_percent'), m.get('attendance_marks'),
                                 m.get('mid_obtained'), m.get('final_obtained')])
        return out_json, out_csv
