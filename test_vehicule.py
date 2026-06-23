"""Tests de la hiérarchie Vehicule (épreuve flotte).

Ces tests CONSTITUENT la spécification de Vehicule, VoitureElectrique
et Camion : valeurs de retour exactes, comportement polymorphe,
identité, sérialisation et exceptions. Organisés en classes thématiques.

Exécution : python -m unittest test_vehicule -v
"""

import unittest

from vehicule import Vehicule, VoitureElectrique, Camion


# Châssis valides (17 caractères alphanumériques) réutilisés partout.
CH1 = "VF1AAAAA11A111111"
CH2 = "5YJ3E1EA7KF000000"
CH3 = "YV2AAAAA11A222222"


class TestConstruction(unittest.TestCase):
    """Construction, validation et lecture seule de Vehicule."""

    def test_attributs(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        self.assertEqual(v.marque, "Renault")
        self.assertEqual(v.modele, "Clio")
        self.assertEqual(v.numero_chassis, CH1)
        self.assertEqual(v.nb_places, 5)
        self.assertEqual(v.annee, 2018)

    def test_disponible_a_la_construction(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        self.assertTrue(v.disponible)

    def test_marque_vide_refusee(self):
        with self.assertRaises(ValueError):
            Vehicule("  ", "Clio", CH1, 5, 2018)

    def test_chassis_mauvaise_longueur_refuse(self):
        with self.assertRaises(ValueError):
            Vehicule("Renault", "Clio", "TROPCOURT", 5, 2018)

    def test_chassis_non_alphanumerique_refuse(self):
        with self.assertRaises(ValueError):
            Vehicule("Renault", "Clio", "VF1AAAAA11A11-11!", 5, 2018)

    def test_nb_places_non_entier_leve_typeerror(self):
        with self.assertRaises(TypeError):
            Vehicule("Renault", "Clio", CH1, 5.0, 2018)

    def test_nb_places_hors_plage_leve_valueerror(self):
        with self.assertRaises(ValueError):
            Vehicule("Renault", "Clio", CH1, 0, 2018)
        with self.assertRaises(ValueError):
            Vehicule("Renault", "Clio", CH1, 81, 2018)

    def test_annee_hors_plage_leve_valueerror(self):
        with self.assertRaises(ValueError):
            Vehicule("Renault", "Clio", CH1, 5, 1850)

    def test_bool_refuse_pour_nb_places(self):
        # True ne doit pas passer pour un entier valide.
        with self.assertRaises(TypeError):
            Vehicule("Renault", "Clio", CH1, True, 2018)

    def test_lecture_seule(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        with self.assertRaises(AttributeError):
            v.nb_places = 7


class TestChassisValide(unittest.TestCase):
    """Méthode statique chassis_valide."""

    def test_valide(self):
        self.assertTrue(Vehicule.chassis_valide(CH1))

    def test_mauvaise_longueur(self):
        self.assertFalse(Vehicule.chassis_valide("ABC123"))

    def test_non_alphanumerique(self):
        self.assertFalse(Vehicule.chassis_valide("VF1AAAAA11A1111 1"))

    def test_non_chaine(self):
        self.assertFalse(Vehicule.chassis_valide(12345678901234567))


class TestMetier(unittest.TestCase):
    """Cycle de location : louer / restituer."""

    def test_louer_rend_indisponible(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        v.louer()
        self.assertFalse(v.disponible)

    def test_restituer_rend_disponible(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        v.louer()
        v.restituer()
        self.assertTrue(v.disponible)

    def test_louer_deux_fois_leve(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        v.louer()
        with self.assertRaises(ValueError):
            v.louer()

    def test_restituer_disponible_leve(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        with self.assertRaises(ValueError):
            v.restituer()


class TestFicheResume(unittest.TestCase):
    """fiche_resume : le cœur du polymorphisme (dispatch dynamique)."""

    def test_vehicule_generique(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        self.assertEqual(v.fiche_resume(), "5 places")

    def test_voiture_electrique_enrichit(self):
        # La capacité reste un préfixe ; l'autonomie est ajoutée.
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        self.assertEqual(ve.fiche_resume(), "5 places [électrique, 420 km]")

    def test_camion_remplace(self):
        # Le nombre de places disparaît : la mesure devient la charge.
        c = Camion("Volvo", "FH16", CH3, 2, 2020, 12.0)
        self.assertEqual(c.fiche_resume(), "12.0 t de charge")

    def test_dispatch_sans_isinstance(self):
        parc = [
            Vehicule("Renault", "Clio", CH1, 5, 2018),
            VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420),
            Camion("Volvo", "FH16", CH3, 2, 2020, 3.5),
        ]
        resumes = [v.fiche_resume() for v in parc]
        self.assertEqual(
            resumes,
            ["5 places", "5 places [électrique, 420 km]", "3.5 t de charge"],
        )


class TestHeritage(unittest.TestCase):
    """Héritage et identité propagée."""

    def test_voiture_est_un_vehicule(self):
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        self.assertIsInstance(ve, Vehicule)

    def test_camion_est_un_vehicule(self):
        c = Camion("Volvo", "FH16", CH3, 2, 2020, 12.0)
        self.assertIsInstance(c, Vehicule)

    def test_validation_heritee_appliquee(self):
        # La plage d'année (héritée) s'applique aussi aux sous-classes.
        with self.assertRaises(ValueError):
            VoitureElectrique("Tesla", "Model 3", CH2, 5, 1850, 420)

    def test_attribut_propre_voiture(self):
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        self.assertEqual(ve.autonomie_km, 420)

    def test_attribut_propre_camion(self):
        c = Camion("Volvo", "FH16", CH3, 2, 2020, 12.0)
        self.assertEqual(c.charge_utile_t, 12.0)

    def test_autonomie_non_positive_refusee(self):
        with self.assertRaises(ValueError):
            VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 0)

    def test_charge_non_positive_refusee(self):
        with self.assertRaises(ValueError):
            Camion("Volvo", "FH16", CH3, 2, 2020, 0)


class TestIdentite(unittest.TestCase):
    """Égalité et hachage par numéro de châssis (entité)."""

    def test_egalite_par_chassis(self):
        # Même châssis = même véhicule, même si le reste diffère.
        a = Vehicule("Renault", "Clio", CH1, 5, 2018)
        b = Vehicule("Peugeot", "208", CH1, 5, 2019)
        self.assertEqual(a, b)

    def test_chassis_different_non_egal(self):
        a = Vehicule("Renault", "Clio", CH1, 5, 2018)
        b = Vehicule("Renault", "Clio", CH3, 5, 2018)
        self.assertNotEqual(a, b)

    def test_identite_cross_type(self):
        # Un Vehicule et une VoitureElectrique de même châssis sont égaux.
        v = Vehicule("Tesla", "Model 3", CH2, 5, 2022)
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        self.assertEqual(v, ve)

    def test_hash_par_chassis(self):
        a = Vehicule("Renault", "Clio", CH1, 5, 2018)
        b = Vehicule("Peugeot", "208", CH1, 5, 2019)
        self.assertEqual(hash(a), hash(b))

    def test_dedoublonnage_par_set(self):
        # Le set s'appuie sur __eq__/__hash__ : un seul exemplaire par châssis.
        a = Vehicule("Renault", "Clio", CH1, 5, 2018)
        b = Vehicule("Peugeot", "208", CH1, 5, 2019)
        c = Vehicule("Volvo", "V40", CH3, 5, 2020)
        self.assertEqual(len({a, b, c}), 2)

    def test_pas_d_ordre_canonique(self):
        # Vehicule est une ENTITE : pas de __lt__, donc sorted() lève.
        # Pour trier, il faut fournir une clé (sorted(..., key=...)).
        parc = [
            Vehicule("Renault", "Clio", CH1, 5, 2018),
            Vehicule("Volvo", "V40", CH3, 5, 2020),
        ]
        with self.assertRaises(TypeError):
            sorted(parc)
        # Avec une clé, le tri fonctionne.
        tries = sorted(parc, key=lambda v: v.marque)
        self.assertEqual([v.marque for v in tries], ["Renault", "Volvo"])


class TestConstructeurCsv(unittest.TestCase):
    """Constructeur alternatif depuis_csv (cls -> type exact)."""

    def test_vehicule_depuis_csv(self):
        v = Vehicule.depuis_csv(f"Renault;Clio;{CH1};5;2018")
        self.assertIsInstance(v, Vehicule)
        self.assertEqual(v.marque, "Renault")
        self.assertEqual(v.nb_places, 5)

    def test_voiture_depuis_csv_type_exact(self):
        ve = VoitureElectrique.depuis_csv(f"Tesla;Model 3;{CH2};5;2022;420")
        # Type EXACT, pas un parent générique.
        self.assertIs(type(ve), VoitureElectrique)
        self.assertEqual(ve.autonomie_km, 420)

    def test_camion_depuis_csv_type_exact(self):
        c = Camion.depuis_csv(f"Volvo;FH16;{CH3};2;2020;12.5")
        self.assertIs(type(c), Camion)
        self.assertEqual(c.charge_utile_t, 12.5)

    def test_mauvais_nombre_de_champs(self):
        with self.assertRaises(ValueError):
            Vehicule.depuis_csv(f"Renault;Clio;{CH1};5")  # 4 champs
        with self.assertRaises(ValueError):
            VoitureElectrique.depuis_csv(f"Tesla;Model 3;{CH2};5;2022")  # 5


class TestRepresentations(unittest.TestCase):
    """__str__ et __repr__."""

    def test_str_mentionne_etat(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        self.assertIn("disponible", str(v))
        v.louer()
        self.assertIn("loué", str(v))

    def test_repr_reconstructible(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        reconstruit = eval(repr(v))
        self.assertEqual(reconstruit, v)

    def test_repr_voiture_reconstructible(self):
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        reconstruit = eval(repr(ve))
        self.assertIs(type(reconstruit), VoitureElectrique)
        self.assertEqual(reconstruit.autonomie_km, 420)


if __name__ == "__main__":
    unittest.main(verbosity=2)
