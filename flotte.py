# flotte.py - À COMPLÉTER (épreuve flotte)
#
# Conteneur Flotte, à transposer de Bibliotheque (S12) : enveloppe
# encapsulée d'une liste de Vehicule, exposant len(), in et for.
# Aucune docstring demandée ; les tests (test_flotte.py) fixent le
# comportement exact. Complétez les corps « ... ».

from vehicule import Vehicule


class Flotte:
    # Garde l'ordre d'ajout, refuse les doublons par châssis, et expose
    # les protocoles de conteneur. La hiérarchie Vehicule la traverse
    # sans aucune modification (polymorphisme) : ni isinstance ni cas
    # particulier par sous-type.

    def __init__(self):
        # Collection interne : une liste (préserve l'ordre d'ajout).
        self._vehicule = []

    # --- ajouter, retirer ---

    def ajouter(self, vehicule):
        # Refuser un objet qui n'est pas un Vehicule (TypeError) et un
        # doublon de châssis déjà présent (ValueError). Indice : « déjà
        # présent ? » se teste élégamment avec l'opérateur « in » sur self.
        if not isinstance(vehicule, Vehicule):
            raise TypeError()
        if vehicule in self:
            raise ValueError()
        self._vehicule.append(vehicule)

    def retirer(self, vehicule):
        # Refuser un non-Vehicule (TypeError) ; absent -> KeyError.
        # __eq__ de Vehicule (par châssis) localise l'élément à retirer.
        if not isinstance(vehicule, Vehicule):
            raise TypeError()
        if vehicule not in self:
            raise KeyError()
        self._vehicules.remove(vehicule)

    # --- Protocole de conteneur ---

    def __len__(self):
        return len(self._vehicule)

    def __contains__(self, item):
        # Accepter soit un Vehicule (comparé par châssis via __eq__), soit
        # une chaîne de châssis. Tout autre type -> False (sans lever).
        if isinstance(item, Vehicule):
            return item in self._vehicule
        if isinstance(item, str):
            return any(
                v.numero_chassis == item
                for v in self._vehicule
            )
        return False

    def __iter__(self):
        # Itérer dans l'ordre d'ajout.
        return iter(self._vehicule)


    # --- Méthodes métier ---

    def trouver_par_chassis(self, numero_chassis):
        # Renvoyer le véhicule de ce châssis ; absent -> KeyError.
        for v in self._vehicule:
            if v.numero_chassis == numero_chassis:
                return v
        raise KeyError(numero_chassis)

    def vehicules_disponibles(self):
        # Liste des véhicules dont disponible vaut True, dans l'ordre d'ajout.
        return[
            v for v in self._vehicule
            if v.disponible
        ]

    @property
    def nombre_disponibles(self):
        return len(self.vehicules_disponibles())

    # --- Représentation ---

    def __repr__(self):
        return f"flotte({self._vehicule!r})"
