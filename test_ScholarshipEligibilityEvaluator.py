from ScholarshipEligibilityEvaluator import Status, evaluate_scholarship

'''
Equivalência de Classes (idade):
- REJEITA (idade < 16)
- MANUAL_REVIEW (16 < idade <= 17)
- ACEITA (idade > 18)

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

def test_idade_intermediaria_deve_retornar_revisao():
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


