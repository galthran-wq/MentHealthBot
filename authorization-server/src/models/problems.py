from enum import Enum

class Problem():
    def __init__(self, name, button):
        self.name = name
        self.button = button
        self.short = button.split("_")[0]


class Problems(Enum):
    TIRED = Problem("Выгорание и переутомление", "tired_problem_button")
    DEPRESSIVE = Problem("Депрессивные состояния", "depressive_problem_button")
    SELF = Problem("Личные отношения", "self_problem_button")
    KIN = Problem("Проблемы с родственниками", "kin_problem_button")
    SURROUND = Problem("Конфликты с окружающими", "surround_problem_button")
    NUTRITION = Problem("Расстройства пищевого поведения",
                        "nutrition_problem_button")
    ADAPTATION = Problem("Проблемы адаптации", "adaptation_problem_button")
    LGBT = Problem("Проблемы LGBT+ community", "LGBT_problem_button")
    ANXIETY = Problem("Тревожность", "anxiety_problem_button")
