


# visualizer.py

# Text-based insights (NO PLOTTING)
# Shows useful analysis instead of graphs.

class Visualizer:
    def __init__(self, dm, planner):
        self.dm = dm
        self.planner = planner

    def show_text_insights(self):
        courses = self.dm.get_courses()
        if not courses:
            print("No courses available for insights.")
            return

        print("\n====== COURSE PERFORMANCE INSIGHTS ======\n")
        details = self.planner.compute_cgpa()['details']

        # 1. Best and Weakest Course
        sorted_courses = sorted(details.items(), key=lambda x: x[1]['total'], reverse=True)

        best = sorted_courses[0]
        worst = sorted_courses[-1]

        print(f"Highest scoring course : {best[0]} ({best[1]['total']} marks)")
        print(f"Weakest scoring course : {worst[0]} ({worst[1]['total']} marks)\n")

        # 2. Difficulty vs Performance
        print("Difficulty → Performance analysis:")
        for code, info in details.items():
            diff = courses[code]['difficulty']
            total = info['total']
            status = "GOOD" if total >= 70 else "AVERAGE" if total >= 50 else "NEEDS WORK"
            print(f"- {code}: Difficulty={diff} | Score={total} | Status={status}")

        # 3. Attendance summary
        print("\nAttendance summary:")
        for code in courses:
            marks = self.dm.get_marks(code)
            att = marks.get('attendance_percent')
            given = marks.get('attendance_marks')
            if att is None: continue
            print(f"- {code}: Attendance {att}% → Attendance Marks: {given}")

        print("\n(End of Text Insights)")
