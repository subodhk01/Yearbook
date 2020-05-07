import os

from django.core.management import base, call_command

from myapp import DEPARTMENTS_MAP, models, utils


def get_poll_votes(polls):
    result = list()
    for p in polls:
        tmpVotes = []
        for (person,count) in p.votes.items():
            try:
                Person=models.User.objects.filter(username=person)[0].student.name
            except:
                Person=""
            tmpVotes.append([int(count),Person])
        print(tmpVotes)
        tmpVotes.sort(reverse=True)
        ind = min(5,len(tmpVotes))
        if ind!=0:
            result.append([p.poll,tmpVotes[0:ind]])
    return result

class Command(base.BaseCommand):
    help = "Generate Yearbook PDFs of given departments"

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--department',
            default='all',
            type=str,
            help='Given Department.'
        )
        parser.add_argument(
            '-o', '--output',
            default='outputs',
            type=str,
            help='Output folder'
        )

    def setup(self, **options):
        output_dir = options['output']
        os.makedirs(output_dir, exist_ok=True)

    def get_data(self, dep):
        students_dep = models.Student.objects.filter(department=dep)
        questions = models.GenQuestion.objects.all()

        for student in students_dep:
            ques_ans = list()
            for q in questions:
                try:
                    ans = student.AnswersAboutMyself[str(q.id)]
                    if ans:
                        ques_ans.append((str(q.question), ans))
                except KeyError:
                    pass

        all_polls=get_poll_votes(models.Poll.objects.filter(department='all'))
        dep_polls=get_poll_votes(models.Poll.objects.filter(department=dep))

        return {
            'students': students_dep,
            'department': DEPARTMENTS_MAP[dep],
            'allPolls': all_polls,
            'deptPolls': dep_polls
        }

    def handle(self, *args, **options):
        self.setup(**options)
        dep = options['department']
        if dep not in DEPARTMENTS_MAP:
            raise ValueError('Invalid department passed!')
        context = self.get_data(dep)
        output_dir = options['output']
        with open(os.path.join(output_dir, f'yearbook_{dep}.pdf'), 'wb') as f:
            pdf = utils.get_pdf_response('myapp/yearbook.html', 'dep', context, False)
            f.write(pdf)