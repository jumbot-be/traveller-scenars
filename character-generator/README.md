# Character Generator — API Cepheus Engine (Traveller SRD)

Mini-serveur HTTP (Python 3, **stdlib uniquement, aucune dépendance**) qui génère des
personnages Traveller / Cepheus Engine à la volée, en respectant la procédure de création
du **Cepheus Engine SRD** (contenu Open Gaming, OGL — Samardan Press). Le futur bot Discord
fera simplement un appel à cette API (`POST /api/characters`) pour générer un personnage,
puis l'affichera. Prochaines extensions prévues : véhicules (VDS), vaisseaux, robots.

## Règles implémentées (checklist SRD, chapitre 1)

1. **Caractéristiques** : 2D6 pour STR, DEX, END, INT, EDU, SOC ; DM = ⌊score/3⌋ − 2 ; UPP en pseudo-hex (`687B9C`). Âge de départ 18, caractéristiques plafonnées à 15.
2. **Monde natal (optionnel)** : compétences de background = `3 + DM EDU` au niveau 0 (2 premières liées au monde natal si `--homeworld`, le reste depuis la liste d'éducation).
3. **Carrière** : 24 carrières du SRD (voir `cepheus/data/careers.json`, parsé depuis le SRD par `tools/parse_srd_careers.py`). Jet de qualification `2D6 + DM carac − 2 × carrières précédentes` ; en cas d'échec : Drifter ou Tirage au sort (une seule fois). On ne peut pas reprendre une carrière quittée (sauf Drifter).
4. **Formation de base** : 1ʳᵉ carrière → toutes les compétences du tableau Service à 0 ; carrières suivantes → une au choix.
5. **Survie** : `2D6 + DM ≥ cible` de la carrière ; un 2 naturel est toujours un échec → **mort** (règle optionnelle `survival_mishap` : table des mésaventures, demi-terme, pas de bénéfice pour ce terme).
6. **Commission & avancement** : rang 0 au départ ; commission → rang 1 + jet de compétence + compétence de rang ; avancement (rang ≥ 1, max 6) idem. Les carrières sans hiérarchie (Athlete, Barbarian, Belter, Drifter, Entertainer, Hunter, Scout) donnent **2 jets de compétence par terme**.
7. **Compétences** : à chaque terme, 1 jet 1D6 sur une table au choix (Développement perso / Service / Spécialiste / Éducation avancée si EDU 8+). Compétences en cascade résolues avec spécialisation (`Gun Combat (Slug Rifle)`).
8. **Vieillissement** : à partir de 34 ans (fin du 4ᵉ terme), `2D6 − nombre total de termes` sur la table de vieillissement ; caractéristique à 0 → crise (mort sauf paiement de `1D6×10 000 Cr`, puis échec automatique aux qualifications).
9. **Réengagement** : `2D6 ≥ cible` pour rester ; 12 naturel = on reste obligatoirement ; **7 termes ou plus = retraite obligatoire** (sauf 12 naturel).
10. **Démobilisation** : 1 jet de bénéfice par terme plein (+1 si rang O4, +2 si O5, +3 si O6) ; max 3 jets en cash (1D6, +1 si skill Gambling ou retraité), le reste en matériel (1D6, +1 si rang O5+) ; pension annuelle à partir de 5 termes dans la même carrière.

Chaque personnage embarque un `history` complet (tous les jets avec dés, DM et cibles), donc
la génération est **auditable et reproductible** via le `seed`.

## Arborescence

```
character-generator/
├── README.md                  ce fichier
├── server.py                  mini-serveur API HTTP (stdlib : http.server)
├── cli.py                     génération en ligne de commande (JSON ou texte)
├── cepheus/
│   ├── __init__.py
│   ├── dice.py                RNG seedé (reproductible)
│   ├── data.py                règles statiques SRD (vieillissement, blessures, draft, cascades...)
│   ├── data/careers.json      les 24 carrières (généré depuis le SRD)
│   └── character.py           moteur de génération (Generator)
├── tools/
│   └── parse_srd_careers.py   parseur SRD -> cepheus/data/careers.json
└── tests/                     tests unitaires (stdlib unittest)
```

## Utilisation

```sh
cd character-generator

# tests
python3 -m unittest discover -s tests -v

# CLI : un personnage reproductible en texte
python3 cli.py --seed 42 --text

# CLI : 5 personnages JSON, carrière forcée
python3 cli.py --count 5 --career marine --out persos.json

# mini-serveur API (loopback par défaut)
python3 server.py --host 127.0.0.1 --port 8080
```

## API

| Méthode | Route | Description |
| --- | --- | --- |
| GET | `/api/health` | statut du service |
| GET | `/api/careers` | les 24 carrières (résumé) |
| GET | `/api/careers/<key>` | détail d'une carrière (tables complètes) |
| POST | `/api/characters` | génère `count` personnage(s), renvoie la fiche complète + `id` |
| GET | `/api/characters` | liste des personnages générés (résumés) |
| GET | `/api/characters/<id>` | fiche complète JSON d'un personnage |
| GET | `/api/characters/<id>/text` | fiche en texte brut (format "Universal Character Format") |

### `POST /api/characters`

Corps JSON optionnel (tous les champs sont optionnels) :

```json
{
  "count": 1,
  "seed": 42,
  "career": "marine",
  "max_terms": 7,
  "p_stay": 0.5,
  "p_new_career": 0.5,
  "p_draft": 0.5,
  "survival_mishap": false,
  "background_skills": true,
  "homeworld": false,
  "name": "Rio Zhaleo",
  "gender": "M"
}
```

- `seed` : entier → génération reproductible (les seeds enfants sont dérivés du seed du lot).
- `career` : clé ou nom d'une des 24 carrières pour la **première** carrière (`"random"` / absent = aléatoire).
- `max_terms` : 1–12 (défaut 7, la règle SRD).
- `p_stay` / `p_new_career` / `p_draft` : probabilités de rester dans la carrière, de commencer une
  nouvelle carrière, de tenter le tirage au sort après un échec de qualification.
- `survival_mishap` : règle optionnelle SRD (mésaventure au lieu de mort).

Exemple :

```sh
curl -s -X POST http://127.0.0.1:8080/api/characters \
  -H 'Content-Type: application/json' \
  -d '{"count": 1, "seed": 2024, "career": "scout"}' | python3 -m json.tool
```

Réponse `201` : `{"characters": [ { ...fiche complète..., "id": "14bf9ff47920" } ]}`.
La fiche contient `name`, `upp`, `age`, `characteristics` (valeur + DM), `skills`, `careers`
(termes, rang, titre, bénéfices, pension), `credits`, `passages`, `ship_shares`, `equipment`,
`alive` / `death_cause`, `homeworld`, et `history` (journal de tous les jets).

## Pour le bot Discord (étape suivante)

Commande slash type `/personnage [carrière] [seed]` → le bot fait
`POST http://<hôte>:<port>/api/characters` avec `{"career": ..., "seed": ...}`, puis poste
la fiche (JSON ou `/text`) dans le salon. Le serveur écoute par défaut sur `127.0.0.1`
(loopback) ; à n'exposer que sur le réseau local du bot.

## Sources et licence

Règles et tables : **Cepheus Engine System Reference Document**, Samardan Press (Jason "Flynn"
Kemp), contenu Open Gaming sous OGL — PDF sur DriveThruRPG, miroir HTML/markdown :
<https://github.com/orffen/cepheus-srd> (`src/book1/character-creation.md`, `src/book1/skills.md`).
`cepheus/data/careers.json` est généré depuis ce SRD par `tools/parse_srd_careers.py`.
Les titres de produits et marques (Cepheus Engine, Samardan Press) restent la propriété de leurs
ayants droit ; le code de ce dépôt est sous la licence du dépôt.
