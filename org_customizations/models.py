from django.db import models
from organizations.models import Organization

class Verticals(models.Model):
    '''
    Create a new table to associate an organization with a vertical
    '''
    name = models.CharField(
        max_length = 255, 
        unique = True
    )
    
    class Meta:
        app_label = "org_customizations"
        verbose_name = "Vertical"
        verbose_name_plural = "Verticals"

    def __str__(self):
        return self.name         
           
class OrganizationExtraData(models.Model):
    '''
    Added new column to the organization table, the short_name in Hebrew lang
    '''
    org = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        null=False,
        related_name ='org_extra_data_id'
    )
       
    vertical = models.ManyToManyField(
        Verticals,
        null = False,
        related_name = 'vertical_id'
    )   
       
    heb_name = models.CharField(
        max_length = 255,
        unique = True,
        verbose_name = 'heb_name',
    )
    
    class Meta:
        app_label = "org_customizations"
        verbose_name = "Custom Organization"
        verbose_name_plural = "Custom Organizations"
    
    def __str__(self):
            return self.org.name
