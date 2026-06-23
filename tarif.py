# tarif.py - À COMPLÉTER (épreuve flotte)
#
# Objet-valeur Tarif, à transposer de l'objet-valeur Argent (S11).
# Pour cette épreuve, aucune docstring n'est demandée : les indices «#»
# donnent le ROLE, et les tests (test_tarif.py) fixent les valeurs
# exactes, l'ordre et les exceptions. Complétez les corps « ... ».

from functools import total_ordering


@total_ordering
class Tarif:
    # Objet-valeur IMMUABLE : l'égalité ET l'ordre portent sur la VALEUR
    # (montant + devise), pas sur l'identité mémoire. C'est le contraste
    # avec Vehicule, qui est une entité (identité par châssis).

    def __init__(self, montant, devise="EUR"):
        # Refuser un montant strictement négatif ; stocker le montant en float.
        if montant < 0:
            raise ValueError("montant negatif")
        self._montant = float(montant)
        self._devise = devise

    @property
    def montant(self):
        return self._montant

    @property
    def devise(self):
        return self._devise

    def __eq__(self, autre):
        # Égalité de valeur : même montant ET même devise.
        # Renvoyer NotImplemented si « autre » n'est pas un Tarif.
        if not isinstance(autre, Tarif):
            return NotImplemented
        return(
            self.montant == autre.montant and self.devise == autre.devise
        )

    def __hash__(self):
        # Cohérent avec __eq__ : hacher le couple (montant, devise).
        return hash((self.montant, self.devise))

    def __lt__(self, autre):
        # Comparer deux Tarif de MÊME devise ; devises différentes -> erreur.
        # Comme Argent : __lt__ + @total_ordering suffisent à dériver tout
        # le reste de l'ordre (<=, >, >=).
        if not isinstance(autre, Tarif):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError("devise differentes")
        return self.montant < autre.montant

    def __add__(self, autre):
        # Additionner deux Tarif de MÊME devise -> un NOUVEAU Tarif.
        # NotImplemented si « autre » n'est pas un Tarif (l'addition avec un
        # nombre doit échouer, pas réussir silencieusement).
        if not isinstance(autre, Tarif):
            return NotImplemented
        if self.devise != autre.devise:
            raise ValueError("devises differentes")
        return Tarif(
            self.montant + autre.montant,
            self.devise
        )

    def __str__(self):
        return f"{self.montant:.2f} {self.devise}"

    def __repr__(self):
        return f"tarif({self.montant!r}, {self.devise!r})"
