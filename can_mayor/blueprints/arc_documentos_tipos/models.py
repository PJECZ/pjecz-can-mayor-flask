"""
Archivo - Documentos Tipos, modelos
"""

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.universal_mixin import UniversalMixin
from can_mayor.extensions import database


class ArcDocumentoTipo(database.Model, UniversalMixin):
    """ArcDocumentoTipo"""

    # Nombre de la tabla
    __tablename__ = "arc_documentos_tipos"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    nombre: Mapped[str] = mapped_column(String(32), unique=True)

    # Hijos
    arc_documentos: Mapped[List["ArcDocumento"]] = relationship(back_populates="arc_documento_tipo")
    arc_remesas: Mapped[List["ArcRemesa"]] = relationship(back_populates="arc_documento_tipo")

    def __repr__(self):
        """Representación"""
        return f"<ArcDocumentoTipo {self.id}>"
