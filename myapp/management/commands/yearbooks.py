import asyncio
import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import base, call_command

from myapp import DEPARTMENTS_MAP, models, utils

COLLAGES_PATH = os.path.join(settings.MEDIA_ROOT, 'collages')

async def get_poll_votes(polls):
    result = list()
    for p in polls:
        tmpVotes = []
        for (person,count) in p.votes.items():
            try:
                Person=models.User.objects.filter(username=person)[0].student.name
            except:
                Person=""
            tmpVotes.append((int(count),Person))
        tmpVotes.sort(reverse=True)
        ind = min(5,len(tmpVotes))
        if ind!=0:
            result.append((p.poll, tmpVotes[0:ind]))
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
        parser.add_argument(
            '--all',
            action='store_true',
            help='Batch generate all yearbooks!'
        )

    async def setup(self, **options):
        self.verbose = options['verbosity'] > 1
        output_dir = options['output']
        os.makedirs(output_dir, exist_ok=True)

    async def get_data(self, dep):
        students_dep = models.Student.objects.filter(department=dep).order_by('name')
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
            comments = list()
            for a in student.CommentsIGet:
                try:
                    c_student = models.User.objects.filter(username=a['fromWhom']).first().student.name
                    if a['comment'] and a['displayInPdf'] == 'True':
                        if a.get('showNameinPDF', 'False') == 'True':
                            val = (a['comment'], c_student)
                        else:
                            val = (a['comment'], '')
                        comments.append(val)
                except:
                    pass
            student.AnswersAboutMyself = ques_ans
            student.CommentsIGet = comments

        all_polls = await get_poll_votes(models.Poll.objects.filter(department='all'))
        dep_polls = await get_poll_votes(models.Poll.objects.filter(department=dep))

        # To deal with static loads
        domain = Site.objects.get_current().domain
        base_url = '{protocol}://{domain}'.format(
            protocol='http' if settings.DEBUG else 'https',
            domain=domain
        )

        folder = os.path.join(COLLAGES_PATH, dep)
        collage_urls = (
            '/media/collages/%s' % f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        )

        return {
            'base_url': base_url,
            'students': students_dep,
            'department': DEPARTMENTS_MAP[dep],
            'dept_photo': '/media/dept/{dep}.jpg'.format(dep=dep),
            'collage_urls': collage_urls,
            'allPolls': all_polls,
            'deptPolls': dep_polls
        }

    async def generate_dept_yearbook(self, dep, **options):
        print('==== Generating for', DEPARTMENTS_MAP[dep], '====')
        context = self.get_data(dep)
        output_dir = options['output']
        filename = 'yearbook_{dep}.pdf'.format(dep=dep)
        path = os.path.join(output_dir, filename)
        if self.verbose:
            print('V: Writing to', path)
        with open(path, 'wb') as f:
            pdf = utils.get_pdf_response('myapp/yearbook.html', 'dep', context, False, verbose=self.verbose)
            f.write(pdf)

    async def handle_async(self, *args, **options):
        await self.setup(**options)
        batch_gen = options['all']
        if batch_gen:
            asyncio.gather(*(self.generate_dept_yearbook(dep, **options) for dep in DEPARTMENTS_MAP))
        else:
            dep = options['department']
            if dep not in DEPARTMENTS_MAP:
                raise ValueError('Invalid department passed!')
            await self.generate_dept_yearbook(dep, **options)

    def handle(self, *args, **options):
        asyncio.run(self.handle_async(*args, **options))
