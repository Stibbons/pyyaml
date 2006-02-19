
import test_appliance

from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import *

class TestStructure(test_appliance.TestAppliance):

    def _testStructure(self, test_name, data_filename, structure_filename):
        node1 = None
        node2 = eval(file(structure_filename, 'rb').read())
        try:
            parser = Parser(Scanner(Reader(file(data_filename, 'rb'))))
            node1 = []
            while not parser.check(StreamEndEvent):
                node1.append(self._convert(parser))
            parser.get()
            if len(node1) == 1:
                node1 = node1[0]
            self.failUnlessEqual(node1, node2)
        except:
            print
            print "DATA:"
            print file(data_filename, 'rb').read()
            print "NODE1:", node1
            print "NODE2:", node2
            raise

    def _convert(self, parser):
        if parser.check(ScalarEvent):
            event = parser.get()
            if event.tag or event.anchor or event.value:
                return True
            else:
                return None
        elif parser.check(SequenceEvent):
            parser.get()
            sequence = []
            while not parser.check(CollectionEndEvent):
                sequence.append(self._convert(parser))
            parser.get()
            return sequence
        elif parser.check(MappingEvent):
            parser.get()
            mapping = []
            while not parser.check(CollectionEndEvent):
                key = self._convert(parser)
                value = self._convert(parser)
                mapping.append((key, value))
            parser.get()
            return mapping
        elif parser.check(AliasEvent):
            parser.get()
            return '*'
        else:
            parser.get()
            return '?'

TestStructure.add_tests('testStructure', '.data', '.structure')

class TestParser(test_appliance.TestAppliance):

    def _testParser(self, test_name, data_filename, canonical_filename):
        events1 = None
        events2 = None
        try:
            parser = Parser(Scanner(Reader(file(data_filename, 'rb'))))
            events1 = list(iter(parser))
            canonical = test_appliance.CanonicalParser(file(canonical_filename, 'rb').read())
            events2 = canonical.parse()
            self._compare(events1, events2)
        except:
            print
            print "DATA1:"
            print file(data_filename, 'rb').read()
            print "DATA2:"
            print file(canonical_filename, 'rb').read()
            print "EVENTS1:", events1
            print "EVENTS2:", events2
            raise

    def _compare(self, events1, events2):
        self.failUnlessEqual(len(events1), len(events2))
        for event1, event2 in zip(events1, events2):
            self.failUnlessEqual(event1.__class__, event2.__class__)
            if isinstance(event1, AliasEvent):
                #self.failUnlessEqual(event1.name, event2.name)
                pass
            elif isinstance(event1, ScalarEvent):
                #self.failUnlessEqual(event1.anchor, event2.anchor)
                #self.failUnlessEqual(event1.tag, event2.tag)
                self.failUnlessEqual(event1.value, event2.value)
            if isinstance(event1, CollectionEvent):
                #self.failUnlessEqual(event1.anchor, event2.anchor)
                #self.failUnlessEqual(event1.tag, event2.tag)
                pass


TestParser.add_tests('testParser', '.data', '.canonical')

class TestParserOnCanonical(test_appliance.TestAppliance):

    def _testParserOnCanonical(self, test_name, canonical_filename):
        events1 = None
        events2 = None
        try:
            parser = Parser(Scanner(Reader(file(canonical_filename, 'rb'))))
            events1 = list(iter(parser))
            canonical = test_appliance.CanonicalParser(file(canonical_filename, 'rb').read())
            events2 = canonical.parse()
            self._compare(events1, events2)
        except:
            print
            print "DATA:"
            print file(canonical_filename, 'rb').read()
            print "EVENTS1:", events1
            print "EVENTS2:", events2
            raise

    def _compare(self, events1, events2):
        self.failUnlessEqual(len(events1), len(events2))
        for event1, event2 in zip(events1, events2):
            self.failUnlessEqual(event1.__class__, event2.__class__)
            if isinstance(event1, AliasEvent):
                self.failUnlessEqual(event1.name, event2.name)
            elif isinstance(event1, ScalarEvent):
                self.failUnlessEqual(event1.anchor, event2.anchor)
                self.failUnlessEqual(event1.tag, event2.tag)
                self.failUnlessEqual(event1.value, event2.value)
            if isinstance(event1, CollectionEvent):
                self.failUnlessEqual(event1.anchor, event2.anchor)
                self.failUnlessEqual(event1.tag, event2.tag)

TestParserOnCanonical.add_tests('testParserOnCanonical', '.canonical')

