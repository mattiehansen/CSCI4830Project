from django.test import TestCase
from .models import Student,Teacher,Pass
from .forms import LoginForm, PassForm, ReturnForm

class Test(TestCase):

    def create_whatever(self,
                        fn='firstname',
                        ln='lastname',
                        id=1000000001,
                        ps='password',
                        ac='accom here',
                        n='notes here',
                        pn=0,
                        rn=0,):
        return Student.objects.create(student_first_name=fn,
                                      student_last_name=ln,
                                      student_id=id,
                                      student_password=ps,
                                      accommodations=ac,
                                      notes=n,
                                      number_of_passes=pn,
                                      number_of_rejections=rn)

    def test_whatever_creation(self):
        w = self.create_whatever()
        self.assertTrue(isinstance(w, Student))
        self.assertEqual(w.__str__(),
                         w.student_first_name,
                         w.student_last_name,)
