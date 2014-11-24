#!/usr/bin/env python
"""Action that display a statistic of what translator has translated and based on what quality of suggestions"""
import os
from django.core.exceptions import ObjectDoesNotExist
from pootle.scripts.actions import StoreAction
from pootle_project.models import Project
from django.contrib.auth import get_user_model
from pootle_store.models import Store, TMUnit
from pootle_store.util import TRANSLATED

User = get_user_model()


class FtMoveAction(StoreAction):
    def __init__(self, **kwargs):
        super(FtMoveAction, self).__init__(**kwargs)
        self.icon = 'icon-reject'
        self.permission = "administrate"

    def run(self, **kwargs):
        pootle_path = "/%s/%s/%s" % (kwargs['language'], kwargs['project'], kwargs['store'])
        store = Store.objects.get(pootle_path=pootle_path)


        langs = store.translation_project.project.languages
        stores_to_process = []

        import pdb; pdb.set_trace()
        for lang in langs:
            pootle_path = "/%s/%s/%s" % (lang.code, kwargs['project'], kwargs['store'])

            try:
                store = Store.objects.get(pootle_path=pootle_path)
            except ObjectDoesNotExist:
                continue

            if len(store.units.filter(state__lt=TRANSLATED)) > 0:
                self.set_output('Untranslated units exist. Aborting.')
                return

            stores_to_process.append(store)

        paths_to_delete = []
        for store in stores_to_process:
            tm_store = Store.objects.get(pootle_path='/%s/TM/TM.po' % store.translation_project.language.code)
            tm_project = Project.objects.get(code='TM')
            tm_project.last_submission = None
            tm_project.save()

            for u in store.units:
                u.store = tm_store
                u.save()
                tm_unit = TMUnit.objects.get(unit=u)
                tm_unit.project = tm_project
                tm_unit.save()

            store.translation_project.last_submission = None
            store.translation_project.save()

            paths_to_delete.append(os.path.join(kwargs['root'], kwargs['project'], store.translation_project.language.code, store.name))

            store.delete()

        self.set_output(str(kwargs) + str(paths_to_delete))


FtMoveAction.show = FtMoveAction(category="Reporting", title="Move file to TM")