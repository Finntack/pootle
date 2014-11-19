#!/usr/bin/env python
"""Action that display a statistic of what translator has translated and based on what quality of suggestions"""

from pootle.scripts.actions import TranslationProjectAction, StoreAction
from pootle_project.models import Project
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()
ranges = [
    (0, 0),
    (1, 10),
    (11, 20),
    (21, 30),
    (31, 40),
    (41, 50),
    (51, 60),
    (61, 70),
    (71, 80),
    (81, 90),
    (91, 99),
    (100, 100)
]


class FtStatisticsAction(TranslationProjectAction, StoreAction):
    def __init__(self, **kwargs):
        super(FtStatisticsAction, self).__init__(**kwargs)
        self.icon = 'icon-web-translate'

    def run(self, path, root, tpdir,  # pylint: disable=R0913
            language, project, store='*', style='', **kwargs):
        project = Project.objects.get(code=project)

        OUT = '<table class="ft statistics"><tr><th>Filename</th><th>Translator</th><th>Lang</th><th>Sug. Q</th><th>WC</th></tr>'
        stores = project.get_children()
        for store in stores:
            files = store.get_children()
            for f in files:
                units = f.units.filter(state__gte=200)
                for r in ranges:
                    vals = units.filter(suggest_quality__range=r).values('submitted_by').annotate(wordcount=Sum('source_wordcount'))
                    user_wordcount = [(User.objects.get(id=x['submitted_by']).username, x['wordcount']) for x in vals]
                    for wc in user_wordcount:
                        OUT += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%i</td></tr>' % \
                               (f.name, wc[0], f.translation_project.language.code, '%i - %i%%' % r, wc[1])

        self.set_output(OUT + '</table>')


FtStatisticsAction.show = FtStatisticsAction(category="Reporting", title="View statistics")
