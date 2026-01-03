{
    'name': 'Vivek Hospital Management',
    'version': '1.0.0',
    'author': 'Vivek Raja',
    'summary': 'Manage hospital operations efficiently',
    'description': """
Vivek Hospital Management Module
===============================
This module helps in managing various hospital operations including patient registration, appointment scheduling, billing, and medical records.
    """,                    
    'category': 'Health',
    'depends': ['base','mail','product','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/vivek.hospital.patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appoiment_view.xml',
        'views/menus.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appoiment_view.xml',
        'views/pateint_tag_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
        'views/code_executor.xml',
        'views/mail_template.xml',
        # 'views/assets.xml',
        'report/patient_details.xml',
        'report/report.xml'
        ],                   
    'application': True,
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'images': ['static/description/icon.png'],

}