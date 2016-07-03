import unicodecsv

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('../../data/enrollments.csv')
daily_engagement = read_csv('../../data/daily_engagement.csv')
project_submissions = read_csv('../../data/project_submissions.csv')

### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.

#New function to count unique students
def count_unique_student(file_name, key):
    counter_set = set()
    for rec in file_name:
        counter_set.add(rec[key])
    return len(counter_set)

enrollment_num_rows = len(enrollments)
print "Number of rows in enrollment:", enrollment_num_rows
enrollment_num_unique_students = count_unique_student(enrollments, 'account_key')
print "Number of unique students in enrollment:", enrollment_num_rows

engagement_num_rows = len(daily_engagement)
print "Number of rows in daily engagement:", engagement_num_rows
engagement_num_unique_students = count_unique_student(daily_engagement, 'account_key')
print "Number of unique students in daily engagement:", engagement_num_unique_students

print "Daily engagement account key:", daily_engagement[0]['account_key']

submission_num_rows = len(project_submissions)
print "Number of rows in submission:", submission_num_rows
submission_num_unique_students = count_unique_student(project_submissions, 'account_key')
print "Number of unique students in submission:", submission_num_unique_students
