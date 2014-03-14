import unittest
from helpers import jobs


class TestJobs(unittest.TestCase):

    def setUp(self):
        # this can run
        self.a = jobs.Job("a", "ls")
        # this cannot run
        self.b = jobs.Job("b", "/bin/lils")
        # this will depend on the above
        self.c = jobs.Job("b", "/bin/time")

    def test_perror_no_error(self):
        self.assertEqual(self.a.perror(), (None, None))

    def test_perror_with_error(self):
        self.b.run()
        self.assertEqual(self.b.perror()[0], -1)

    def test_can_run_false1(self):
        self.c.add_dependency([self.a])
        self.assertFalse(self.c.can_run())

    def test_can_run_false2(self):
        self.c.add_dependency([self.a, self.b])
        self.a.run()
        self.assertFalse(self.c.can_run())

    def test_can_run_false3(self):
        self.c.add_dependency([self.a, self.b])
        self.a.run()
        self.b.run()
        self.assertFalse(self.c.can_run())

    def test_can_run_true1(self):
        self.c.add_dependency([self.a])
        self.a.run()
        self.assertTrue(self.c.can_run())


if __name__ == '__main__':
    unittest.main()
