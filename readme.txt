Using python And Django framework i developed application.
pycharm is used as a  code editor.
postgresql used for database

we can use s3 to store videos.
we can implement caching to increase performance
do indexing in database
we can use load balancer to increase performance
we can implement more security(token based Authentication)
here i am not doing any more validation
(we can add same videos multiple time,
we can add same video, tag, and subject  for same course, webinar but we have to avoid all these.

How to run project :
install Python,postgresql
crete virtual environment
pip install -m requirment.txt
crete Django project
python manage.py makemigrations, migrate
python manage.py runserver
