from django import forms

GENDER_CHOICES = (
    ("Male", "Man"),
    ("Female", "Woman"),
    ("Lesbian", "Lesbian"),
    ("Gay", "Gay"),
    ("Transgender", "Transgender"),
    ("Non-Conforming", "Non Conforming"),
    ("LGBT", "LGBT"),
)

IDENTITY_CHOICES = (
    ("Arab", "Arab"),
    ("Asian", "Asian"),
    ("Black", "Black"),
    ("Hispanic", "Hispanic"),
    ("Jewish", "Jewish"),
    ("White", "White"),
    ("Other Ethnicity", "Other Ethnicity")
)

RELIGION_CHOICES = (
    ("Jewish", "Jewish"), ("Buddhist", "Buddhist"), ("Catholic","Catholic"), ("Hindu", "Hindu"), 
    ("Jehovah's Witness", "Jehovah's Witness"), ("Muslim", "Muslim"), ("Other Religion", "Other Religion")
)


class GenderForm(forms.Form):    
    gender_form = forms.MultipleChoiceField(choices=GENDER_CHOICES, widget=forms.CheckboxSelectMultiple(), required=False, label="Gender/Sexuality", label_suffix=":\t")


class IdentityForm(forms.Form):
    identity_form = forms.MultipleChoiceField(choices=IDENTITY_CHOICES, widget=forms.CheckboxSelectMultiple(), required=False, label="Race/Ethnicity", label_suffix=":\t")


class ReligionForm(forms.Form):
    religion_form = forms.MultipleChoiceField(choices=RELIGION_CHOICES, widget=forms.CheckboxSelectMultiple(), required=False, label="Religion", label_suffix=":\t")
