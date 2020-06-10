'''
Define form in _CensusImputeForm, create instances using CensusImputeForm
'''

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, BooleanField

class CensusImputeForm():
    def __init__(self, data_dict, numeric_fields, recordname2description):
        self.form_class = _CensusImputeForm.make_form(data_dict, numeric_fields, recordname2description)
        self.numeric_fields = numeric_fields
        self.data_dict = data_dict

    def get_instance(self,request_form=None):
        instance = self.form_class(request_form)
        instance.field_list = list()

        for key in self.numeric_fields:
            instance.field_list.append((getattr(instance, key), getattr(instance, 'mask_' + key)))

        for key in self.data_dict:
            instance.field_list.append((getattr(instance, key), getattr(instance, 'mask_' + key)))
        return instance

class _CensusImputeForm(FlaskForm):
    #Creates a form with all the right fields
    @classmethod
    def make_form(cls, data_dict, numeric_fields, recordname2description):

        for key in numeric_fields:

            setattr(cls, key, DecimalField(id=key, label=recordname2description[key].split('(')[0]))
            setattr(cls, 'mask_' + key, BooleanField(label='mask_' + key))

        for key in data_dict:

            setattr(cls, key, SelectField(id=key, label=recordname2description[key],
                                          choices=[(-1, 'None selected')]+list(data_dict[key].items())))
            setattr(cls, 'mask_' + key, BooleanField(label='mask_' + key))

        return cls
