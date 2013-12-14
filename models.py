import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.db import models


class Base(models.Model):
    class Meta:
        app_label = 'main'
        abstract = True


class Expression(Base):
    text = models.CharField(max_length=75, null=False, db_index=True)
    entry_id = models.IntegerField(db_index=True)

    class Meta(Base.Meta):
        unique_together = ("text", "entry_id")

    def __str__(self):
        return "%s %s" % (self.entry_id, self.text)


class Reading(Base):
    text = models.CharField(max_length=75, null=False, db_index=True)
    entry_id = models.IntegerField(db_index=True)

    class Meta(Base.Meta):
        unique_together = ("text", "entry_id")

    def __str__(self):
        return "%s %s" % (self.entry_id, self.text)


class Sense(Base):
    text = models.TextField(null=False)
    pos = models.CharField(max_length=100, null=True)
    entry_id = models.IntegerField(db_index=True)
    sense_id = models.IntegerField(db_index=True)

    class Meta(Base.Meta):
        unique_together = [("text", "entry_id"),
                           ("sense_id", "entry_id")]

    def __str__(self):
        return "%s.%s %s" % (self.entry_id, self.sense_id, self.text)


class Association(Base):
    expression = models.ForeignKey(Expression, null=True)
    reading = models.ForeignKey(Reading, null=False)
    sense = models.ForeignKey(Sense, null=False)
    entry_id = models.IntegerField(db_index=True)
    #priorities = models.IntegerField(db_index=True, default=0)

    class Meta(Base.Meta):
        unique_together = ("expression", "reading", "sense")
        index_together = [("expression", "reading")]

    def __str__(self):
        return "%s,%s,%s" % (self.expression.text,
                             self.reading.text, self.sense.sense_id)
