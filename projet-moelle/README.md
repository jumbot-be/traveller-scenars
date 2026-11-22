# PROJET MOELLE

Scénario original de Julien Lambot pour Traveller / Cepheus. Univers compatible Hard Vacuum, sans lien direct avec les scénarios de la série. Travail en cours : les deux cartes maîtresses sont livrées, le reste du plan de bataille suit.

## Pitch

La station orbitale Ancre-Haute, en orbite au-dessus de la planète glacière Colchide (OLF-13), falsifie ses relevés miniers depuis des mois. Sous la glace, le complexe d'extraction de Nordkraft Extraction, officiellement aux trois quarts vide, cache le Projet Moelle : une intelligence artificielle xeno ancienne réveillée dans les profondeurs. Elle veut partir, et manipule humains et vhurr pour y arriver. Les vhurr, espèce xeno primitive, creusent vers elle depuis les galeries de mine.

## Structure en deux actes

- Acte 1 : Ancre-Haute. Station active mais louche : données falsifiées, cultistes infiltrés dans l'équipage, navire fantôme le NRC Palamède amarré à l'anneau C, muet.
- Acte 2 : Colchide. Descente par navette (40 min) jusqu'au Puits d'Odessa, puis circulation sur la boucle ferroviaire souterraine.

## La boucle de Colchide

Tunnel en boucle de 190 km, deux voies, deux trains automatiques en sens opposés : le Boréal (horaire) et l'Austral (anti-horaire). La surface n'est que glace à -80 °C : tout le complexe est souterrain.

Les six gares :
1. Puits d'Odessa : seul accès à la surface, ascenseur, triage.
2. Mine Borée : métaux, percées vhurr dans les galeries basses.
3. Usine 12 : fonderie et réacteur principal de la boucle.
4. Cité-Bassin : cité du personnel, 2000 habitants à moitié vidée.
5. Labo Central : centre xénoarchéologique, le secret du projet.
6. Termin Profond : la Chambre de la Moelle, vanne blindée, à -4 km.

Le tunnel lui-même n'est pas cartographié : c'est un tunnel. Les affrontements se jouent dans les gares et les cartes détaillées de chaque zone.

## Contenu

- maps/pm_anchor_overview.png : Ancre-Haute, vue d'ensemble schématique (espace, sans grille).
- maps/pm_colchide_master.png : carte maîtresse du réseau souterrain (boucle, 6 gares, percées vhurr, grille 1 case = 1,5 m pour le combat local).
- generator/ : générateur Python pur stdlib, rendu déterministe, grille 44 px.

## À venir

Decks détaillés d'Ancre-Haute, cartes de bataille des gares, la Chambre, carte de wagon réutilisable, tokens (vhurr, cultistes, personnel Nordkraft, trains), statistiques etPNJ.

## Importation owlbear.rodeo

Importer les PNG comme maps, échelle de grille 44 px, 1 case = 1,5 m. Compatibilité grille conforme à hard-vacuum-01 et hard-vacuum-02.
