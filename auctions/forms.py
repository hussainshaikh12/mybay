from django import forms

class CreateListing(forms.Form):
    title = forms.CharField(label="Title" ,max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    price = forms.CharField(label="Price" ,max_length=10, widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(label="Description" , widget=forms.Textarea(attrs={'class' : 'form-control'}))
    category = forms.CharField(label="Category" ,max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control'}), required=False)
    
    IMG_UPLOAD_CHOICE = (('ch','Choose..'),('1','Upload an Image'),('2','Load from URL'))
    upload_choice = forms.ChoiceField(choices=IMG_UPLOAD_CHOICE, widget=forms.Select(attrs={'class' : 'form-control','id':'img_choice','onchange':'onSelectChange()'}), required=False)
    img = forms.ImageField( widget=forms.FileInput(attrs={'class' : 'form-control-file','id':'browse','disabled':True}), required=False)
    img_url = forms.URLField( widget=forms.TextInput(attrs={'class' : 'form-control','id':'url','disabled':True,'placeholder':'Enter Url'}), required=False)

class listingComment(forms.Form):
    comment_title = forms.CharField(label="Add a Title", max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    comment = forms.CharField(label="Write your Comment", max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control'}))

