import unittest
from count_keeper import CountKeeper
import os
class CountKeeperTest(unittest.TestCase):
    def test_add_cogs(self):
        keeper = CountKeeper()
        cogs = keeper.get_cogs(f'{os.getcwd()}/cogs_for_testing')
        cogs_names = [cog.__name__ for cog in cogs]
        # Here we are testing both that it gets all the cogs, and that it doesn't grab any noncogs
        compare_list = ["Cog1", "Cog2", "Cog3", "Cog4"]
        self.assertEqual(cogs_names, compare_list)
    def test_find_cogs(self):
        path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
        keeper = CountKeeper()
        cog = keeper.find_cog("Cog1", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is not None)
        
        cog = keeper.find_cog("Cog2", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is not None)
        
        cog = keeper.find_cog("Cog3", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is not None)
        
        cog = keeper.find_cog("Cog4", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is not None)
        
        
        cog = keeper.find_cog("nonsense", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is None)
    
    def test_load_and_unload(self):
        path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
        keeper = CountKeeper()
        cog1 = "Cog1"
        
        
        keeper.load(cog1, path_to_cogs=path_to_test_cogs)
        contains_after_adding: bool = False
        for cog in keeper.cogs:
            if cog == cog1:
                contains_after_adding = True
        self.assertTrue(contains_after_adding)
        
        
        keeper.unload(cog1)
        contains_after_removal: bool = False
        for cog in keeper.cogs:
            if cog == cog1:
                contains_after_removal = True
        self.assertFalse(contains_after_removal)
    
if __name__ == '__main__':
    unittest.main()