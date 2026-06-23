"""Tests du conteneur Flotte (épreuve flotte).

Ces tests CONSTITUENT la spécification de Flotte : protocoles de
conteneur (len, in, for), ajout/retrait, recherche, et traversée
polymorphe de la hiérarchie Vehicule sans isinstance.

Exécution : python -m unittest test_flotte -v
"""

import unittest

from vehicule import Vehicule, VoitureElectrique, Camion
from flotte import Flotte


CH1 = "VF1AAAAA11A111111"
CH2 = "5YJ3E1EA7KF000000"
CH3 = "YV2AAAAA11A222222"


def flotte_exemple():
    """Construit une flotte hétérogène de trois véhicules."""
    f = Flotte()
    f.ajouter(Vehicule("Renault", "Clio", CH1, 5, 2018))
    f.ajouter(VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420))
    f.ajouter(Camion("Volvo", "FH16", CH3, 2, 2020, 12.0))
    return f


class TestAjout(unittest.TestCase):
    """Ajout et refus des doublons / types invalides."""

    def test_ajouter_augmente_la_taille(self):
        f = Flotte()
        self.assertEqual(len(f), 0)
        f.ajouter(Vehicule("Renault", "Clio", CH1, 5, 2018))
        self.assertEqual(len(f), 1)

    def test_doublon_chassis_refuse(self):
        f = Flotte()
        f.ajouter(Vehicule("Renault", "Clio", CH1, 5, 2018))
        with self.assertRaises(ValueError):
            f.ajouter(Vehicule("Peugeot", "208", CH1, 5, 2019))

    def test_type_invalide_refuse(self):
        f = Flotte()
        with self.assertRaises(TypeError):
            f.ajouter("pas un véhicule")

    def test_sous_classes_acceptees(self):
        # Aucune modification de Flotte n'a été nécessaire (polymorphisme).
        f = flotte_exemple()
        self.assertEqual(len(f), 3)


class TestProtocoleConteneur(unittest.TestCase):
    """len(), in et for."""

    def test_len(self):
        self.assertEqual(len(flotte_exemple()), 3)

    def test_in_avec_vehicule(self):
        f = flotte_exemple()
        cible = Vehicule("Autre", "Modele", CH1, 5, 2000)
        self.assertIn(cible, f)  # comparaison par châssis

    def test_in_avec_chaine_chassis(self):
        f = flotte_exemple()
        self.assertIn(CH2, f)
        self.assertNotIn("INCONNU0000000000", f)

    def test_in_autre_type_renvoie_false(self):
        f = flotte_exemple()
        self.assertNotIn(42, f)  # ne lève pas, renvoie False

    def test_iteration_ordre_d_ajout(self):
        f = flotte_exemple()
        chassis = [v.numero_chassis for v in f]
        self.assertEqual(chassis, [CH1, CH2, CH3])

    def test_iteration_polymorphe(self):
        # for traverse la flotte et chaque véhicule répond à sa façon.
        f = flotte_exemple()
        resumes = [v.fiche_resume() for v in f]
        self.assertEqual(
            resumes,
            ["5 places", "5 places [électrique, 420 km]", "12.0 t de charge"],
        )


class TestRetrait(unittest.TestCase):
    """Retrait par véhicule."""

    def test_retirer_diminue_la_taille(self):
        f = flotte_exemple()
        f.retirer(Vehicule("Renault", "Clio", CH1, 5, 2018))
        self.assertEqual(len(f), 2)
        self.assertNotIn(CH1, f)

    def test_retirer_absent_leve_keyerror(self):
        f = flotte_exemple()
        with self.assertRaises(KeyError):
            f.retirer(Vehicule("X", "Y", "ZZZZZZZZZZZZZZZZZ", 5, 2000))

    def test_retirer_type_invalide_leve_typeerror(self):
        f = flotte_exemple()
        with self.assertRaises(TypeError):
            f.retirer(CH1)  # une chaîne n'est pas un Vehicule


class TestRecherche(unittest.TestCase):
    """trouver_par_chassis, vehicules_disponibles, nombre_disponibles."""

    def test_trouver_par_chassis(self):
        f = flotte_exemple()
        v = f.trouver_par_chassis(CH2)
        self.assertIs(type(v), VoitureElectrique)

    def test_trouver_absent_leve_keyerror(self):
        f = flotte_exemple()
        with self.assertRaises(KeyError):
            f.trouver_par_chassis("INCONNU0000000000")

    def test_vehicules_disponibles(self):
        f = flotte_exemple()
        f.trouver_par_chassis(CH1).louer()
        dispos = f.vehicules_disponibles()
        self.assertEqual(len(dispos), 2)
        self.assertNotIn(CH1, [v.numero_chassis for v in dispos])

    def test_nombre_disponibles(self):
        f = flotte_exemple()
        self.assertEqual(f.nombre_disponibles, 3)
        f.trouver_par_chassis(CH1).louer()
        self.assertEqual(f.nombre_disponibles, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
