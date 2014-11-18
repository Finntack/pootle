# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import connection, models


class Migration(SchemaMigration):
    depends_on = ()

    no_dry_run = True

    def forwards(self, orm):
        # First we check whether the migration is needed.
        db.add_column(u'pootle_store_unit', 'suggest_quality',
                      self.gf('django.db.models.fields.SmallIntegerField')(db_index=False, default=0),
                      keep_default=False)

    def backwards(self, orm):
        raise NotImplementedError

    complete_apps = ["pootle_store"]