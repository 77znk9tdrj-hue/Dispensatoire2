"""Tests de l'objet-valeur Tarif (épreuve flotte).

Ces tests CONSTITUENT la spécification : ils fixent les valeurs de
retour exactes, les égalités, l'ordre et les exceptions attendues.
Un Tarif réussi fait passer la totalité de ce fichier au vert.

Exécution : python -m unittest test_tarif -v
"""

import unittest

from tarif import Tarif


class TestConstruction(unittest.TestCase):
    """Construction et accès en lecture seule."""

    def test_montant_et_devise(self):
        t = Tarif(45.0, "EUR")
        self.assertEqual(t.montant, 45.0)
        self.assertEqual(t.devise, "EUR")

    def test_devise_par_defaut_eur(self):
        t = Tarif(30)
        self.assertEqual(t.devise, "EUR")

    def test_montant_converti_en_float(self):
        t = Tarif(30)
        self.assertIsInstance(t.montant, float)
        self.assertEqual(t.montant, 30.0)

    def test_montant_zero_autorise(self):
        t = Tarif(0)
        self.assertEqual(t.montant, 0.0)

    def test_montant_negatif_refuse(self):
        with self.assertRaises(ValueError):
            Tarif(-1, "EUR")

    def test_lecture_seule(self):
        t = Tarif(45, "EUR")
        with self.assertRaises(AttributeError):
            t.montant = 50


class TestEgalite(unittest.TestCase):
    """Égalité de valeur et hachage."""

    def test_egalite_de_valeur(self):
        # Deux instances distinctes mais de même valeur sont égales.
        self.assertEqual(Tarif(45, "EUR"), Tarif(45, "EUR"))

    def test_difference_de_montant(self):
        self.assertNotEqual(Tarif(45, "EUR"), Tarif(30, "EUR"))

    def test_difference_de_devise(self):
        self.assertNotEqual(Tarif(45, "EUR"), Tarif(45, "USD"))

    def test_hash_coherent_avec_egalite(self):
        self.assertEqual(hash(Tarif(45, "EUR")), hash(Tarif(45, "EUR")))

    def test_utilisable_dans_un_set(self):
        ensemble = {Tarif(45, "EUR"), Tarif(45, "EUR"), Tarif(30, "EUR")}
        self.assertEqual(len(ensemble), 2)

    def test_comparaison_a_autre_type(self):
        # L'égalité à un type étranger est False, pas une erreur.
        self.assertNotEqual(Tarif(45, "EUR"), 45)
        self.assertFalse(Tarif(45, "EUR") == "45 EUR")


class TestOrdre(unittest.TestCase):
    """Ordre canonique (total_ordering) sur une même devise."""

    def test_inferieur(self):
        self.assertLess(Tarif(30, "EUR"), Tarif(45, "EUR"))

    def test_superieur_derive(self):
        # > est dérivé par total_ordering à partir de __lt__ et __eq__.
        self.assertGreater(Tarif(45, "EUR"), Tarif(30, "EUR"))

    def test_inferieur_ou_egal_derive(self):
        self.assertLessEqual(Tarif(45, "EUR"), Tarif(45, "EUR"))

    def test_tri_croissant(self):
        tarifs = [Tarif(45, "EUR"), Tarif(30, "EUR"), Tarif(60, "EUR")]
        ordonnes = sorted(tarifs)
        self.assertEqual(
            [t.montant for t in ordonnes], [30.0, 45.0, 60.0]
        )

    def test_comparaison_devises_differentes_leve(self):
        with self.assertRaises(ValueError):
            Tarif(45, "EUR") < Tarif(45, "USD")


class TestAddition(unittest.TestCase):
    """Addition de deux Tarif de même devise."""

    def test_addition_meme_devise(self):
        somme = Tarif(45, "EUR") + Tarif(30, "EUR")
        self.assertEqual(somme, Tarif(75, "EUR"))

    def test_addition_produit_un_nouveau_tarif(self):
        a = Tarif(45, "EUR")
        somme = a + Tarif(30, "EUR")
        self.assertIsInstance(somme, Tarif)
        self.assertIsNot(somme, a)  # immutabilité : a n'est pas modifié
        self.assertEqual(a.montant, 45.0)

    def test_addition_devises_differentes_leve(self):
        with self.assertRaises(ValueError):
            Tarif(45, "EUR") + Tarif(30, "USD")

    def test_addition_avec_int_refusee(self):
        # __add__ renvoie NotImplemented -> Python lève TypeError.
        with self.assertRaises(TypeError):
            Tarif(45, "EUR") + 30


class TestRepresentation(unittest.TestCase):
    """Représentations lisible et non ambiguë."""

    def test_str(self):
        self.assertEqual(str(Tarif(45, "EUR")), "45.00 EUR")

    def test_str_deux_decimales(self):
        self.assertEqual(str(Tarif(45.5, "EUR")), "45.50 EUR")

    def test_repr_reconstructible(self):
        t = Tarif(45.0, "EUR")
        self.assertEqual(eval(repr(t)), t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
