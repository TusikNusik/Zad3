from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Point
from .models import PointList
from .forms import FormPoint
from .forms import FormList
# Create your views here.

def index(request):
    return render(request, "trasy/base.html")

def points(request):
    pointList = Point.objects.all()

    pointDictonary = {"pointList": pointList}

    return render(request, "trasy/pointList.html", pointDictonary)

# Zmienna request wie czy dostajemy POST czy GET request   
def addPoint(request, id):
    list = PointList.objects.get(id=id)

    #dict to słownik w postaci {"nazwa_obiektu": ["value_obiektu"], ...}, który zawiera w ten sposób magazynowane informacje z FORM.
    # dlatego nazwa i value są ważne
    dict = request.POST
    
    if request.method == "POST":
        if dict.get("save"):
            for point in list.points.all():
                if dict.get(f"{point.id}") == "included":
                    point.included = True
                else:
                    point.included = False
                
                point.save()

        elif dict.get("addPoint"):
            x = dict.get("X-cord")
            y = dict.get("Y-cord")


            temp = Point(x=x, y=y, included=True)
            temp.save()
            list.points.add(temp)

    return render(request, "trasy/addPoint.html", {"list": list})

def addList(request):
    if request.method == "POST":
        form = FormList(request.POST, request.FILES)  # Tworzy obiekt FormPoint o danych wysłanych przez użytkownika.

        if form.is_valid():
            point_list = form.save(commit=False)
            point_list.user = request.user
            point_list.save()

    form = FormList()  # Przekazujemy nasz obiekt html wie co robic
    return render(request, "trasy/addList.html", {"form": form})

@login_required
def savedProjects(request):
    user_lists = PointList.objects.filter(user=request.user)
    return render(request, "trasy/savedProjects.html", {"user_lists": user_lists})