import luigi
from luigi.mock import MockTarget
from bioluigi.tasks.non_atomic import NonAtomicTaskRunContext, non_atomic

class NonAtomicTask(luigi.Task):
    def run(self):
        with NonAtomicTaskRunContext(self):
            with self.output().open('w'):
                pass
            assert self.output().exists()
            raise RuntimeError('Dang! output is created, but task failed :(')
    def output(self):
        return MockTarget('some-non-atomic-output')

def test_non_atomic_run_context():
    task = NonAtomicTask()
    try:
        task.run()
    except Exception as e:
        assert str(e) == 'Dang! output is created, but task failed :('
    finally:
        assert not task.output().exists()

@non_atomic
class DecoratedNonAtomicTask(luigi.Task):
    def run(self):
        with self.output().open('w'):
            assert self.output().exists()
            raise RuntimeError('Dang! output is created, but task failed :(')

    def output(self):
        return MockTarget('some-non-atomic-output')

def test_non_atomic_decorator():
    task = DecoratedNonAtomicTask()
    try:
        task.run()
    except:
        pass
    finally:
        assert not task.output().exists()
