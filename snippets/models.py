from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS           = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES    = sorted([(item,item) for item in get_all_styles()])

class Snippet(models.Model):
    created     = models.DateField(auto_now_add=True)
    title       = models.CharField(max_length=100, blank=True, default='')
    code        = models.TextField()
    lineos      = models.BooleanField(default=False)
    language    = models.CharField(choices=LANGUAGE_CHOICES, default='python',max_length=100)
    style       = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner       = models.ForeignKey('auth.user', related_name='snippets',on_delete=models.CASCADE)
    highlighted = models.TextField()
# line 19 and the function below will save the information that is highlighted
    

    class Meta:
        ordering = ('created',)
    
    def save(self, *args, **kwargs):
# *args passes variable number of non-keyworded arguments 
# and on which operation of the tuple can be performed. 
# **kwargs passes variable number of keyword arguments dictionary to 
# function on which operation of a dictionary can be performed. 
# *args and **kwargs make the function flexible.
# Use the `pygments` library to create a highlighted HTML
# representation of the code snippet.
       lexer            = get_lexer_by_name(self.language)
       lineos           = 'table' if self.lineos else False
       options          = {'title': self.title} if self.title else{}
       formatter        = HtmlFormatter(style=self.style,lineos=lineos,full=True,**options)
       self.highlighted = highlight(self.code, lexer, formatter)
       super(Snippet,self).save(*args,**kwargs)
# The super function is used to give access to methods and properties of a 
# parent or sibling class. The super function 
# returns an object that represents the parent class.

    def __str__(self):
        return self.title