"""

decorators.py

Miscellaneous decorators used project-wide.

"""

from __future__ import unicode_literals


def html5_required(Form):
    """ Adds a "required" HTML5 attribute to any Form fields that are 
    required.
    
    """
    
    try:
        items = Form.base_fields.iteritems()
    except AttributeError:
        # Python 3 compatibility
        items = Form.base_fields.items()
    
    for fieldName, field in items:
        if field.required:
            field.widget.attrs['required'] = 'required'
            
    return Form
    
    