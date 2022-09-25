from audioop import reverse
from contextlib import redirect_stderr
from distutils.command.build_scripts import first_line_re
from email import message
from email.policy import default
from importlib.metadata import requires
from pyexpat.errors import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Player, Race, Game, RaceDefault, Mapposition
from .form import makegame, addplayer, draftraces, picking2, voting, picking, picking2, picking3, CreatUserForm
from django.http import HttpResponseRedirect
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import git
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("kopriva.pythonanywhere.com/") 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

def registerpage(request):
    form = CreatUserForm()
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('mainpageurl')


    return render(request, "register.html", {'form':form})

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')     
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('mainpageurl')          

    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('loginurl')

@login_required(login_url='loginurl')
def mainpage(request):
    
    return render(request, "mainpage.html",)

@login_required(login_url='loginurl')
def newgame(request):
    if request.method == "POST":
        form = makegame(request.POST)
        if form.is_valid():
            gameid = form.save()
            gamepk = gameid.pk
            number_of_players = gameid.gamesize
            races_per_player = 4
            default_rand_list = list(range(1,RaceDefault.objects.filter(default=True).count()+1))       
            random.shuffle(default_rand_list)
            for mapposition in range(number_of_players):
                Mapposition.objects.create(position=mapposition+1, game=gameid)
            order=0
            for each in RaceDefault.objects.filter(default=True):
                
                in_game_changer = False
                if default_rand_list[order] <= number_of_players*races_per_player:
                    in_game_changer = True

                Race.objects.create(racename=each.racename, game=gameid, racegameorder=default_rand_list[order], in_game=in_game_changer)
                order += 1
            
            # hned pridam zakladjiciho hrace
            player = request.user
            gamesize=gameid.gamesize
            count_p_in_game = Player.objects.filter(game=gameid).count()
            if count_p_in_game >= gamesize:
                return render(request, "newplayer.html", {'gameid':gameid, 'toomanyplayers':'HRA JE PLNA! Mas smulu!'})
            dont_exist=True
            while dont_exist == True:
                rand_order = random.randint(1, gamesize)
                dont_exist = Player.objects.filter(game=gameid, gameorder=rand_order).exists()
            playerobject = Player(playername=player, game=gameid, gameorder=rand_order)
            playerobject.save()
            return HttpResponseRedirect(reverse('drafturl', args=(gamepk,)))
    else: 
        form = makegame()   
    return render(request, "newgame.html", {'form':form})


@login_required(login_url='loginurl')
def joingame(request):
    player = request.user
    #liste her ve ktere jiz hrac je
    my_games = Player.objects.filter(playername=player).values_list('game', flat=True)
    my_games_list=list(my_games)
    my_games_names=[]
    for each in my_games_list:
        my_games_names.append(Game.objects.get(pk=each).gamename)    

    if request.method == "POST":
        gamename = request.POST.get('gamename')
        if Game.objects.filter(gamename=gamename).exists():
            gameid = Game.objects.get(gamename=gamename)
            gamepk = gameid.pk
            
            if Player.objects.filter(game=gameid, playername=player).exists():
                #hrac uz je ve hre
                return HttpResponseRedirect(reverse('drafturl', args=(gamepk,)))
            else:
                gamesize=gameid.gamesize
                count_p_in_game = Player.objects.filter(game=gameid).count()
                if count_p_in_game >= gamesize:
                    return render(request, "newplayer.html", {'gameid':gameid, 'toomanyplayers':'HRA JE PLNA! Mas smulu!'})
                dont_exist=True
                while dont_exist == True:
                    rand_order = random.randint(1, gamesize)
                    dont_exist = Player.objects.filter(game=gameid, gameorder=rand_order).exists()
                playerobject = Player(playername=player, game=gameid, gameorder=rand_order)
                playerobject.save()


                return HttpResponseRedirect(reverse('drafturl', args=(gamepk,)))
        else:
            return render(request, "joingame.html", {'nogame':'Taková hra neexistuje!'})
    return render(request, "joingame.html", {'my_games': my_games_names})

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# PRIDAT join game na menu, vyber her v kterych jsems

@login_required(login_url='loginurl')
def newplayer(request, gamepk):
    gameid=Game.objects.get(pk=gamepk)
    if request.method == "POST":
        form = addplayer(request.POST)
        if form.is_valid():
            playerid = form.save(commit=False)
            playerid.game = gameid  
            gamesize=gameid.gamesize
            count_p_in_game = Player.objects.filter(game=gameid).count()
            if count_p_in_game >= gamesize:
                return render(request, "newplayer.html", {'form':form, 'gameid':gameid, 'toomanyplayers':'HRA JE PLNA! Mas smulu!'})
            dont_exist=True
            while dont_exist == True:
                rand_order = random.randint(1, gamesize)
                dont_exist = Player.objects.filter(game=gameid, gameorder=rand_order).exists()
             
            playerid.gameorder = rand_order
            playerid.save()
            return HttpResponseRedirect(reverse('drafturl', args=(gamepk, playerid)))
    else: 
        form = addplayer()   
    return render(request, "newplayer.html", {'form':form, 'gameid':gameid})

@login_required(login_url='loginurl')
def draft(request, gamepk):
    gameid=Game.objects.get(pk=gamepk)
    user = request.user
    playerid = Player.objects.get(playername=user, game=gameid)
    if playerid.drafted == True:
        if playerid.voted == True:
            return HttpResponseRedirect(reverse('finalpickurl', args=(gamepk,)))
        else:
            return HttpResponseRedirect(reverse('poolvotingurl', args=(gamepk,)))
    else:
        all_players=Player.objects.filter(game=gameid).order_by('gameorder')
        if request.method == "POST":
            form = draftraces(request.POST, gamepk=gamepk, playerid=playerid)
            if form.is_valid():
                
                racetopool=form.cleaned_data['racetopool']
                racetoban=form.cleaned_data['racetoban']

                if racetoban == racetopool:
                    return render(request, "draft.html", {'form':form, 'gameid':gameid, 'playerid':playerid,'all_players':all_players, 'ban_pool_same': 'Rasa na Ban musí být jiná než ta do poolu!'})

                Race.objects.filter(racename=racetopool, game=gameid).update(chosen=True)
                Race.objects.filter(racename=racetoban, game=gameid).update(banned=True)
                playerid.drafted=True
                playerid.save()
                return HttpResponseRedirect(reverse('poolvotingurl', args=(gamepk,)))
        else:
            form = draftraces(gamepk=gamepk, playerid=playerid)   
        return render(request, "draft.html", {'form':form, 'gameid':gameid, 'playerid':playerid, 'all_players':all_players,})

@login_required(login_url='loginurl')
def poolvoting(request, gamepk):
    gameid=Game.objects.get(pk=gamepk)
    user = request.user
    playerid=Player.objects.get(playername=user, game=gameid)
    if playerid.voted == True:
        return HttpResponseRedirect(reverse('finalpickurl', args=(gamepk,)))
    else:  
        racesinpool=Race.objects.filter(game=gameid, chosen=True, voted=False)
        race_with_vote=Race.objects.filter(game=gameid, chosen=False, voted=True)
        all_players=Player.objects.filter(game=gameid).order_by('gameorder')
        
        if racesinpool.count() == gameid.gamesize:
            all_chosen = True
        else:
            all_chosen = False

        voting_turn = Player.objects.filter(game=gameid, voted=True).count()+1
        print(voting_turn)

        if request.method == "POST":
            form = voting(request.POST, gamepk=gamepk, playerid=playerid)
            if form.is_valid():
                voted_race = form.cleaned_data['racetovote']
                if  Race.objects.filter(racename=voted_race, game=gameid, voted = True):
                    Race.objects.filter(racename=voted_race, game=gameid).update(chosen=True)
                else:    
                    Race.objects.filter(racename=voted_race, game=gameid).update(voted=True)
                playerid.voted=True
                playerid.save()
                return HttpResponseRedirect(reverse('finalpickurl', args=(gamepk,)))
        else:
            form = voting(gamepk=gamepk, playerid=playerid)
        return render(request, "poolvoting.html", {'form':form, 'gameid':gameid, 'playerid':playerid, 'racesinpool':racesinpool, 'race_with_vote':race_with_vote, 'all_chosen':all_chosen, 'all_players':all_players, 'voting_turn':voting_turn})

@login_required(login_url='loginurl') 
def finalpick(request, gamepk): 
    user = request.user
    gameid=Game.objects.get(pk=gamepk)
    playerid=Player.objects.get(playername=user, game=gameid)
    player=Player.objects.filter(playername=user)
    all_players=Player.objects.filter(game=gameid).order_by('gameorder')
    gamesize=gameid.gamesize
    
    #zjistuju jeslti uz vsichni votovali
    voted_count=Player.objects.filter(game=gameid, voted=True).count()
    if voted_count == gamesize:
        voting_done = True
    else:
        voting_done = False

    #pocitdalo toho kdo je na rade s pickovanim
    not_picked_races=Player.objects.filter(game=gameid, chosenrace=None).count()
    picked_race=gamesize-not_picked_races
    not_picked_poss=Player.objects.filter(game=gameid, mappositon=None).count()
    picked_poss=gamesize-not_picked_poss
    speakeringame=Player.objects.filter(game=gameid, speaker=True).count()
    turn=picked_poss+picked_race+speakeringame+1
    reverse_order = 2*gamesize+1-playerid.gameorder #vypocet poradi od konce
    third_pick = 2*gamesize+1
    if playerid.gameorder == turn or reverse_order == turn:
        yourturn = True
    elif third_pick == turn :
        if playerid.chosenrace == None or playerid.mappositon == None:
            yourturn = True     
        else:
            yourturn = False
    else:
        yourturn = False

    #kontrola jeslti je volny speaker
    if Player.objects.filter(game=gameid, speaker=True).count() == 0:
        freespeaker = True
    else:
        freespeaker = False
    
    if request.method == "POST":
        form=picking(request.POST, gamepk=gamepk)
        if form.is_valid():
            race=form.cleaned_data['pick']
            player.update(chosenrace=race)
            race.taken=True
            race.save()
            return HttpResponseRedirect(request.path_info)

        form2=picking2(request.POST, gamepk=gamepk)   
        if form2.is_valid():
            pos=form2.cleaned_data['pick2']
            player.update(mappositon=pos)
            Mapposition.objects.filter(game=gameid, position=pos.position).update(taken=True)
            return HttpResponseRedirect(request.path_info)

        form3=picking3(request.POST)   
        if form3.is_valid():
            player.update(speaker=form3.cleaned_data['pick3'])
            return HttpResponseRedirect(request.path_info)

    else:
        form=picking(gamepk=gamepk)
        form2=picking2(gamepk=gamepk)   
        form3=picking3()
    return render(request, "finalpick.html", {'form':form, 'form2':form2, 'form3':form3, 'gameid':gameid, 'playerid':playerid, 'all_players':all_players, 'yourturn':yourturn, 'freespeaker':freespeaker, 'voting_done': voting_done})
