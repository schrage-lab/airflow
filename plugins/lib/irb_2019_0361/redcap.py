import enum


# these are enums to make it easier to get the correct names
class Events(enum.Enum):
    """enum class for easy identification of available events in the REDCap project"""
    prescreening_arm_1 = 1
    screening_arm_1 = 2
    cognitive_testing_arm_1 = 3
    mri_structural_vis_arm_1 = 4
    ogttmri_visit_arm_1 = 5
    dexa_data_arm_1 = 6
    concomitant_medica_arm_1 = 7
    deviations_arm_1 = 8
    adverse_events_arm_1 = 9
    note_to_file_arm_1 = 10
    visit_note_arm_1 = 11
    subject_off_study_arm_1 = 12
    rescreening_arm_1 = 13
    recognitive_testin_arm_1 = 14
    remri_structural_v_arm_1 = 15
    reogttmri_visit_arm_1 = 16
    redexa_data_arm_1 = 17
    vo2max_data_arm_1 = 18
    revo2max_data_arm_1 = 19


class Forms(enum.Enum):
    """enum class for easy identification of available forms in the REDCap project"""
    insulin_resistance_in_adolescents_survey = 1
    office_use = 2
    eassent = 3
    econsent = 4
    saved_consents = 5
    demographics_survey = 6
    medical_history_survey = 7
    mri_survey = 8
    tanner_survey = 9
    par_survey = 10
    yogtt002_screening_visit_checklist = 11
    yogtt003_informed_consenthippa_authorization_docum = 12
    yogtt004_demographics = 13
    yogtt005_medical_history = 14
    yogtt006_mri_safety_questionnaire = 15
    yogtt007_3_day_physical_activity_recall = 16
    yogtt008_tanner_questionnaire = 17
    yogtt009_screening_visit_data_collection_form = 18
    yogtt010_eligibility_criteria_form = 19
    yogtt011_cognitive_study_visit_protocol_checklist = 20
    yogtt012_mri_structural_visit_checklist = 21
    yogtt013_ogtt_mri_study_visit_protocol_checklist = 22
    yogtt015_concomitant_medication_tracking_log = 23
    yogtt016_deviation_tracking_log = 24
    yogtt017_adverse_event_tracking_log = 25
    yogtt018_note_to_file = 26
    yogtt019_visit_note = 27
    yogtt020_subject_off_study = 28
    dexa_data = 29
    insulin_data = 30
    cognitive_scores = 31
    internal_audit_review_form = 32
    yogtt023_vo2max_visit_checklist = 33
    yogtt024_vo2max_data_collection_form = 34
    yogtt025_dexa_visit_checklist = 35
