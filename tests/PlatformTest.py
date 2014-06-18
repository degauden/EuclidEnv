from Euclid.Platform import NativeMachine
from Euclid.Platform import isBinaryType
import unittest

class PlatformTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testFlavour(self):
        machine = NativeMachine()
        self.assertEqual(machine.OSFlavour(), "Fedora")
        print machine.OSVersion()
        print machine.CMTSystem()
        print machine.binaryOSFlavour()
        print machine.OSEquivalentFlavour()
        print machine.compatibleBinaryTag()
        print machine.compatibleBinaryTag(debug=True)
        print machine.supportedBinaryTag()
        print machine.supportedBinaryTag(debug=True)
        print machine.nativeCompilerVersion()
        print machine.nativeCompiler()
        print machine.nativeBinaryTag()
        print machine.nativeBinaryTag(debug=True)
        print "================================================================"
        self.assertEqual(machine.OSFlavour(teststring="Scientific Linux CERN SLC release 5.4 (Boron)"), "Scientific Linux")
        print machine.OSVersion()
        print machine.CMTSystem()
        print machine.binaryOSFlavour()
        print machine.OSEquivalentFlavour()
        print machine.compatibleBinaryTag()
        print machine.compatibleBinaryTag(debug=True)
        print machine.supportedBinaryTag()
        print machine.supportedBinaryTag(debug=True)
        print machine.nativeCompilerVersion()
        print machine.nativeCompiler()
        print machine.nativeBinaryTag()
        print machine.nativeBinaryTag(debug=True)
    def testBinaryType(self):
        self.assertTrue(isBinaryType("x86_64-fc20-gcc48-dbg", "Debug"))
        self.assertFalse(isBinaryType("x86_64-fc20-gcc48-opt", "Debug"))
        self.assertFalse(isBinaryType("x86_64-fc20-gcc48-dbg", "Release"))
        self.assertTrue(isBinaryType("x86_64-fc20-gcc48-opt", "Release"))

    def testVersion(self):
        pass

if __name__ == '__main__':
    unittest.main()