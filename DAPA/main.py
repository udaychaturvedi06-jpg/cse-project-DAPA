

from data_manager import DataManager
from planner import Planner
from visualizer import Visualizer
import json, os

def print_header(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

def pretty(d): print(json.dumps(d, indent=2))

def main():
    dm = DataManager('dapa_data.json')
    planner = Planner(dm)
    viz = Visualizer(dm, planner)

    
    if not dm.get_courses():
        dm.add_or_update_course('CS101','Intro to Programming',3,3)
        dm.add_or_update_course('MA102','Calculus',4,4)
        dm.add_or_update_course('EC103','Digital Systems',3,3)
        dm.enter_marks('CS101', assignment=8, quiz=7, presentation=9, attendance_percent=92, mid_obtained=35, final_obtained=78)
        dm.enter_marks('MA102', assignment=6, quiz=8, presentation=7, attendance_percent=85, mid_obtained=28, final_obtained=64)
        dm.enter_marks('EC103', assignment=9, quiz=9, presentation=8, attendance_percent=97, mid_obtained=40, final_obtained=85)

    while True:
        print_header(" Dynamic Academic Planner ")
        print("1. Course Manager (Add / Update Course)")
        print("2. Enter Course Marks")
        print("3. Predict GPA / CGPA ")
        print("4. Generate Study Plan")
        print("5. Show Insights ")
        print("6. Export Summary")
        print("0. Exit")

        ch = input("Choice: ").strip()

        if ch == "1":
            line = input("Quick add (CODE,Name,credits,difficulty) or Enter: ").strip()
            if line:
                try:
                    code,name,cr,diff = [x.strip() for x in line.split(",")]
                    dm.add_or_update_course(code, name, float(cr), int(diff))
                except:
                    print("Invalid quick format.")
            else:
                code = input("Course code: ")
                name = input("Name: ")
                cr = float(input("Credits: "))
                diff = int(input("Difficulty 1-5: "))
                dm.add_or_update_course(code, name, cr, diff)
            print("Saved.")

        elif ch == "2":
            code = input("Course code: ")
            if not dm.get_course(code):
                print("Course not found.")
                continue
            a = input("Assignment: "); q = input("Quiz: "); p = input("Presentation: ")
            att = input("Attendance %: "); mid = input("Mid (50): "); fin = input("Final (100): ")
            dm.enter_marks(code,
                assignment=float(a) if a else None,
                quiz=float(q) if q else None,
                presentation=float(p) if p else None,
                attendance_percent=float(att) if att else None,
                mid_obtained=float(mid) if mid else None,
                final_obtained=float(fin) if fin else None
            )
            print("Marks saved.")

        elif ch == "3":
            result = planner.compute_cgpa()
            pretty(result)

            if input("Run what-if? (y/N): ").lower() == 'y':
                overrides={}
                while True:
                    cd=input("Override course (blank to stop): ")
                    if not cd: break
                    field=input("Field to override: ")
                    val=input("Value: ")
                    try: 
                        overrides.setdefault(cd,{})[field]=float(val)
                    except:
                        print("Invalid"); continue
                preview=planner.what_if(overrides)
                print("Preview:")
                pretty(preview)

        elif ch == "4":
            days=int(input("Days until exam: ") or 7)
            hrs=float(input("Study hours/day: ") or 4)
            plan=planner.generate_study_plan(days,hrs)
            pretty(plan)

        elif ch == "5":
            viz.show_text_insights()

        elif ch == "6":
            j,c = dm.export_summary()
            print("Exported:", j, c)

        elif ch == "0":
            print("GoodLuck.")
            break

        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    main()
