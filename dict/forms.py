from django import forms

from .models import Pose_model

class PoseForm(forms.ModelForm):
    class Meta:
        model = Pose_model
        fields = [
            "pose_array"
            ]