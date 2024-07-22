import copy
from forms.form import Form

# _FORMS[user_id] = _Form
_FORMS = {}

# TODO add form stack (several consecutive forms for the same user).

def _delete_form(_form: Form):
    """
    Callback function passed to a form
    in order to avoid circular imports.
    """
    global _FORMS
    if _form.user_id in _FORMS:
        del _FORMS[_form.user_id]


# forms.start
def start(user_id: int, form_template: Form):
    global _FORMS
    """Creates a new form to fill."""
    form = _FORMS[user_id] = copy.deepcopy(form_template)
    form.set_user_id(user_id)
    form.set_destructor(_delete_form)
    return form


# forms.get
def get(user_id: int) -> Form:
    global _FORMS
    return _FORMS.get(user_id)
