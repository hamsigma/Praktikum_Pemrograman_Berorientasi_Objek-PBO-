
from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC, abstractmethod

# -------------------------
# Models
# -------------------------
ScheduleEntry = Tuple[str, int, int]  # (day, start_minute, end_minute)

@dataclass
class Course:
    code: str
    name: str
    sks: int
    prerequisites: List[str]
    schedule: List[ScheduleEntry]

@dataclass
class Registration:
    student_name: str
    completed_courses: List[str]
    selected_courses: List[Course]

# -------------------------
# Abstraksi: Validation Rule
# -------------------------
class IValidationRule(ABC):
    @abstractmethod
    def validate(self, registration: Registration) -> Tuple[bool, str]:
        """Kembalikan (ok: bool, message: str)."""
        pass

# -------------------------
# Implementasi Rule
# -------------------------
class SksLimitRule(IValidationRule):
    def __init__(self, max_sks: int):
        self.max_sks = max_sks

    def validate(self, registration: Registration) -> Tuple[bool, str]:
        total = sum(c.sks for c in registration.selected_courses)
        if total > self.max_sks:
            return False, f"Total SKS ({total}) melebihi batas maksimum ({self.max_sks})."
        return True, "SKS OK."

class PrerequisiteRule(IValidationRule):
    def validate(self, registration: Registration) -> Tuple[bool, str]:
        missing = []
        completed = set(registration.completed_courses)
        for course in registration.selected_courses:
            for pre in course.prerequisites:
                if pre not in completed:
                    missing.append((course.code, pre))
        if missing:
            msgs = [f"{c} butuh {p}" for c, p in missing]
            return False, "Prasyarat tidak terpenuhi: " + ", ".join(msgs)
        return True, "Prasyarat OK."

class JadwalBentrokRule(IValidationRule):
    def validate(self, registration: Registration) -> Tuple[bool, str]:
        entries = []  # (day, start, end, course_code)
        for course in registration.selected_courses:
            for (day, s, e) in course.schedule:
                entries.append((day, s, e, course.code))
        for i in range(len(entries)):
            day_i, s_i, e_i, c_i = entries[i]
            for j in range(i+1, len(entries)):
                day_j, s_j, e_j, c_j = entries[j]
                if day_i != day_j:
                    continue
                if s_i < e_j and s_j < e_i:
                    return False, f"Jadwal bentrok antara {c_i} ({format_time(s_i)}-{format_time(e_i)}) dan {c_j} ({format_time(s_j)}-{format_time(e_j)})"
        return True, "Tidak ada jadwal bentrok."

def format_time(minutes: int) -> str:
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

# -------------------------
# Koordinator: RegistrationService
# -------------------------
class RegistrationService:
    def __init__(self, rules: List[IValidationRule]):
        # Dependency Injection: menerima daftar rule berbasis abstraksi
        self.rules = rules

    def run_registration(self, registration: Registration) -> Tuple[bool, List[str]]:
        errors = []
        for rule in self.rules:
            ok, msg = rule.validate(registration)
            if not ok:
                errors.append(msg)
        if errors:
            return False, errors
        return True, ["Validasi sukses."]

# -------------------------
# Demo / Main
# -------------------------
def minutes(h, m=0):
    return h*60 + m

def demo():
    mat101 = Course("MAT101", "Matematika Dasar", 3, [], [("Senin", minutes(9,0), minutes(11,0))])
    fis201 = Course("FIS201", "Fisika I", 4, ["MAT101"], [("Senin", minutes(10,30), minutes(12,0))])
    ifs300 = Course("IFS300", "Ilmu Komputer Lanjut", 3, ["MAT101", "FIS201"], [("Selasa", minutes(9,0), minutes(11,0))])

    reg = Registration(student_name="Ani", completed_courses=["MAT101"], selected_courses=[mat101, fis201])

    rules = [
        SksLimitRule(max_sks=24),
        PrerequisiteRule(),
        JadwalBentrokRule(),  # Challenge: tambah rule tanpa mengubah RegistrationService
    ]

    service = RegistrationService(rules=rules)

    print("--- Skenario: Menjalankan validasi dengan rule SKS, Prasyarat, dan JadwalBentrok ---")
    ok, messages = service.run_registration(reg)
    if not ok:
        print("Validasi gagal:")
        for m in messages:
            print(f"- {m}")
    else:
        print("Validasi sukses:")
        for m in messages:
            print(f"- {m}")

if __name__ == "__main__":
    demo()