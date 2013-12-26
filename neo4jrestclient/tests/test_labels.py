# -*- coding: utf-8 -*-
from datetime import datetime
import unittest
import os

from neo4jrestclient import client
from neo4jrestclient.request import StatusException


NEO4J_URL = os.environ.get('NEO4J_URL', "http://localhost:7474/db/data/")
NEO4J_VERSION = os.environ.get('NEO4J_VERSION', None)


class GraphDatabaseTesCase(unittest.TestCase):

    def setUp(self):
        self.url = NEO4J_URL
        self.gdb = client.GraphDatabase(self.url)

    def tearDown(self):
        if self.gdb:
            self.gdb.flush()


@unittest.skipIf(NEO4J_VERSION in ["1.6.3", "1.7.2", "1.8.3", "1.9.5"],
                 "Not supported by Neo4j {}".format(NEO4J_VERSION))
class LabelsTestCase(GraphDatabaseTesCase):

    def test_label_append(self):
        n = self.gdb.nodes.create()
        label = "label"
        n.labels.add(label)
        self.assertIn(label, n.labels)

    def test_label_append_safe(self):
        n = self.gdb.nodes.create()
        label = u"label ñöś"
        n.labels.add(label)
        self.assertIn(label, n.labels)

    def test_labels_append(self):
        n = self.gdb.nodes.create()
        labels = ["label1", "label2"]
        n.labels.add(labels)
        for label in labels:
            self.assertIn(label, n.labels)

    def test_labels_append_safe(self):
        n = self.gdb.nodes.create()
        labels = [u"ñö", u"öś"]
        n.labels.add(labels)
        for label in labels:
            self.assertIn(label, n.labels)

    def test_label_append_invalud(self):
        n = self.gdb.nodes.create()
        label = ""
        self.assertRaises(StatusException, n.labels.add, label)

    def test_labels_replace(self):
        n = self.gdb.nodes.create()
        labels1 = ["label1", "label2"]
        n.labels.add(labels1)
        labels2 = ["bel1", "bel2"]
        n.labels = labels2
        labels = n.labels
        for label in labels1:
            self.assertNotIn(label, labels)
        for label in labels2:
            self.assertIn(label, labels)

    def test_labels_replace_safe(self):
        n = self.gdb.nodes.create()
        labels1 = [u"ñö", u"öś"]
        n.labels.add(labels1)
        labels2 = [u"ŕẅ", u"ó/~½ö"]
        n.labels = labels2
        labels = n.labels
        for label in labels1:
            self.assertNotIn(label, labels)
        for label in labels2:
            self.assertIn(label, labels)

    def test_labels_remove(self):
        n = self.gdb.nodes.create()
        labels = ["label1", "label2"]
        n.labels.add(labels)
        n.labels.remove("label1")
        self.assertIn("label2", n.labels)
        self.assertNotIn("label1", n.labels)

    def test_labels_remove_safe(self):
        n = self.gdb.nodes.create()
        labels = [u"ñö", u"öś"]
        n.labels.add(labels)
        n.labels.remove(u"ñö")
        self.assertIn(u"öś", n.labels)
        self.assertNotIn(u"ñö", n.labels)

    def test_labels_list(self):
        n = self.gdb.nodes.create()
        labels = ["label1", "label2"]
        n.labels.add(labels)
        self.assertEqual(labels, n.labels)

    def test_labels_list_safe(self):
        n = self.gdb.nodes.create()
        labels = [u"lâbel1", u"lâbel2"]
        n.labels.add(labels)
        self.assertEqual(labels, n.labels)

    def test_list_nodes_with_a_label(self):
        nodes = []
        label = u"lâbel_{}".format(datetime.now())
        for i in range(10):
            n = self.gdb.nodes.create()
            n.labels.add(label)
            nodes.append(n)
        labeled_nodes = self.gdb.labels[label]
        for node in nodes:
            self.assertIn(node, labeled_nodes)
        self.assertEqual(len(nodes), len(labeled_nodes))

    def test_get_nodes_with_a_label(self):
        nodes = []
        label = u"lâbel_{}".format(datetime.now())
        for i in range(10):
            n = self.gdb.nodes.create()
            n.labels.add(label)
            nodes.append(n)
        labeled_nodes = self.gdb.labels.get(label)
        for node in nodes:
            self.assertIn(node, labeled_nodes)
        self.assertEqual(len(nodes), len(labeled_nodes))

    def test_get_nodes_with_a_label_and_property(self):
        nodes = []
        label = u"lâbel_{}".format(datetime.now())
        value = u"propertÿ_{}".format(datetime.now())
        for i in range(10):
            if i % 2 == 0:
                n = self.gdb.nodes.create(property=value)
                n.labels.add(label)
                nodes.append(n)
            else:
                n = self.gdb.nodes.create()
        labeled_nodes = self.gdb.labels.get(label, property=value)
        for node in nodes:
            self.assertIn(node, labeled_nodes)
        self.assertEqual(len(nodes), len(labeled_nodes))

    def test_labels(self):
        n1 = self.gdb.nodes.create()
        n1.labels.add(["label1", "label2"])
        n2 = self.gdb.nodes.create()
        n2.labels.add("label3")
        for label in n1.labels + n2.labels:
            self.assertIn(label, self.gdb.labels)
        self.assertTrue(len(n1.labels) + len(n2.labels) <=
                        len(self.gdb.labels))