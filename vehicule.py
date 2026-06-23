class Vehicule:
    # ENTITE largement immuable. Identité métier : le numéro de châssis
    # (qui ne change jamais, contrairement à la plaque). Seule la
    # disponibilité évolue. Transposé de Livre (identité par ISBN).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):
        # Valider chaque caractéristique avant de la stocker :
        #   - marque, modèle : chaînes non vides ;
        #   - châssis : utiliser la méthode de validation dédiée ;
        #   - nb_places, année : entiers, bornes exactes dans les tests.
        # Distinguer TypeError (mauvais type) et ValueError (mauvaise valeur).
        # À la création, le véhicule est disponible.

        if not isinstance(marque, str):
            raise TypeError()
        if not marque.strip():
            raise ValueError()

        if not isinstance(modele, str):
            raise TypeError()
        if not modele.strip():
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
        # Vrai si la chaîne a exactement la bonne longueur et n'est faite
        # que de caractères alphanumériques. Longueur et nature exactes :
        # déductibles des tests. Une entrée non-str renvoie False.

        if not isinstance(chaine, str):
            return False

        return len(chaine) == 17 and chaine.isalnum()

    # --- Constructeur alternatif ---

    @classmethod
    def depuis_csv(cls, ligne):
        # Découper la ligne, vérifier le nombre de champs, construire via
        # cls(...). Même rôle que Livre.depuis_chaine_csv : utiliser cls
        # (et non Vehicule) est ce qui donnera le TYPE EXACT dans les
        # sous-classes.

        champs = ligne.split(";")

        if len(champs) != 5:
            raise ValueError()

        return cls(
            champs[0],
            champs[1],
            champs[2],
            int(champs[3]),
            int(champs[4])
        )

    # --- Sérialisation JSON ---

    def to_dict(self):
        # Produire un dict marqué d'un champ « type » (le discriminateur
        # qui guidera la reconstruction). Clés attendues : voir les tests.

        return {
            "type": "Vehicule",
            "marque": self.marque,
            "modele": self.modele,
            "numero_chassis": self.numero_chassis,
            "nb_places": self.nb_places,
            "annee": self.annee,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, donnees):
        # Pendant de to_dict : reconstruire via cls(...), puis restaurer la
        # disponibilité par l'API publique (jamais en écrivant l'attribut
        # privé). Même logique que Livre.from_dict.

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
        # Si l'objet était loué, le replacer dans cet état via la méthode
        # métier. Factorisé : toutes les sous-classes restaurent pareil.

        if not donnees["disponible"]:
            vehicule.louer()

    # --- Méthodes métier ---

    def louer(self):
        # Bascule vers « loué » ; refuser si déjà loué.

        if not self.disponible:
            raise ValueError()

        self._disponible = False

    def restituer(self):
        # Bascule vers « disponible » ; refuser si déjà disponible.

        if self.disponible:
            raise ValueError()

        self._disponible = True

    def fiche_resume(self):
        # Description de la capacité d'un véhicule générique. Format exact :
        # voir les tests. (Transposé de Livre.taille_estimee.)

        return f"{self.nb_places} places"

    # --- Représentations ---

    def __str__(self):
        etat = "disponible" if self.disponible else "loué"

        return (
            f"{self.marque} {self.modele} "
            f"({self.numero_chassis}) - {etat}"
        )

    def __repr__(self):
        return (
            f"Vehicule("
            f"{self.marque!r}, "
            f"{self.modele!r}, "
            f"{self.numero_chassis!r}, "
            f"{self.nb_places!r}, "
            f"{self.annee!r})"
        )

    # --- Identité (entité) ---

    def __eq__(self, autre):
        # Vehicule est une ENTITE : égalité par numéro de châssis.

        if not isinstance(autre, Vehicule):
            return NotImplemented

        return self.numero_chassis == autre.numero_chassis

    def __hash__(self):
        # Cohérent avec __eq__ : fondé sur le châssis.

        return hash(self.numero_chassis)