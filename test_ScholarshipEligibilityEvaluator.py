import pytest

from ScholarshipEligibilityEvaluator import Status, evaluate_scholarship

'''
Equivalência de Classes (idade):
- REJEITA (idade < 16)
- MANUAL_REVIEW (16 <= idade <= 17)
- ACEITA (idade >= 18)

Testar: idade = 15, idade = 16, idade = 17, idade = 18
Técnicas: Equivalence Partitioning Class e Boundary-Value Analysis
'''

def test_sem_idade_minima_deve_rejeitar():
    result = evaluate_scholarship(
        age=15,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.REJECTED
    assert "Applicant is younger than the minimum age." in result.reasons

def test_idade_no_limite_inferior_da_classe_intermediaria_deve_revisar():
    result = evaluate_scholarship(
        age=16,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "Applicant is under 18 and requires manual review." in result.reasons

def test_idade_intermediaria_deve_revisar():
    result = evaluate_scholarship(
        age=17,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "Applicant is under 18 and requires manual review." in result.reasons

def test_sem_motivos_de_rejeicao_nem_revisao_deve_aceitar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.APPROVED
    assert "Applicant meets all scholarship requirements." in result.reasons

'''
Equivalência de Classes (gpa):
- INVÁLIDO (gpa < 0.0)
- REJEITA (0.0 <= gpa < 6.0)
- MANUAL_REVIEW (6.0 <= gpa < 7.0)
- ACEITA (7.0 <= idade <= 10.0)
- INVÁLIDO (gpa > 10.0)

Testar: gpa = 5.9, gpa = 6.0, gpa = 6.5, gpa = 7.0
Técnicas: Equivalence Partitioning Class e Boundary-Value Analysis
'''

def test_sem_gpa_minimo_deve_rejeitar():
    result = evaluate_scholarship(
        age=18,
        gpa=5.9,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.REJECTED
    assert "GPA is below the minimum required." in result.reasons

def test_gpa_no_limite_inferior_deve_revisar():
    result = evaluate_scholarship(
        age=18,
        gpa=6.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "GPA is in the manual review range." in result.reasons

def test_gpa_intermediario_deve_revisar():
    result = evaluate_scholarship(
        age=18,
        gpa=6.5,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "GPA is in the manual review range." in result.reasons

'''
Equivalência de Classes (attendance_rate):
- INVÁLIDO (attendance_rate < 0.0)
- REJEITA (0.0 <= attendance_rate < 75.0)
- MANUAL_REVIEW (75.0 <= attendance_rate < 80.0)
- ACEITA (80.0 <= attendance_rate <= 100.0)
- INVÁLIDO (attendance_rate > 100.0)

Testar: attendance_rate = 74.0, attendance_rate = 75.0, attendance_rate = 78.0, attendance_rate = 80.0
Técnicas: Equivalence Partitioning Class e Boundary-Value Analysis
'''

def test_sem_attendance_rate_minimo_deve_rejeitar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=74.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.REJECTED
    assert "Attendance rate is below the minimum required." in result.reasons

def test_attendance_rate_no_limite_inferior_deve_revisar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=75.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "Attendance rate is in the manual review range." in result.reasons

def test_attendance_rate_intermediario_deve_revisar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=78.0,
        has_required_courses=True,
        disciplinary_record=False
    )

    assert result.status == Status.MANUAL_REVIEW
    assert "Attendance rate is in the manual review range." in result.reasons

'''
(has_required_courses):
- REJEITA (as_required_courses == False)
- ACEITA (has_required_courses == True)

Testar: has_required_courses = False, has_required_courses = True
Técnica: Logical and Decision coverage 
'''

def test_falta_has_required_courses_deve_rejeitar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=False,
        disciplinary_record=False
    )

    assert result.status == Status.REJECTED
    assert "Required courses have not been completed." in result.reasons

'''
(disciplinary_record):
- REJEITA (disciplinary_record == True)
- ACEITA (disciplinary_record == False)

Testar: disciplinary_record = True, disciplinary_record = False 
Técnica: Logical and Decision coverage 
'''

def test_possui_disciplinary_record_deve_rejeitar():
    result = evaluate_scholarship(
        age=18,
        gpa=8.0,
        attendance_rate=90.0,
        has_required_courses=True,
        disciplinary_record=True
    )

    assert result.status == Status.REJECTED
    assert "Applicant has a disciplinary record." in result.reasons

def test_gpa_invalido_raises_value_error():
    with pytest.raises(ValueError, match="GPA must be between 0 and 10."):
        evaluate_scholarship(
            age=18,
            gpa=10.1,
            attendance_rate=90.0,
            has_required_courses=True,
            disciplinary_record=False
        )
    

def test_attendance_rate_invalido_raises_value_error():
    with pytest.raises(ValueError, match="Attendance rate must be between 0 and 100."):
        evaluate_scholarship(
            age=18,
            gpa=8.0,
            attendance_rate=100.1,
            has_required_courses=True,
            disciplinary_record=False
        )

def test_rejeitar_deve_ter_precedencia_sobre_revisao():
    result = evaluate_scholarship(
		age=17,
		gpa=8.0,
		attendance_rate=90.0,
		has_required_courses=True,
		disciplinary_record=True
	)

    assert result.status == Status.REJECTED

def test_multiplos_motivos_de_rejeicao():
    result = evaluate_scholarship(
        age=15,
        gpa=5.0,
        attendance_rate=70.0,
        has_required_courses=False,
        disciplinary_record=True,
    )

    assert len(result.reasons) > 1
    assert result.status == Status.REJECTED
