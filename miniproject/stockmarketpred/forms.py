from django import forms


class SignupForm(forms.Form):
    email = forms.EmailField()
    fname = forms.CharField()
    lname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)


class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MyForm(forms.Form):
    dropdown = forms.ChoiceField(
        label="Select a stock:",    
        choices=( 
        ('ACC', 'ACC Ltd.'), 
        ('AMBUJACEM', 'Ambuja Cements'),
        ('APOLLOHOSP', 'Apollo Hospitals Enterprises'),
        ('BRITANNIA', 'Britannia Industries'),
        ('BOSCHLTD', 'Bosch Ltd.'),
        ('CASTROLIND', 'Castrol India'),
        ('COALINDIA', 'Coal India'),
        ('GRASIM', 'Grasim Industries'),
        ('HDFCBANK', 'HDFC Bank'),
        ('HINDUNILVR', 'Hindustan Unilever'),
        ('ITC', 'ITC Ltd.'),
        ('INFY', 'Infosys'),
        ('LTIM', 'LTIMindTree Ltd.'),
        ('LT', 'Larsen & Toubro'),
        ('MARICO', 'Marico Ltd.'),
        ('Maruti', 'Maruti Suzuki India'),
        ('OIL', 'Oil India'),
        ('RELIANCE', 'Reliance Industries'),
        ('TCS', 'Tata Consultancy Services'),
        ('TITAN', 'Titan Company Ltd.'),
    ))

class FeedbackForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)