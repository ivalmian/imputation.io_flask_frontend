from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, BooleanField
from flask_wtf.csrf import CSRFProtect
from inference_demo import app
# from wtforms.validators import DataRequired, Email


csrf = CSRFProtect(app)
csrf.init_app(app)


class CensusImputeForm(FlaskForm):

    @classmethod
    def make_form(cls, data_dict, numeric_fields, recordname2description, request_form=None):

        for key in numeric_fields:

            setattr(cls, key, DecimalField(id=key, label=recordname2description[key].split('(')[0]))
            setattr(cls, 'mask_' + key, BooleanField(label='mask_' + key))

        for key in data_dict:

            setattr(cls, key, SelectField(id=key, label=recordname2description[key],
                                          choices=[(-1, 'None selected')]+list(data_dict[key].items())))
            setattr(cls, 'mask_' + key, BooleanField(label='mask_' + key))

        if not request_form:
            instance = cls()
        else:
            instance = cls(request_form)
        instance.field_list = list()

        for key in numeric_fields:
            instance.field_list.append((getattr(instance, key), getattr(instance, 'mask_' + key)))

        for key in data_dict:
            instance.field_list.append((getattr(instance, key), getattr(instance, 'mask_' + key)))

        return instance
