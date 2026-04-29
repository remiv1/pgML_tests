# Dépôt de test pour PostgreML

Ce dépôt contient du code de test pour l'intégration de PostgreML, une extension de PostgreSQL pour le machine learning. Le code inclut des fonctions pour ajouter des produits à un catalogue et pour faire correspondre des produits à partir de descriptions OCR.

## Structure du projet

- `models.py`: Définit les modèles de données pour les produits et les correspondances.
- `functions.py`: Contient les fonctions pour interagir avec la base de données PostgreSQL, notamment pour ajouter des produits et faire des correspondances OCR.
- `pgml.ipynb`: Un notebook Jupyter pour tester les fonctions définies dans `functions.py`.
- `.gitignore`: Fichier pour ignorer les fichiers et dossiers générés automatiquement, comme les environnements virtuels et les caches.
- `README.md`: Ce fichier de documentation.

## Apprentissage

Je vais résumer ce que j'ai fait aujourd'hui et ce que j'ai pu constater.
On peut utiliser des modèles directement avec PostgreML, c'est terriblement efficace.
On crée la vectorisation lors de la création du produit. Ca prend du temps et donc il vaut mieux vectoriser lors de la création du produit ainsi la recherche est relativement rapide.
J'ai testé, c'est réalisable et donc maintenant, je connais le usecase et je peux plus facilement l'implémenter et intégrer ceci dans une solution métier.
Par la suite, on utilisera d'autres modèles pour benchmarker des cas d'usage et comprendre quel modèle pour quel usecase.

## Post LinkedIn

Accroche :
Arrêtez de demander à vos commerciaux de saisir manuellement des devis à partir de PDFs. 🛑

Le Problème :
L'OCR classique vous donne du texte, mais pas de l'intelligence. "ASUS Vivo 15" extrait d'un bon de commande ne matchera jamais avec "Vivobook Go 15 OLED" dans votre base SQL avec une recherche classique. Résultat ? Des heures de correction manuelle et des erreurs de prix.

La Solution :
J'ai passé quelques heures à tester l'intégration de PostgreML et pgvector directement dans une architecture Podman. Le constat est sans appel : transformer votre base de données en moteur d'IA change la donne.

Ce que j'ai appris aujourd'hui :

L'intelligence réside dans le SQL : Plus besoin d'envoyer vos données à une API externe. Le modèle de Machine Learning tourne dans la base de données.

Vectorisation à l'entrée : En générant un "embedding" (une empreinte mathématique) dès la création du produit, la recherche devient instantanée.

Le test de la "Cacahuète" : L'IA est si puissante qu'elle trouve toujours le voisin le plus proche. Le secret ? Utiliser des scores de confiance pour rejeter les produits qui n'ont rien à voir avec l'informatique.

Le résultat métier :
Un client télécharge un PDF ➡️ l'outil extrait les lignes ➡️ l'IA suggère le produit exact du catalogue avec le prix à jour ➡️ le pré-devis est prêt en 10 secondes.

Même avec une envolée du prix des composants (RAM, SSD), le système reste fiable car il lie l'intelligence sémantique à la donnée métier en temps réel.

L'IA n'est plus un gadget, c'est une extension de votre base de données. 🚀

`#IntelligenceArtificielle #PostgreSQL #PostgreML #Productivity #Python #OpenSource`
