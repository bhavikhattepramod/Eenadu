from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError


class Language(models.Model):
    _name = 'res.language'

    speak_lang = fields.Boolean(string="Speak")
    langauge_name = fields.Char(string="Language Name")
    write_lang = fields.Boolean(string="Write")
    employee_language = fields.Many2one('hr.employee')
    read_lang = fields.Boolean(string="Read")

    @api.constrains('langauge_name', 'employee_language')
    def _check_unique_language_name(self):
        for language in self:
            employee = language.employee_language
            if employee:
                duplicate_languages = self.search(
                    [('langauge_name', '=', language.langauge_name), ('employee_language', '=', employee.id)])
                if len(duplicate_languages) > 1:
                    raise exceptions.ValidationError(
                        f"Duplicate language name found for Employee {employee.name}: {language.langauge_name}")

