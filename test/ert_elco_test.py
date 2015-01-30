import unittest
import imp

class TestElcoDriver(unittest.TestCase):
    def setUp(self):
        self.module = imp.load_source("client" , "../ert-client")
        
    def test_create(self):
        with self.assertRaises(IOError):
            elco_input = self.module.ElcoInput("does-not-exist")
    
    def test_missing_required(self):
        with self.assertRaises(ValueError):
            def_input = self.module.ElcoInput("data/missing_required.einp")
            
    def test_default(self):
        def_input = self.module.ElcoInput("data/empty.einp")
        self.assertEqual( def_input.getErtSrcName() , "default")
        self.assertEqual( def_input.getErtTargetName() , "elcoDefault")
        self.assertEqual( def_input.getReportStep() , 1 )
        self.assertEqual( def_input.getHost() , "localhost" )


    def test_assign_default(self):
        def_input = self.module.ElcoInput("data/default_set.einp")
        self.assertEqual( def_input.getErtSrcName() , "ert_src")
        self.assertEqual( def_input.getErtTargetName() , "Target:with:colon")
        self.assertEqual( def_input.getHost() , "xxx.yyy")
        self.assertEqual( def_input.getReportStep() , 99 )


    def test_invalid(self):
        with self.assertRaises(ValueError):
            inp1 = self.module.ElcoInput("data/invalid_report.einp")

        with self.assertRaises(ValueError):
            inp1 = self.module.ElcoInput("data/invalid_colon.einp")

        with self.assertRaises(ValueError):
            inp1 = self.module.ElcoInput("data/invalid_control.einp")


    def test_controls(self):
        inp1 = self.module.ElcoInput("data/valid_controls.einp")
        self.assertTrue( inp1.hasControl("CONTROL1"))
        self.assertTrue( inp1.hasControl("CONTROL2"))
        self.assertFalse( inp1.hasControl("CONTROL3"))

        self.assertEqual( inp1.getControl("CONTROL1") , [1000 , 2000])
        self.assertEqual( inp1.getControl("CONTROL2") , [100 , 200])
        with self.assertRaises(KeyError):
            inp1.getControl("CONTROL3")

        
    def test_results(self):
        inp1 = self.module.ElcoInput("data/valid_results.einp")
        self.assertTrue( inp1.hasResult("RESULT1"))
        self.assertTrue( inp1.hasResult("Result2"))
        self.assertFalse( inp1.hasResult("NO"))

        with self.assertRaises(KeyError):
            inp1.setResult("RESULTX" , [0])

        with self.assertRaises(ValueError):
            inp1.setResult("RESULT1" , 10)

        inp1.setResult("RESULT1" , [10,20,30])
        

            


    def test_requests(self):
        inp1 = self.module.ElcoInput("data/valid_controls.einp")
        self.assertEqual( inp1.initSimulationRequest() , ["INIT_SIMULATION" , 88 , "default" , "Target"])
        self.assertEqual( inp1.addSimulationRequest() , ["ADD_SIMULATION" , 100 , 10 , 1 , [["CONTROL2" , 100, 200],["CONTROL1" , 1000 , 2000]]])
        
        inp1 = self.module.ElcoInput("data/valid_results.einp")
        request_list = inp1.getResultRequests()
        self.assertEqual( 2 , len(request_list))
        self.assertEqual( request_list[0], ["GET_RESULT" , 1 , 100 , "RESULT1"])
        self.assertEqual( request_list[1], ["GET_RESULT" , 1 , 100 , "Result2"])



if __name__ == "__main__":
    unittest.main()
