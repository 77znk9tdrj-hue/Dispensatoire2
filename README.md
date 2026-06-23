# Épreuve - Parc de véhicules de location

Programmation Orientée Objet

## Ce que vous devez faire

Quatre fichiers sont **à compléter** : `tarif.py`, `vehicule.py`,
`flotte.py`, `persistance.py`. Ils ne contiennent que les **signatures**
des méthodes et des **indices** en commentaire `#`. À vous d'écrire le
corps de chaque méthode (les `...`).

Les fichiers `test_*.py` sont **fournis complets**. Ils constituent la
**spécification** : ils fixent les valeurs de retour exactes, l'ordre,
les égalités et les exceptions attendues. **Vous ne les modifiez pas.**
Votre travail est réussi quand toute la batterie passe au vert.

> Pour cette épreuve **uniquement**, les **docstrings ne sont pas
> demandées** (dérogation exceptionnelle à la règle du cours). Les
> indices `#` déjà présents suffisent ; n'en ajoutez pas d'autres.

## L'idée : transposer ce que vous connaissez

Le domaine est **calqué** sur celui des livres travaillé tout au long de
l'année. Si vous avez pratiqué les cas `Livre` / `Bibliotheque` /
persistance, vous reconnaîtrez chaque méthode :

| Vous connaissez (livres) | À écrire ici (véhicules) |
|---|---|
| `Livre` (identité par ISBN) | `Vehicule` (identité par châssis) |
| `LivreNumerique` (enrichit) | `VoitureElectrique` (enrichit) |
| `LivreAudio` (remplace) | `Camion` (remplace) |
| `Bibliotheque` | `Flotte` |
| `depuis_chaine_csv` | `depuis_csv` |
| `to_dict` / `from_dict` + registre | idem |
| objet-valeur `Argent` | objet-valeur `Tarif` |

## Comment travailler

1. Lisez d'abord le fichier de tests correspondant : il vous dit
   exactement ce que la méthode doit produire.
2. Complétez les `...`, une classe à la fois.
3. Lancez les tests souvent :

```bash
python -m unittest test_tarif -v
python -m unittest test_vehicule -v
python -m unittest test_flotte -v
python -m unittest test_persistance -v
```

   Ou tout d'un coup :

```bash
python -m unittest discover -p "test_*.py" -v
```

## Remise : fork + pull request

1. **Forkez** ce dépôt sur votre compte GitHub.
2. Clonez votre fork, complétez les quatre fichiers, **committez**.
3. Poussez sur votre fork.
4. Ouvrez une **pull request** vers le dépôt d'origine **avant la fin du
   cours**.

Ne committez ni fichiers générés (`__pycache__`, `*.json` de test) ni
fichiers d'environnement : le `.gitignore` est déjà configuré.

## Critères d'évaluation

L'épreuve couvre les trois acquis d'apprentissage :

- **AA1** - concevoir et coder les classes et fonctions demandées ;
- **AA2** - faire passer la totalité des tests fournis (vert) ;
- **AA3** - vos choix sont déjà cadrés par les tests ; ce qui est évalué,
  c'est leur mise en œuvre correcte et cohérente (entité vs objet-valeur,
  enrichissement vs remplacement, dispatch sans `isinstance`, registre).
