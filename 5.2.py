# Mock data for completed contracts
completed_contracts = [
    {'monster': 'Грифон', 'reward': 150, 'date': '2023-01-10'},
    {'monster': 'Вампайр', 'reward': 200, 'date': '2023-02-05'},
    {'monster': 'Медведь', 'reward': 100, 'date': '2023-03-15'}
]

@app.route('/generate_report')
def generate_report():
    if session.get('rank') != 'Master':
        return "Доступ запрещен", 403

    # Create CSV report
    report_data = "Монстр, Вознаграждение, Дата\n"
    for contract in completed_contracts:
        report_data += f"{contract['monster']}, {contract['reward']}, {contract['date']}\n"

    response = app.response_class(
        response=report_data,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=completed_contracts.csv"}
    )
    return response