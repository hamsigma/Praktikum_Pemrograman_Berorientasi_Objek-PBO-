from dataclasses import dataclass

@dataclass
class Course:
    code: str
    sks: int
    prerequisites: list
    schedule: list  # list of (day, start_minute, end_minute)

@dataclass
class Registration:
    student_name: str
    completed_courses: list
    selected_courses: list

class ValidatorManager:
    def validate(self, registration: Registration):
        # 1. Cek SKS
        total = sum(c.sks for c in registration.selected_courses)
        if total > 24:
            print(f"Total SKS ({total}) > 24")
            return False

        # 2. Cek Prasyarat
        for course in registration.selected_courses:
            for pre in course.prerequisites:
                if pre not in registration.completed_courses:
                    print(f"Prasyarat {pre} untuk {course.code} belum dipenuhi")
                    return False

        # 3. Cek jadwal bentrok (pairwise)
        entries = []
        for course in registration.selected_courses:
            for day, s, e in course.schedule:
                entries.append((day, s, e, course.code))
        for i in range(len(entries)):
            di, si, ei, ci = entries[i]
            for j in range(i+1, len(entries)):
                dj, sj, ej, cj = entries[j]
                if di != dj:
                    continue
                if si < ej and sj < ei:
                    print(f"Bentrokan antara {ci} dan {cj}")
                    return False

        print("Validasi sukses (bad manager).")
        return True

def minutes(h, m=0):
    return h*60 + m

def demo():
    mat101 = Course("MAT101", 3, [], [("Senin", minutes(9,0), minutes(11,0))])
    fis201 = Course("FIS201", 4, ["MAT101"], [("Senin", minutes(10,30), minutes(12,0))])

    reg = Registration("Ani", ["MAT101"], [mat101, fis201])

    validator = ValidatorManager()
    print("--- Menjalankan validator_bad ---")
    validator.validate(reg)

if __name__ == "__main__":
    demo()