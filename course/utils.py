from functools import wraps
from .models import Course

import random

# Slugs Utils
def slug_generator(string):
   return '-'.join(string.lower().split(' '))

def checking_slug(slug):
   tournaments = Course.objects.filter(slug=slug)
   
   if (tournaments.count() > 0):
      slug += str(random.randrange(10000))
      return slug 
   else:
      return slug 