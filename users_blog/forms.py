from django import forms

# Creating a form using "forms.Form":

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # This type of field is rendered as an "<input type='text'>" HTML element.
    email = forms.EmailField() # To insert the author's email.
    to = forms.EmailField() # To insert the destinatary's email.
    comments = forms.CharField(required=False, widget=forms.Textarea) # We've used "widget=forms.Textarea" to display this as a <textarea> 
    # HTML element, instead of a default <input> HTML element.

    # Note: The default "widget" (from every field), can be overridden with the "widget" attribute.

####################################################################################################################################

# Creating a from using "forms.ModelForm":

from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")

#  Note: To create a form from a model (this is, using "forms.ModelFrom"), inside "Meta" class we just need to indicate which model to use to build the form.
#  Django introspects the model and builds the form dynamically for you.