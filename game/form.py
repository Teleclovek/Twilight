
from dataclasses import field, fields
from email.policy import default
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Game, Mapposition, Race, RaceDefault, Player
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 


class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password': None,
        }



class makegame(ModelForm):
    class Meta:
        model = Game
        fields = ['gamename', 'gamesize']


class addplayer(ModelForm):
    class Meta:
        model = Player
        fields = ['playername']


class draftraces(forms.Form):

    racetopool = forms.ModelChoiceField(queryset=None)
    racetoban = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):  
        self.gamepk = kwargs.pop('gamepk', None)
        self.playerid = kwargs.pop('playerid', None)
        
        self.game=Game.objects.get(pk=self.gamepk)
        self.order=self.playerid.gameorder
        self.start_of_range=(1+(4*(self.order-1)))
        self.end_of_range=(5+(4*(self.order-1)))

        super(draftraces, self).__init__(*args, **kwargs)
        self.fields['racetopool'].queryset=Race.objects.filter(game=self.game, racegameorder__in=range(self.start_of_range,self.end_of_range))
        self.fields['racetoban'].queryset=Race.objects.filter(game=self.game, racegameorder__in=range(self.start_of_range,self.end_of_range))
        self.fields['racetopool'].label = 'Rasa do poolu:'
        self.fields['racetoban'].label = 'Rasa do banu:'

class voting(forms.Form):
    racetovote = forms.ModelChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):  
        self.gamepk = kwargs.pop('gamepk', None)
        self.playerid = kwargs.pop('playerid', None)
        self.game=Game.objects.get(pk=self.gamepk)
        super(voting, self).__init__(*args, **kwargs)
        self.fields['racetovote'].queryset=Race.objects.filter(game=self.game, in_game=True, banned=False, chosen=False)
        self.fields['racetovote'].label = 'Hlas pro:'

class picking(forms.Form):
    pick = forms.ModelChoiceField(queryset=None)
    def __init__(self, *args, **kwargs):  
        self.gamepk = kwargs.pop('gamepk', None)
        self.game=Game.objects.get(pk=self.gamepk)
        super(picking, self).__init__(*args, **kwargs)
        self.fields['pick'].queryset=Race.objects.filter(game=self.game, chosen=True, taken=False)
        self.fields['pick'].label = 'Rasa:'

class picking2(forms.Form):
    pick2 = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):  
        self.gamepk = kwargs.pop('gamepk', None)
        self.game=Game.objects.get(pk=self.gamepk)
        super(picking2, self).__init__(*args, **kwargs)
        self.fields['pick2'].queryset=Mapposition.objects.filter(game=self.game, taken=False)
        self.fields['pick2'].label = 'Pozice:'

class picking3(forms.Form):
    pick3 = forms.BooleanField(required=False, initial=False, label='Speaker')
   

