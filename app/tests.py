from django.test import TestCase, Client
from app import models
from app.models import User, Directory, File, SectionCategory, Status, StatusData, FileSection
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import FileForm, DirectoryForm, VCsForm, tab_options
from django.contrib import auth
from .functions import dir_array, dir_array_levels, file_array, merge_dirs_files, get_dirs_and_files, delete_dir, get_result, create_sections, get_command, basic_compile, adv_compile, parse_compilation, html_tree
from .views import index_view, add_file_view, add_directory_view, show_tab, save_prover, save_vcs, auth_user
from .views import js_show_file, js_delete_file, js_delete_directory, js_compile
from django.urls import reverse
from django.test.client import RequestFactory

# Create your tests here.

class ModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(name="abc", login="abc", password="pass1234")
        dir = Directory.objects.create(name="dir", description="directory", owner=user)
        Directory.objects.create(name="dir2", description="directory2", owner=user, parent_directory=dir)
        file = File.objects.create(name="file", description="file", file=SimpleUploadedFile("t.txt", ""), directory=dir, owner=user)
        section_category = SectionCategory.objects.create(category="section")
        status = Status.objects.create(status="failed")
        status_data = StatusData.objects.create(status_data="status data", user=user)
        file_section = FileSection.objects.create(name="file_section", description="file_section", category=section_category, status=status, status_data=status_data, file=file)

    def test_user(self):
        user = User.objects.get(name="abc")
        self.assertEqual(user.login, "abc")
        self.assertEqual(user.password, "pass1234")
        self.assertEqual(str(user), user.name)

    def test_dir(self):
        user = User.objects.get(name="abc")
        dir = Directory.objects.get(name="dir")
        dir2 = Directory.objects.get(name="dir2")
        file = File.objects.get(name="file")
        self.assertEqual(dir.description, "directory")
        self.assertEqual(dir2.description, "directory2")
        self.assertEqual(dir.owner, user)
        self.assertEqual(dir2.owner, user)
        self.assertEqual(str(dir), dir.name)

    def test_file(self):
        user = User.objects.get(name="abc")
        dir = Directory.objects.get(name="dir")
        file = File.objects.get(name="file")
        self.assertEqual(file.description, "file")
        self.assertEqual(file.directory, dir)
        self.assertEqual(file.owner, user)
        self.assertEqual(str(file), file.name)

    def test_section_category(self):
        section_category = SectionCategory.objects.get(category="section")
        self.assertEqual(section_category.category, "section")
        self.assertEqual(str(section_category), section_category.category)

    def test_status(self):
        status_data = StatusData.objects.get(status_data="status data")
        user = User.objects.get(name="abc")
        self.assertEqual(status_data.user, user)
        self.assertEqual(str(status_data), status_data.status_data)

    def test_status_data(self):
        status = Status.objects.get(status="failed")
        self.assertEqual(status.status, "failed")
        self.assertEqual(str(status), status.status) 

    def test_file_section(self):
        file_section = FileSection.objects.get(name="file_section")
        user = User.objects.get(name="abc")
        dir = Directory.objects.get(name="dir")
        file = File.objects.get(name="file")
        section_category = SectionCategory.objects.get(category="section")
        status = Status.objects.get(status="failed")
        status_data = StatusData.objects.get(status_data="status data")
        self.assertEqual(file_section.description, "file_section")
        self.assertEqual(file_section.category, section_category)
        self.assertEqual(file_section.status, status)
        self.assertEqual(file_section.status_data, status_data)
        self.assertEqual(file_section.file, file)
        self.assertEqual(str(file_section), file_section.name)


class FormTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(name="abc", login="abc", password="pass1234")
        dir = Directory.objects.create(name="dir", description="directory", owner=user)
        file = File.objects.create(name="file", description="file", file=SimpleUploadedFile("t.txt", b"xxxx"), directory=dir, owner=user)
        
    def test_directory(self):
        dir = Directory.objects.get(name="dir")
        form_data = {'name': 'abc', 'description': 'desc', 'parent_directory': dir}
        form = DirectoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_file_clean_name(self):
        dir = Directory.objects.get(name="dir")
        file = File.objects.get(name="file")
        form_data = {'name': 'abc;', 'description': 'desc', 'directory': dir, 'file': SimpleUploadedFile("xxx.c", "")}
        form = FileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_vcs(self):
        OPTIONS = [
            (1, "@invariant"),
            (2, "@lemma"),
            (3, "@ensures"),
            (4, "@requires"),
            (5, "@assigns"),
            (6, "@exits"),
            (7, "@assert"),
            (8, "@check"),
            (9, "@variant"),
            (10, "@breaks"),
            (11, "@continues"),
            (12, "@returns")
        ]

        vcs_list = [(3, "@ensures"), (8, "@check")]

        client = Client()

        data = {'vcs': vcs_list}
        response = client.post('/app/save_vcs/', data)

        i = 0
        for vc in vcs_list:
            self.assertIn(data['vcs'][i], OPTIONS)
            i = i + 1

        self.assertEqual(response.status_code, 302)


class ViewTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        auth.models.User.objects.create_user(username='abc', password='pass1234')
        self.client = Client()
        self.client.login(username='abc', password='pass1234')

        user = models.User.objects.create(name="abc", login="abc", password="pass1234")
        dir = Directory.objects.create(name="dir", description="directory", owner=user)
        dir2 = Directory.objects.create(name="dir2", description="directory2", owner=user, parent_directory=dir)
        file = File.objects.create(name="file", description="file", file=SimpleUploadedFile("t.txt", b"zzz"), directory=dir, owner=user)
        file2 = File.objects.create(name="file2", description="file2", file=SimpleUploadedFile("t2.txt", b"xxx"), directory=dir2, owner=user)

    def test_index_view(self):
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_add_file_view(self):
        response = self.client.get('/app/add_file/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('add_file.html')

    def test_add_file_view_post(self):
        response = self.client.post('/app/add_file/', {'form': FileForm()})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('add_file.html')

    def test_add_directory_view(self):
        response = self.client.get('/app/add_directory/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('add_directory.html')

    def test_add_directory_view_post(self):
        response = self.client.post('/app/add_directory/', {'form': DirectoryForm()})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('add_directory.html')

    def test_show_tab_vcs(self):        
        response = self.client.get(reverse('app:show_tab', args=['vcs']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_show_tab_result(self):
        session = self.client.session
        session['result'] = None
        session['chosen_file'] = 'file'
        session.save()
        response = self.client.get(reverse('app:show_tab', args=['result']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_show_tab_provers(self):
        response = self.client.get(reverse('app:show_tab', args=['provers']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')

    def test_save_vcs(self):
        response = self.client.post(reverse('app:save_vcs'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('index.html')

    def test_save_prover(self):
        response = self.client.post(reverse('app:save_prover'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('index.html')

    def test_auth_user(self):
        response = self.client.get('/auth_user/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('index.html')

    def test_js_show_file(self):
        user = auth.models.User.objects.get(username='abc')
        response = self.client.get(reverse('app:js_show_file'), data={'name': 'file'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')
    
    def test_js_delete_file(self):
        response = self.client.get(reverse('app:js_delete_file'), data={'name': 'file'})
        self.assertEqual(response.status_code, 200)

    def test_js_delete_directory(self):
        response = self.client.get(reverse('app:js_delete_directory'), data={'name': 'dir'})
        self.assertEqual(response.status_code, 200)

    def test_js_compile(self):
        session = self.client.session
        session['chosen_file'] = 'file'
        session['prover'] = 'None'
        session.save()

        response = self.client.post(reverse('app:js_compile'))
        self.assertEqual(response.status_code, 200)