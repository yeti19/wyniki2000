from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from wyniki_2017.models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep


class OfflineTest(TestCase):
    def setUp(self):
        v = Voivodeship.objects.create(name='Mazowieckie', num=1)
        d = District.objects.create(name='Pierwszy', num=1, voivodeship=v)
        c = Commune.objects.create(name='Gmina1', num=1, district=d)
        Precinct.objects.create(num=1, address='abc', commune=c, allowed=20,
                                cards_issued=18, votes_cast=16, valid_votes=14,
                                invalid_votes=2, votes_1=2, votes_2=2,
                                votes_3=1, votes_4=1, votes_5=1, votes_6=1,
                                votes_7=1, votes_8=1, votes_9=1, votes_10=1,
                                votes_11=1, votes_12=1)
        Precinct.objects.create(num=2, address='bcd', commune=c, allowed=20,
                                cards_issued=18, votes_cast=16, valid_votes=14,
                                invalid_votes=2, votes_1=2, votes_2=2,
                                votes_3=1, votes_4=1, votes_5=1, votes_6=1,
                                votes_7=1, votes_8=1, votes_9=1, votes_10=1,
                                votes_11=1, votes_12=1)

    def test_aggregate_precinct(self):
        data = aggregate_precincts(Precinct.objects)
        self.assertEqual(data, [40, 36, 32, 4, 28, 4, 4, 2, 2, 2, 2, 2, 2, 2,
                                2, 2, 2])


class MyPage(webdriver.Chrome):
    def __init__(self, url):
        # self.driver = webdriver.Chrome()
        super(MyPage, self).__init__()
        self.get(url)
        self.implicitly_wait(1)

    def ClickButtonAndWait(self, button):
        ActionChains(self).click(self.find_element_by_xpath(button)).perform()
        WebDriverWait(self, 10).until(EC.invisibility_of_element_located((By.ID, "loading")))

    def IsLoggedIn(self):
        return self.find_element_by_xpath("//span[@id='logged_in']").is_displayed()

    def Login(self, username, password):
        username_input = self.find_element_by_xpath("//form[@id='login']/input[@name='username']")
        password_input = self.find_element_by_xpath("//form[@id='login']/input[@name='password']")
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        self.ClickButtonAndWait("//span[@id='logged_out']/button[1]")

    def Register(self, username, password):
        ActionChains(self).click(self.find_element_by_xpath("//span[@id='logged_out']/button[2]")).perform()
        username_input = self.find_element_by_xpath("//form[@id='register']/div/input[@name='username']")
        password_input = self.find_element_by_xpath("//form[@id='register']/div/input[@name='password']")
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        self.ClickButtonAndWait("//button[@onclick='register()']")
    
    def Logout(self):
        self.ClickButtonAndWait("//span[@id='logged_in']/button[1]")

    def AddElement(self, name):
        name_input = self.find_element_by_xpath("//tr[@data-num='666']/td/input[@type='text']")
        name_input.send_keys(name)
        self.ClickButtonAndWait("//tr[@data-num='666']/td/button[1]")

    def GoTo(self, num):
        self.ClickButtonAndWait("//table[@class='regions']/tbody/tr[" + str(num) + "]/td[1]/button[1]")

    def Back(self):
        self.ClickButtonAndWait("//button[@id='back']")

    def Search(self, str):
        self.find_element_by_xpath("//input[@name='q']").send_keys(str)
        self.ClickButtonAndWait("//form[@id='search']/button")

    def CountElements(self):
        return len(self.find_elements_by_xpath("//table[@class='regions']/tbody/tr"))


class LoggedOutCleanPageTest(StaticLiveServerTestCase):
    def setUp(self):
        self.page = MyPage(self.live_server_url)

    def tearDown(self):
        self.page.close()

    def test_start_page(self):
        assert "Wyniki wyborów 2000" in self.page.title
        assert not self.page.find_element_by_xpath("//span[@id='logged_in']").is_displayed()
        assert self.page.find_element_by_xpath("//span[@id='logged_out']").is_displayed()
        assert len(self.page.find_elements_by_xpath("//table[@class='regions']/thead/tr/th")) == 14
        assert len(self.page.find_elements_by_xpath("//table[@class='regions']/tbody/tr")) == 0
        assert self.page.find_element_by_xpath("//button[@id='refresh']").is_displayed()
        self.assertRaises(NoSuchElementException, self.page.find_element_by_xpath, "//button[@id='back']")
        assert self.page.find_element_by_xpath("//span[@id='msg']").text == ''

    def test_logging_in_out(self):
        self.page.Login("abcd", "abcd")
        assert self.page.IsLoggedIn() is False
        self.page.Register("abcd", "abcd")
        assert self.page.IsLoggedIn() is True
        self.page.Logout()
        assert self.page.IsLoggedIn() is False
        self.page.Login("abcd", "abcd")
        assert self.page.IsLoggedIn() is True


class LoggedInTest(StaticLiveServerTestCase):
    def setUp(self):
        self.page = MyPage(self.live_server_url)
        self.page.Register("abcd", "abcd")

    def tearDown(self):
        self.page.close()

    def test_adding_voivodeship(self):
        self.page.AddElement("Wojewodztwo")
        self.page.AddElement("Wojewodztwo2")
        self.page.AddElement("Wojewodztwo")
        assert self.page.CountElements() == 4
        self.page.AddElement("Wojewodztwoyweirouyweohwojdhjbjdkcbsuchifhe")
        assert self.page.CountElements() == 4

    def test_adding_district(self):
        self.page.AddElement("Wojewodztwo")
        self.page.GoTo(1)
        self.page.AddElement("Okrąg1")
        self.page.AddElement("Okrąg2")
        assert self.page.CountElements() == 3
        self.page.AddElement("Wojewodztwoyweirouyweohwojdhjbjdkcbsuchifhe")
        assert self.page.CountElements() == 3

    def test_adding_commune(self):
        self.page.AddElement("Wojewodztwo")
        self.page.GoTo(1)
        self.page.AddElement("Okrąg1")
        self.page.GoTo(1)
        self.page.AddElement("Gmina1")
        self.page.AddElement("Gmina2")
        assert self.page.CountElements() == 3
        self.page.AddElement("Wojewodztwoyweirouyweohwojdhjbjdkcbsuchifhe")
        assert self.page.CountElements() == 3


class WithDataTest(StaticLiveServerTestCase):
    def setUp(self):
        self.page = MyPage(self.live_server_url)
        self.page.Register("abcd", "abcd")
        self.page.AddElement("Wojewodztwo")
        self.page.AddElement("Wojewodztwo2abc")
        self.page.AddElement("Wojewodztwo")
        self.page.GoTo(1)
        self.page.AddElement("Okrąg1")
        self.page.AddElement("Okrąg2")
        self.page.GoTo(1)
        self.page.AddElement("Gmina1")
        self.page.AddElement("Gmina2")
        self.page.Back()
        self.page.Back()

    def tearDown(self):
        self.page.close()

    def test_search(self):
        self.page.Search("abc")
        assert self.page.CountElements() == 2
        