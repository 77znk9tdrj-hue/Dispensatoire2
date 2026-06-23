"""Tests de la persistance de la flotte (épreuve flotte).

Ces tests CONSTITUENT la spécification de la persistance :
sérialisation par to_dict (discriminateur + enrichissement), fabrique
de reconstruction pilotée par registre, et round-trip JSON qui
préserve le type exact ET la disponibilité.

Exécution : python -m unittest test_persistance -v
"""

import os
import tempfile
import unittest

from vehicule import Vehicule, VoitureElectrique, Camion
from persistance import (
    vehicule_depuis_dict,
    sauvegarder_flotte_json,
    charger_flotte_json,
)


CH1 = "VF1AAAAA11A111111"
CH2 = "5YJ3E1EA7KF000000"
CH3 = "YV2AAAAA11A222222"


def parc_exemple():
    """Construit un parc hétérogène de trois véhicules."""
    return [
        Vehicule("Renault", "Clio", CH1, 5, 2018),
        VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420),
        Camion("Volvo", "FH16", CH3, 2, 2020, 12.0),
    ]


class TestSerialisationDict(unittest.TestCase):
    """to_dict produit le bon discriminateur et les bons champs."""

    def test_type_vehicule_simple(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        d = v.to_dict()
        self.assertEqual(d["type"], "Vehicule")
        self.assertEqual(d["numero_chassis"], CH1)
        self.assertTrue(d["disponible"])

    def test_enrichissement_voiture(self):
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        d = ve.to_dict()
        self.assertEqual(d["type"], "VoitureElectrique")
        self.assertEqual(d["autonomie_km"], 420)
        # Les champs hérités sont présents (enrichissement, pas réécriture).
        self.assertEqual(d["marque"], "Tesla")

    def test_enrichissement_camion(self):
        c = Camion("Volvo", "FH16", CH3, 2, 2020, 12.0)
        d = c.to_dict()
        self.assertEqual(d["type"], "Camion")
        self.assertEqual(d["charge_utile_t"], 12.0)

    def test_etat_loue_serialise(self):
        v = Vehicule("Renault", "Clio", CH1, 5, 2018)
        v.louer()
        self.assertFalse(v.to_dict()["disponible"])


class TestFabrique(unittest.TestCase):
    """La fabrique restaure le type exact et rejette l'inconnu."""

    def test_reconstruit_voiture(self):
        ve = VoitureElectrique("Tesla", "Model 3", CH2, 5, 2022, 420)
        reconstruit = vehicule_depuis_dict(ve.to_dict())
        self.assertIs(type(reconstruit), VoitureElectrique)
        self.assertEqual(reconstruit.autonomie_km, 420)

    def test_reconstruit_camion(self):
        c = Camion("Volvo", "FH16", CH3, 2, 2020, 12.0)
        reconstruit = vehicule_depuis_dict(c.to_dict())
        self.assertIs(type(reconstruit), Camion)

    def test_type_inconnu_leve(self):
        with self.assertRaises(ValueError):
            vehicule_depuis_dict({"type": "Trottinette"})

    def test_type_absent_leve(self):
        with self.assertRaises(ValueError):
            vehicule_depuis_dict({"marque": "Renault"})


class TestRoundTripJson(unittest.TestCase):
    """Sauvegarder puis recharger en JSON redonne l'identique."""

    def setUp(self):
        self.dossier = tempfile.mkdtemp()
        self.chemin = os.path.join(self.dossier, "flotte.json")

    def test_types_exacts_preserves(self):
        sauvegarder_flotte_json(parc_exemple(), self.chemin)
        recharge = charger_flotte_json(self.chemin)
        types = [type(v) for v in recharge]
        self.assertEqual(types, [Vehicule, VoitureElectrique, Camion])

    def test_valeurs_preservees(self):
        sauvegarder_flotte_json(parc_exemple(), self.chemin)
        recharge = charger_flotte_json(self.chemin)
        self.assertEqual(recharge[1].autonomie_km, 420)
        self.assertEqual(recharge[2].charge_utile_t, 12.0)

    def test_disponibilite_preservee(self):
        parc = parc_exemple()
        parc[2].louer()  # le camion est loué
        sauvegarder_flotte_json(parc, self.chemin)
        recharge = charger_flotte_json(self.chemin)
        self.assertTrue(recharge[0].disponible)
        self.assertFalse(recharge[2].disponible)

    def test_identite_preservee(self):
        sauvegarder_flotte_json(parc_exemple(), self.chemin)
        recharge = charger_flotte_json(self.chemin)
        # __eq__ par châssis : les véhicules rechargés sont « les mêmes ».
        self.assertEqual(recharge, parc_exemple())


if __name__ == "__main__":
    unittest.main(verbosity=2)
