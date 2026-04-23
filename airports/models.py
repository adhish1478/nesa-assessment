from django.db import models

# Create your models here.
class AirportNode(models.Model):
    name= models.CharField(max_length=100)

    parent= models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    left= models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='left_node'
    )
    left_distance= models.IntegerField(null=True, blank=True)

    right= models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='right_node'
    )
    right_distance= models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
