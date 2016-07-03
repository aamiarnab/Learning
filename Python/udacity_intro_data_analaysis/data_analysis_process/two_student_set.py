import unicodecsv
import datetime
from collections import defaultdict
import numpy as np

def describe_data(data):
    print "Mean:", np.mean(data)
    print "Standard Deviation:", np.std(data)
    print "Minimum:", np.min(data)
    print "Maximum:", np.max(data)

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def count_unique_student(filename):
    counter_set = set()
    for rec in filename:
        counter_set.add(rec['account_key'])
    return len(counter_set)

def create_paid_list(filename):
    paid_list = []
    for rec in filename:
        if rec['account_key'] in paid_students:
            paid_list.append(rec)
    return paid_list

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

def get_total_by_key(data, measure_name):
    total_by_key = {}
    for key_name, data_list in data.items():
        total_value = 0.0
        for data_point in data_list:
            total_value += float(data_point[measure_name])
        total_by_key[key_name] = total_value
    return total_by_key

def calculate_metrics(data, measure_name) :
    group_by_account = group_data(data, 'account_key')
    agg_data = get_total_by_key(group_by_account, measure_name)
    describe_data(agg_data.values())

enrollments = read_csv('../../data/enrollments.csv')
daily_engagement = read_csv('../../data/daily_engagement.csv')
project_submissions = read_csv('../../data/project_submissions.csv')

paid_students = {}
for enr_rec in enrollments:
    if enr_rec['is_udacity'] == 'False' and (enr_rec['days_to_cancel'] == '' or int(enr_rec['days_to_cancel']) > 7) :
        if enr_rec['account_key'] not in paid_students or paid_students[enr_rec['account_key']] < enr_rec['join_date']:
            paid_students[enr_rec['account_key']] = enr_rec['join_date']

paid_engagement = create_paid_list(daily_engagement)
paid_submission = create_paid_list(project_submissions)

passed_student = set()
subway_project_lesson_keys = ['746169184', '3176718735']
for rec in paid_submission:
    if rec['lesson_key'] in subway_project_lesson_keys and \
        (rec['assigned_rating'] == 'PASSED' or rec['assigned_rating'] == 'DISTINCTION') :
        passed_student.add(rec['account_key'])

passing_engagement = []
non_passing_engagement = []
for eng_rec in paid_engagement:
    acct = eng_rec['account_key']
    engagement_date = datetime.datetime.strptime(eng_rec['utc_date'] , '%d/%m/%Y')
    enrollment_date = datetime.datetime.strptime(paid_students[acct] , '%Y-%m-%d')
    if (engagement_date - enrollment_date).days< 7 and (engagement_date - enrollment_date).days >= 0:
        #added to check if visited to class
        if acct in passed_student:
            passing_engagement.append(eng_rec)
        else:
            non_passing_engagement.append(eng_rec)

#Calling code to calculate metric
print "Metrics for passing students, total_minutes_visited"
calculate_metrics(passing_engagement, 'total_minutes_visited')
print "Metrics for non passing students, total_minutes_visited"
calculate_metrics(non_passing_engagement, 'total_minutes_visited')
