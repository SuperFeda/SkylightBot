from disnake import OptionChoice, Localized

CHOICE_FOR_SURE = [
    OptionChoice(Localized("Yes", key="edit_all_worker_salary.true_choice"), value=True),
    OptionChoice(Localized("No", key="edit_all_worker_salary.false_choice"), value=False)
]

CHOICE_FOR_PC_TYPE = [
    OptionChoice(name="Premium code", value="youtube_code"),
    OptionChoice(name="Common code", value="common_code")
]

CHOICE_FOR_REPORT_TYPE = [
    OptionChoice(Localized("Error message", key="send_report.error_message_choice"), value="error message"),
    OptionChoice(Localized("Complaint about an employee", key="send_report.employee_message_choice"), value="complaint about an employee")
]

CHOICE_FOR_REQUEST_TYPE = [
    OptionChoice(name="Запрос на покупку", value="покупка"),
    OptionChoice(name="Предложение", value="предложение")
]
