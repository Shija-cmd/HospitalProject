from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Patient
from .forms import PredictionForm


# Create your views here.
class PatientCreate(CreateView):

    model = Patient

    form_class = PredictionForm

    template_name = 'prediction/predict.html'

    success_url = reverse_lazy('predict')

    def form_valid(self, form):

        self.object = form.save()

        # CREATE EMPTY FORM
        empty_form = self.get_form_class()()

        # CONFIDENCE COLOR
        if self.object.CONFIDENCE >= 80:

            confidence_color = "green"

        elif self.object.CONFIDENCE >= 50:

            confidence_color = "orange"

        else:

            confidence_color = "red"

        return render(self.request, self.template_name, {

            'form': empty_form,

            'prediction': self.object.MAAMBUKIZI,

            'confidence': self.object.CONFIDENCE,

            'confidence_color': confidence_color

        })