# vehicule.py - À COMPLÉTER (épreuve flotte)
#
# Hiérarchie Vehicule / VoitureElectrique / Camion, à transposer de la
# hiérarchie Livre / LivreNumerique / LivreAudio (S11-S18).
# Pour cette épreuve, aucune docstring n'est demandée : les indices «#»
# donnent le RÔLE (et parfois le cas analogue à transposer), et les
# tests (test_vehicule.py) fixent les valeurs et exceptions exactes.
# Complétez les corps « ... ».


class Vehicule:
    # ENTITE largement immuable. Identité métier : le numéro de châssis
    # (qui ne change jamais, contrairement à la plaque). Seule la
    # disponibilité évolue. Transposé de Livre (identité par ISBN).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):

        if not isinstance(marque, str) or not marque.strip():
            raise ValueError()

        if not isinstance(modele, str) or not modele.strip():
            raise ValueError()

        if not self.chassis_valide(numero_chassis):
            raise ValueError()

        if type(nb_places) is not int:
            raise TypeError()

        if not (1 <= nb_places <= 80):
            raise ValueError()

        if type(annee) is not int:
            raise TypeError()

        if annee < 1886:
            raise ValueError()

        self._marque = marque
        self._modele = modele
        self._numero_chassis = numero_chassis
        self._nb_places = nb_places
        self._annee = annee
        self._disponible = True

    # --- Propriétés en lecture seule ---

    @property
    def marque(self):
        return self._marque

    @property
    def modele(self):
        return self._modele

    @property
    def numero_chassis(self):
        return self._numero_chassis

    @property
    def nb_places(self):
        return self._nb_places

    @property
    def annee(self):
        return self._annee

    @property
    def disponible(self):
        return self._disponible

    # --- Méthode statique ---

    @staticmethod
    def chassis_valide(chaine):
        if not isinstance(chaine, str):
            return False

        return len(chaine) == 17 and chaine.isalnum()

    # --- Constructeur alternatif ---

    @classmethod
    def depuis_csv(cls, ligne):
        morceaux = ligne.split(";")

        if len(morceaux) != 5:
            raise ValueError()

        marque, modele, chassis, places, annee = morceaux

        return cls(
            marque,
            modele,
            chassis,
            int(places),
            int(annee)
        )

    # --- Sérialisation JSON ---

    def to_dict(self):
        return {
            "type": "Vehicule",
            "marque": self.marque,
            "modele": self.modele,
            "numero_chassis": self.numero_chassis,
            "nb_places": self.nb_places,
            "annee": self.annee,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, donnees):
        vehicule = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"]
        )

        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    @staticmethod
    def _restaurer_disponibilite(vehicule, donnees):
        if not donnees.get("disponible", True):
            vehicule.louer()

    # --- Méthodes métier ---

    def louer(self):
        if not self.disponible:
            raise ValueError()

        self._disponible = False

    def restituer(self):
        if self.disponible:
            raise ValueError()

        self._disponible = True

    def fiche_resume(self):
        return f"{self.nb_places} places"

    # --- Représentations ---

    def __str__(self):
        etat = "disponible" if self.disponible else "loué"
        return f"{self.marque} {self.modele} ({etat})"

    def __repr__(self):
        return (
            f"Vehicule({self.marque!r}, {self.modele!r}, "
            f"{self.numero_chassis!r}, {self.nb_places!r}, "
            f"{self.annee!r})"
        )

    # --- Identité (entité) ---

    def __eq__(self, autre):
        if not isinstance(autre, Vehicule):
            return NotImplemented

        return self.numero_chassis == autre.numero_chassis

    def __hash__(self):
        return hash(self.numero_chassis)


class VoitureElectrique(Vehicule):
    # Enrichit Vehicule d'une autonomie. Transposé de LivreNumerique.

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 autonomie_km):

        super().__init__(
            marque,
            modele,
            numero_chassis,
            nb_places,
            annee
        )

        if type(autonomie_km) is not int:
            raise TypeError()

        if autonomie_km <= 0:
            raise ValueError()

        self._autonomie_km = autonomie_km

    @property
    def autonomie_km(self):
        return self._autonomie_km

    @classmethod
    def depuis_csv(cls, ligne):
        morceaux = ligne.split(";")

        if len(morceaux) != 6:
            raise ValueError()

        marque, modele, chassis, places, annee, autonomie = morceaux

        return cls(
            marque,
            modele,
            chassis,
            int(places),
            int(annee),
            int(autonomie)
        )

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "VoitureElectrique"
        d["autonomie_km"] = self.autonomie_km
        return d

    @classmethod
    def from_dict(cls, donnees):
        vehicule = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["autonomie_km"]
        )

        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    def fiche_resume(self):
        return (
            f"{super().fiche_resume()} "
            f"[électrique, {self.autonomie_km} km]"
        )

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return (
            f"VoitureElectrique({self.marque!r}, {self.modele!r}, "
            f"{self.numero_chassis!r}, {self.nb_places!r}, "
            f"{self.annee!r}, {self.autonomie_km!r})"
        )


class Camion(Vehicule):
    # La mesure pertinente est la charge utile, pas le nombre de places.
    # Transposé de LivreAudio (durée d'écoute plutôt que pages).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 charge_utile_t):

        super().__init__(
            marque,
            modele,
            numero_chassis,
            nb_places,
            annee
        )

        charge_utile_t = float(charge_utile_t)

        if charge_utile_t <= 0:
            raise ValueError()

        self._charge_utile_t = charge_utile_t

    @property
    def charge_utile_t(self):
        return self._charge_utile_t

    @classmethod
    def depuis_csv(cls, ligne):
        morceaux = ligne.split(";")

        if len(morceaux) != 6:
            raise ValueError()

        marque, modele, chassis, places, annee, charge = morceaux

        return cls(
            marque,
            modele,
            chassis,
            int(places),
            int(annee),
            float(charge)
        )

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "Camion"
        d["charge_utile_t"] = self.charge_utile_t
        return d

    @classmethod
    def from_dict(cls, donnees):
        vehicule = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["charge_utile_t"]
        )

        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    def fiche_resume(self):
        return f"{self.charge_utile_t} t de charge"

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return (
            f"Camion({self.marque!r}, {self.modele!r}, "
            f"{self.numero_chassis!r}, {self.nb_places!r}, "
            f"{self.annee!r}, {self.charge_utile_t!r})"
        )