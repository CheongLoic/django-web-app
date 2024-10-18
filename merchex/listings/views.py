from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Band
from listings.forms import ContactUsForm, BandForm
from django.core.mail import send_mail
from django.shortcuts import redirect  # ajoutez cet import



def band_list(request):
    bands = Band.objects.all() #Appelle tout le Modèle Band dans une liste
    # utilisé des guillemets triples (""") pour répartir notre chaîne HTML sur plusieurs lignes ;
    # fait de cette chaîne une « f-string » (f""") afin que nous puissions injecter nos noms de groupes dans la chaîne en utilisant{ ... }comme placeholders.
#     return HttpResponse(f"""
#         <h1>Hello Django !</h1>
#         <p>Mes groupes préférés sont :<p>
#         <ul>
#             <li>{bands[0].name}</li>
#             <li>{bands[1].name}</li>
#             <li>{bands[2].name}</li>
#         </ul>
# """)
    return render(request, 'listings/band_list.html',
        {'bands': bands})

def band_detail(request, id):  # notez le paramètre id supplémentaire
#    return render(request,
#           'listings/band_detail.html',
#          {'id': id}) # nous passons l'id au modèle
    band = Band.objects.get(id=id)  # nous sinsérons cette ligne pour obtenir le Band avec cet id
    return render(request,
          'listings/band_detail.html',
          {'band': band}) # nous mettons à jour cette ligne pour passer le groupe au gabarit

def contact(request):
  # ajoutez ces instructions d'impression afin que nous puissions jeter un coup d'oeil à « request.method » et à « request.POST »
  print('La méthode de requête est : ', request.method)
  print('Les données POST sont : ', request.POST)
  if request.method == 'POST': 
        form = ContactUsForm(request.POST)  # ajout d’un nouveau formulaire ici
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).
        return redirect('email-sent') 
  else: 
      form = ContactUsForm() 
  return render(request,
          'listings/contact.html',
          {'form': form})  # passe ce formulaire au gabarit


def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            band = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('band-detail', band.id)
    else:
        form = BandForm()

    return render(request,
            'listings/band_create.html',
            {'form': form})

def band_update(request, id):
    band = Band.objects.get(id=id)
    # form = BandForm(instance=band)  # on pré-remplir le formulaire avec un groupe existant
    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('band-detail', band.id)
    else:
        form = BandForm(instance=band)
    return render(request,
                'listings/band_update.html',
                {'form': form})

def band_delete(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        # supprimer le groupe de la base de données
        band.delete()
        # rediriger vers la liste des groupes
        return redirect('band-list')

    # pas besoin de « else » ici. Si c'est une demande GET, continuez simplement
    return render(request,
           'listings/band_delete.html',
           {'band': band})


def about(request):
    return HttpResponse('<h1>À propos</h1> <p>Nous adorons merch !</p>')

def email_sent(request):
    return HttpResponse('<h1>Email envoyé!</p>')
