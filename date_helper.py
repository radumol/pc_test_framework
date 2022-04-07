from datetime import datetime, timedelta


def get_next_2days_date():
	dt = datetime.now()
	td = timedelta(days=2)
	my_date = dt + td
	date_string = my_date.strftime('Choose %A, %B %-dth, %Y')
	return date_string