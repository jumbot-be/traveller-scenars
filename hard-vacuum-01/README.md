# HARD VACUUM 01 : PIRATE BAIT — Maps & Tokens

Assets pour le scénario Traveller / Cepheus Engine "HARD VACUUM 01 : PIRATE BAIT" (Grape Ape Press), prêts pour owlbear.rodeo.

Grille : 1 case = 1,5 m (44 px à l'échelle owlbear par défaut). Version 2 : toutes les pièces sont alignées sur les carrés (coordonnées en multiples de 44 px, murs sur les lignes de grille, portes de 22/44 px aux frontières de cases) — activer snap to grid.

## Contenu

Maps (dossier `maps/`) :
- `outpost_map.png` — Rodolphe 189, avant-poste minier, niveau unique : quai, stockage, atelier, réfectoire, quartiers officiers, génératrices, 4 cabines à porte individuelle sur couloir, sas, contrôle.
- `asteroid_map.png` — Surface de Rodolphe 189 : avant-poste, tube 25 m, vaisseau des PJ, positions 5 pirates + robot.
- `hotcomet_map.png` — Hot Comet (courier 100 t, vaisseau des PJ) : couloir central, 4 cabines à porte individuelle avec fresher privé, salon, sas, cale 20 t, machines, carburant, propulseurs.
- `chiaroscuro_deck1.png` / `chiaroscuro_deck2.png` — Chiaroscuro (Frontier Trader 300 t, pirates Hounds of the Cursed Moon) : pont 1 avec 3 dortoirs de 4 couchettes à porte individuelle, pont, mess, machines ; pont 2 : cale, portes cargo ouvertes, air/raft.
- `dragonclaw_deck1.png` / `dragonclaw_deck2.png` — Merc Dragon's Claw (raider) : pont 1 avec 3 cabines officiers individuelles, quartiers troupes, brig accessible uniquement par couloir, medbay, pont ; pont 2 : hangar 3 chasseurs, porte de lancement.

Vues extérieures (dossier `exteriors/`) :
- `ext_hotcomet.png` — courier : flèche, aileron dorsal, double moteur bleu.
- `ext_chiaroscuro.png` — trader : coque segmentée, passerelle déportée, pods cargo.
- `ext_dragonclaw.png` — raider : proue fourchue, bandes rouges, triple moteur vert.

Tokens 512 px fond transparent (dossier `tokens/`) :
- `token_pirate_chef.png` — chef pirate : fusil laser 4D6, cutlass 3D6, Leadership-2.
- `token_pirate_demo.png` — démolitionnaire : SMG 2D6, explosifs 3D6.
- `token_pirate_3/4/5.png` — pirates : fusil accélérateur 3D6.
- `token_vuurst.png` — Gerda Vuurst, civile : aucune arme, Admin-2.
- `token_merc_comdt.png`, `token_merc_1.png`, `token_merc_2.png` — mercenaires : fusil Gauss 4D6, armure AR8.
- `token_robot.png` — robot de surveillance.
- `token_ship_hotcomet.png`, `token_ship_chiaroscuro.png`, `token_ship_dragonclaw.png` — vaisseaux vue de dessus.

## Import owlbear.rodeo

1. Ouvrir la map comme image, couche Map.
2. Grille : plans dessinés à 44 px par case de 1,5 m. Les pièces tombent pile sur les carrés — activer la grille et snap to grid.
3. Importer les tokens comme assets, glisser sur la couche Tokens. Fond transparent, aucun nettoyage.

## Rappels scénario

- Abordage : 1-2 par le vaisseau, 3-4 par le tube, 5-6 par le sas.
- Les pirates fuient après 3 pertes. Recul 0-G : malus aux tirs non prévus pour.
- Le raider des mercenaires arrive environ 2 h après le premier signal, avec 3 chasseurs.

## Regénérer les PNG

Le dossier `generator/` contient le générateur complet (Python 3, stdlib uniquement, aucune dépendance) :

```sh
cd generator && sh generate_all.sh
```

Produit les 23 PNG dans le dossier courant. Rendu déterministe (seeds fixes). Les cartes de bataille utilisent `wb_common.py` (coordonnées en cases de 44 px, murs centrés sur les lignes de grille).
