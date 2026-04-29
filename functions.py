"""Modules de fonctions pour l'ajout de produits au catalogue avec embeddings pré-calculés via SQL
- Utilise la fonction pgml.embed pour calculer les embeddings directement dans la base de données
- Permet d'ajouter facilement de nouveaux produits sans charger le modèle en Python
"""

from typing import Any
from sqlalchemy import func
from pgvector.sqlalchemy import VECTOR
from sqlalchemy.orm import Session
from models import Produit

def ajouter_au_catalogue(session: Session, product: Produit):
    """Fonction d'ajout de produit au catalogue avec embedding pré-calculé via SQL"""
    # On pré-calcule le vecteur via SQL pour ne pas charger le modèle en Python
    emb_query = func.pgml.embed('intfloat/e5-small-v2', f"passage: {product.label}")
    embeding_result = func.cast(emb_query, VECTOR(384)) # pylint: disable=not-callable
    product.embedding = embeding_result
    session.add(product)
    session.commit()

# Test avec vos modèles rivaux
# ajouter_au_catalogue(
#   session,
#   Produit(
#       marque="ASUS",
#       label="Vivobook 15 - R5 - 8Go - 512Go SSD",
#       prix_ht=599.0,
#       description_technique="Ordinateur portable Asus Vivobook 15."
#   ))

from sqlalchemy import select

def match_produit_ocr(session: Session, texte_ocr: str) -> list[tuple[Produit, float, float, int]]:
    """Fonction de recherche du produit le plus similaire à une ligne OCR donnée
    - Transforme le texte OCR en vecteur de requête via SQL
    - Calcule la distance cosinus avec les embeddings des produits
    - Retourne tous les matchs au-dessus du seuil, regroupés par produit
    """
    # 1. On transforme l'entrée OCR en vecteur de requête
    query_vector = func.pgml.embed('intfloat/e5-small-v2', f"query: {texte_ocr}")

    # 2. On calcule la distance cosinus
    # cosine_distance est fourni par pgvector-python
    stmt = (
        select(
            Produit,
            (1 - Produit.embedding.cosine_distance(
                func.cast(query_vector, VECTOR(384))    # pylint: disable=not-callable
                )).label("score")
        )
        .order_by((1 - Produit.embedding.cosine_distance(
            func.cast(query_vector, VECTOR(384))        # pylint: disable=not-callable
        )).desc())
    )

    result = session.execute(stmt).all()

    seuil_critique = 0.80

    regroupes: dict[str, dict[str, Any]] = {}
    for produit, score in result:
        if score < seuil_critique:
            continue

        cle = produit.label
        if cle not in regroupes:
            regroupes[cle] = {
                "produit": produit,
                "best_score": score,
                "sum_score": score,
                "count": 1,
            }
        else:
            regroupes[cle]["count"] += 1
            regroupes[cle]["sum_score"] += score
            if score > regroupes[cle]["best_score"]:
                regroupes[cle]["best_score"] = score

    details: list[tuple[Produit, float, float, int]] = []
    for item in regroupes.values():
        details.append(
            (
                item["produit"],
                item["best_score"],
                item["sum_score"] / item["count"],
                item["count"],
            )
        )

    details.sort(key=lambda x: x[1], reverse=True)
    return details
