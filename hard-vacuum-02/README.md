# HARD VACUUM 02 : WHITE BEAR

Maps de bataille et tokens pour le scénario Traveller/Cepheus "Hard Vacuum 02 : White Bear" (domaine lunaire de Tsygankov sur TG-14, "Chicharito"). Conçus pour import dans owlbear.rodeo.

## Contenu

Maps (grille 44 px, 1 case = 1,5 m, toutes les pièces alignées sur les carrés) :
- `whitebear_estate_map.png` - vue d'ensemble du domaine en L : 2 dômes, tubes, couloirs, coude, salle de contrôle
- `whitebear_deck1_map.png` - couloir 1 : foyer/SAS, 6 cabines de luxe individuelles, expositions d'armures, salle de plaisir (10 invités morts)
- `whitebear_deck2_map.png` - couloir 2 : cabine de Tsygankov (salle de panique cachée dans le dressing), 3 cabines doubles, cuisine (3 corps), salon, salle de contrôle + SAS surface
- `whitebear_pad_map.png` - surface : dôme 1 (yacht + rampe + corps du pilote), dôme 2 (Hot Comet), tubes vers foyer

Tokens 512 px fond transparent :
- `token_serviteur_1..6.png` - robots serviteurs TL13 (x6)
- `token_tsygankov.png` - Tsygankov (cutlass, AR7 mesh)
- `token_mukhtar.png` - Mukhtar (carabine, AR9 cloth)
- `token_rolfo.png` - Rolfo (auto/body pistol, AR3 jack)
- `token_jairzinho.png` - Jairzinho (sans arme)
- `token_rio.png` - Rio Zhaleo (pistolaser laser 4D6, capitaine de la Hot Comet)
- `token_corps.png` - marqueur de corps (10 invités + 4 membres d'équipage)
- `token_ship_yacht.png`, `token_ship_hotcomet.png` - jetons de vaisseaux

## Import owlbear.rodeo

1. Créer une scène, importer la map, régler la grille sur 44 px.
2. Activer "Snap to grid" : les pièces, portes et couloirs tombent pile sur les carrés.
3. Importer les tokens comme assets, les déposer sur la scène (taille 1 case pour les personnages, 2-3 cases pour les vaisseaux).

## Rappels scénario

- Spiritueux empoisonnés offerts par les serviteurs : 2D6+3 dégâts END, perte permanente de 1D6 INT.
- Serviteurs TL13 : coup de poing 2D6, AR6 ; 5 robots dans le domaine + 1 au SAS.
- 10 invités morts dans la salle de plaisir ; 4 autres corps : ingénieur dans le couloir 2 (hors salle de contrôle verrouillée), mécanicien/steward/membre d'équipage du yacht dans la cuisine.
- Porte du dôme verrouillée depuis la salle de contrôle ; vannes iris aux deux extrémités du coude (salle de plaisir scellable).
- Salle de contrôle : Modèle 2/fib, capteurs DM-2 ; casier d'armes : 2 fusils accélérateurs, 2 pistolets snub, 2 combinaisons vacc, 3 trousses d'outils.
- Salle de panique cachée dans le dressing de Tsygankov : porte blindée, verrou électronique.

## Générateur

Python 3 (stdlib uniquement, aucun paquet requis) :

```
cd generator
python3 map_wb_estate.py
python3 map_wb_deck1.py
python3 map_wb_deck2.py
python3 map_wb_pad.py
python3 tokens_whitebear.py
```

Toutes les coordonnées sont en cases de 44 px : pièces en multiples de 44, murs centrés sur les lignes de grille, portes de 22 ou 44 px aux frontières de cases.
