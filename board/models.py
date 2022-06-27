from django.db import models
from member.models import Member
from datetime import datetime

# Create your models here.
# on_delete : CASCADE, DO_NOTHING


class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    member = models.ForeignKey(Member, related_name='board', on_delete=models.CASCADE)
    regdate = models.DateTimeField(default=datetime.now)
    views = models.IntegerField(default=0)
    contents = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'board'
        ordering = ['-regdate']

    def __str__(self):
        return self.title