from airflow import DAG
from airflow.utils.task_group import TaskGroup
from datetime import datetime
from operators.redcap import Redcap2DbOperator
from plugins.lib.common import redcap_api as api
from plugins.lib.irb_2019_0361 import redcap


with DAG('2019_0361_etl_dag', schedule_interval=None, start_date=datetime(2021, 8, 1), catchup=False) as dag:
    CONN_ID = 'schrage_lab_db'

    with TaskGroup(group_id='extract') as extract_tg:
        extract_prescreening_survey = Redcap2DbOperator(
            task_id='extract-prescreening-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_prescreening_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.insulin_resistance_in_adolescents_survey.name],
                'events': [
                    redcap.Events.prescreening_arm_1.name
                ]
            }
        )

        # this extracts data from select screening forms that were originally completed in-person but were later
        # replaced by online survey
        extract_yogtt004_demographics = Redcap2DbOperator(
            task_id='extract-yogtt004_demographics',
            conn_id=CONN_ID,
            table='irb_2019_0361_yogtt004_demographics_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt004_demographics.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_yogtt005_medical_history = Redcap2DbOperator(
            task_id='extract-yogtt005-medical-history',
            conn_id=CONN_ID,
            table='irb_2019_0361_yogtt005_medical_history_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt005_medical_history.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_yogtt006_mri_safety_questionnaire = Redcap2DbOperator(
            task_id='extract-yogtt006-mri-safety-questionnaire',
            conn_id=CONN_ID,
            table='irb_2019_0361_yogtt006_mri_safety_questionnaire_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt006_mri_safety_questionnaire.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_yogtt007_3_day_physical_activity_recall = Redcap2DbOperator(
            task_id='extract-yogtt007-3-day-physical-activity-recall',
            conn_id=CONN_ID,
            table='irb_2019_0361_yogtt007_3_day_physical_activity_recall_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt007_3_day_physical_activity_recall.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_yogtt008_tanner_questionnaire = Redcap2DbOperator(
            task_id='extract-yogtt008_tanner_questionnaire',
            conn_id=CONN_ID,
            table='irb_2019_0361_yogtt008_tanner_questionnaire_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt008_tanner_questionnaire.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        # this extracts all data from the online screening process that changed 2020
        extract_demographics_survey = Redcap2DbOperator(
            task_id='extract-demographics-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_demographics_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.demographics_survey.name
                  ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_medical_history_survey = Redcap2DbOperator(
            task_id='extract-medical-history-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_medical_history_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.medical_history_survey.name
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_mri_survey = Redcap2DbOperator(
            task_id='extract-mri-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_mri_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.mri_survey.name,
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_par_survey = Redcap2DbOperator(
            task_id='extract-par-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_par_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.par_survey.name
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_tanner_survey = Redcap2DbOperator(
            task_id='extract-tanner-survey',
            conn_id=CONN_ID,
            table='irb_2019_0361_tanner_survey_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.tanner_survey.name
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        # this extracts the forms/data related to conducting the in-person screening
        extract_screening_data = Redcap2DbOperator(
            task_id='extract-screening-data',
            conn_id=CONN_ID,
            table='irb_2019_0361_screening_data_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt002_screening_visit_checklist.name,
                    redcap.Forms.yogtt009_screening_visit_data_collection_form.name,
                    redcap.Forms.yogtt010_eligibility_criteria_form.name
                ],
                'events': [
                    redcap.Events.screening_arm_1.name,
                    redcap.Events.rescreening_arm_1.name
                ]
            }
        )

        extract_cognitive_data = Redcap2DbOperator(
            task_id='extract-cognitive-data',
            conn_id=CONN_ID,
            table='irb_2019_0361_cognitive_data_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt011_cognitive_study_visit_protocol_checklist.name,
                    redcap.Forms.cognitive_scores.name
                ],
                'events': [
                    redcap.Events.cognitive_testing_arm_1.name,
                    redcap.Events.recognitive_testin_arm_1.name
                ]
            }
        )

        extract_mri_structural_data = Redcap2DbOperator(
            task_id='extract-mri-structural-data',
            conn_id=CONN_ID,
            table='irb_2019_0361_mri_structural_data_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt012_mri_structural_visit_checklist.name
                ],
                'events': [
                    redcap.Events.mri_structural_vis_arm_1.name,
                    redcap.Events.remri_structural_v_arm_1.name
                ]
            }
        )

        extract_ogtt_data = Redcap2DbOperator(
            task_id='extract-ogtt-data',
            conn_id=CONN_ID,
            table='irb_2019_0361_ogtt_data_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.yogtt013_ogtt_mri_study_visit_protocol_checklist.name,
                    redcap.Forms.insulin_data.name
                ],
                'events': [
                    redcap.Events.ogttmri_visit_arm_1.name,
                    redcap.Events.reogttmri_visit_arm_1.name
                ]
            }
        )

        extract_dexa_data = Redcap2DbOperator(
            task_id='extract-dexa-data',
            conn_id=CONN_ID,
            table='irb_2019_0361_dexa_data_STG',
            python_callable=api.export_records,
            op_kwargs={
                'fields': ['record_id'],
                'forms': [
                    redcap.Forms.dexa_data.name
                ],
                'events': [
                    redcap.Events.dexa_data_arm_1.name,
                    redcap.Events.redexa_data_arm_1.name
                ]
            }
        )