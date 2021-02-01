from django.test import TestCase, Client

from .models import UserProfile

# Exécution
# python manage.py test 



class UserTestCase(TestCase):

    def client_create_connect_admin(self, c):
        user = UserProfile.objects.create_user(
            username="admin",
            email="admin@admin.com",
            password="admin",
            is_superuser=True,
            is_staff=True,
            )
        c.login(username='admin', password='admin')
        return c

    # Que deux même chaines donnent le même résultat. (Le but est de montrer la syntaxe).
    def test_no_error(self):

        self.assertEqual("Test", 'Test')

    # Que l'affichage de la page users/hello renvoie un code HTTP 200
    # Que cette page renvoie bien le texte Hello World!
    def test_hello(self):

        c = Client()

        response = c.get('/users/hello/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hello World!" in str(response.content))


    # On vérifie que la page /admin redirige un utilisateur non connecté
    # On vérifie que la connexion avec le user admin échoue (ça permet de vérifier qu'une base de données de tests est créée à la volée)
    # On vérifie que la création du superuser fonctionne.
    # On vérifie que la même URL retourne un code 200 HTTP qui nous prouve l'accès de l'utilisateur admin au module d'administration.
    def test_admin(self):

        c = Client()

        response = c.get('/admin/')

        self.assertEqual(response.status_code, 302)

        success = c.login(username='admin', password='admin')

        # Normalement, on ne teste pas les responsabilités externes
        self.assertEqual(success, False)

        user = UserProfile.objects.create_user(
            username="admin",
            email="admin@admin.com",
            password="admin",
            is_superuser=True,
            is_staff=True,
            )
        user.save()

        success = c.login(username='admin', password='admin')

        # Normalement, on ne teste pas les responsabilités externes.

        self.assertEqual(success, True)

        response = c.get('/admin/')

        self.assertEqual(response.status_code, 200)


    # On vérifie que la page d'attribution de rôle n'est pas accessible à un utilisateur non connecté.
    # On vérifie que la page d'attribution de rôle n'est pas accessible à un utilisateur connecté standard.
    # On vérifie que la page d'attribution de rôle est accessible à un superuser connecté.
    # On vérifie que la page d'attribution affiche le username de notre utilisateur créé.
    def test_attribution(self):
        c = Client()
        response = c.get('/users/role-attribution/')
        self.assertEqual(response.status_code, 302)

        UserProfile.objects.create_user(
            username="norole_user",
            email="dkdie@admin.com",
            password="norole_user",
            ).save()
        c.login(username='norole_user', password='norole_user')

        response = c.get('/users/role-attribution/')
        self.assertEqual(response.status_code, 302)

        client = self.client_create_connect_admin(c)
        response = c.get('/users/role-attribution/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("norole_user" in str(response.content))
