"""models.py - Définit les modèles de données pour les produits et les extractions OCR
- Produit: Représente un produit informatique avec son embedding pour la recherche vectorielle
- ExtractionLigne: Stocke le résultat brut de l'OCR avant validation, avec une relation vers
                   le produit suggéré par PostgreML
"""

from __future__ import annotations
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, mapped_column, Mapped
from pgvector.sqlalchemy import VECTOR
from datetime import datetime

Base = declarative_base()

class Produit(Base):
    """Représente un produit informatique avec son embedding pour la recherche vectorielle"""
    __tablename__ = 'produits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    marque: Mapped[str] = mapped_column(String)
    label: Mapped[str] = mapped_column(String, nullable=False)
    description_technique: Mapped[str] = mapped_column(String)
    prix_ht: Mapped[float] = mapped_column(Float)
    # Vecteur de 384 dimensions pour e5-small-v2
    embedding: Mapped[list[float]] = mapped_column(VECTOR(384))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
        )

class ExtractionLigne(Base):
    """Stocke le résultat brut de l'OCR avant validation"""
    __tablename__ = 'extraction_lignes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_source: Mapped[str] = mapped_column(String) # Nom du PDF
    texte_brut: Mapped[str] = mapped_column(String)      # Ex: "10x ASUS Vivo 512/8"
    quantite_extraite: Mapped[int] = mapped_column(Integer, default=1)

    # Relation avec le produit suggéré par PostgreML
    produit_suggere_id: Mapped[int] = mapped_column(Integer, ForeignKey('produits.id'))
    score_confiance: Mapped[float] = mapped_column(Float)

    produit_suggere: Mapped[Produit] = relationship("Produit")
