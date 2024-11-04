"""
Autoridades, formularios
"""

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp

from can_mayor.blueprints.autoridades.models import Autoridad
from can_mayor.blueprints.distritos.models import Distrito
from lib.safe_string import CLAVE_REGEXP


class AutoridadNewForm(FlaskForm):
    """Formulario para nueva Autoridad"""

    clave = StringField("Clave (única de hasta 16 caracteres)", validators=[DataRequired(), Regexp(CLAVE_REGEXP)])
    distrito = SelectField("Distrito", coerce=int, validators=[DataRequired()])
    descripcion = StringField("Descripción", validators=[DataRequired(), Length(max=256)])
    descripcion_corta = StringField("Descripción corta (máximo 64 caracteres)", validators=[DataRequired(), Length(max=64)])
    es_archivo_solicitante = BooleanField("Es Archivo Solicitante", validators=[Optional()])
    es_cemasc = BooleanField("Es CEMASC", validators=[Optional()])
    es_defensoria = BooleanField("Es Defensoría", validators=[Optional()])
    es_extinto = BooleanField("Es Extinto", validators=[Optional()])
    es_jurisdiccional = BooleanField("Es Jurisdiccional", validators=[Optional()])
    es_notaria = BooleanField("Es Notaría", validators=[Optional()])
    es_organo_especializado = BooleanField("Es Órgano Especializado", validators=[Optional()])
    es_revisor_escrituras = BooleanField("Es revisor de escrituras", validators=[Optional()])
    organo_jurisdiccional = SelectField(
        "Órgano Jurisdiccional", choices=Autoridad.ORGANOS_JURISDICCIONALES.items(), validators=[DataRequired()]
    )
    sede = SelectField(
        "Sede (clave distrito geográfico para A.J.)", choices=Autoridad.SEDES.items(), validators=[DataRequired()]
    )
    guardar = SubmitField("Guardar")

    def __init__(self, *args, **kwargs):
        """Inicializar y cargar opciones en distrito, materia y municipio"""
        super().__init__(*args, **kwargs)
        self.distrito.choices = [
            (d.id, d.nombre_corto) for d in Distrito.query.filter_by(estatus="A").order_by(Distrito.nombre_corto).all()
        ]


class AutoridadEditForm(FlaskForm):
    """Formulario para editar Autoridad"""

    clave = StringField("Clave (única de hasta 16 caracteres)", validators=[DataRequired(), Regexp(CLAVE_REGEXP)])
    distrito = SelectField("Distrito", coerce=int, validators=[DataRequired()])
    descripcion = StringField("Descripción", validators=[DataRequired(), Length(max=256)])
    descripcion_corta = StringField("Descripción corta (máximo 64 caracteres)", validators=[DataRequired(), Length(max=64)])
    es_archivo_solicitante = BooleanField("Es Archivo Solicitante", validators=[Optional()])
    es_cemasc = BooleanField("Es CEMASC", validators=[Optional()])
    es_defensoria = BooleanField("Es Defensoría", validators=[Optional()])
    es_extinto = BooleanField("Es Extinto", validators=[Optional()])
    es_jurisdiccional = BooleanField("Es Jurisdiccional", validators=[Optional()])
    es_notaria = BooleanField("Es Notaría", validators=[Optional()])
    es_organo_especializado = BooleanField("Es Órgano Especializado", validators=[Optional()])
    es_revisor_escrituras = BooleanField("Es revisor de escrituras", validators=[Optional()])
    organo_jurisdiccional = SelectField(
        "Órgano Jurisdiccional", choices=Autoridad.ORGANOS_JURISDICCIONALES.items(), validators=[DataRequired()]
    )
    sede = SelectField(
        "Sede (clave distrito geográfico para A.J.)", choices=Autoridad.SEDES.items(), validators=[DataRequired()]
    )
    directorio_edictos = StringField("Directorio para edictos", validators=[Optional(), Length(max=256)])
    directorio_glosas = StringField("Directorio para glosas", validators=[Optional(), Length(max=256)])
    directorio_listas_de_acuerdos = StringField("Directorio para listas de acuerdos", validators=[Optional(), Length(max=256)])
    directorio_sentencias = StringField("Directorio para sentencias", validators=[Optional(), Length(max=256)])
    limite_dias_listas_de_acuerdos = IntegerField("Límite días para listas de acuerdos", validators=[NumberRange(0, 365)])
    guardar = SubmitField("Guardar")

    def __init__(self, *args, **kwargs):
        """Inicializar y cargar opciones en distrito, materia y municipio"""
        super().__init__(*args, **kwargs)
        self.distrito.choices = [
            (d.id, d.nombre_corto) for d in Distrito.query.filter_by(estatus="A").order_by(Distrito.nombre_corto).all()
        ]
