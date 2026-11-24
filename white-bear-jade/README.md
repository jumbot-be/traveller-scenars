# White Bear - Variante Jade

Même scénario, même géométrie, même grille 44 px (1 case = 1,5 m) que hard-vacuum-02. Seule la palette change : version vert pâle / gris, style megastructures géométriques propres.

## Principe

Le fond bucco-bleu de la palette d'origine devient sauge/vert pâle via un filtre de teinte appliqué au point d'écriture pixel dans hv.py (fonction _JADE). Les couleurs chaudes (rouge, or, orange) et les couleurs déjà vertes sont inchangées. Aucune coordonnée, aucune pièce, aucun label n'est modifié : les cartes restent compatibles à la case près avec la version bleue.

## Contenu

- generator/ : scripts identiques à hard-vacuum-02/generator, sauf hv.py qui embarque le filtre jade.
- Maps générées : estate (plan d'ensemble), deck1, deck2, pad.

## Régénérer

    cd generator && ./generate_all.sh

Rendu déterministe : pas de texture de bruit, grain identique à chaque exécution.

## Importation owlbear.rodeo

Identique à la version principale : échelle 44 px, 1 case = 1,5 m.
