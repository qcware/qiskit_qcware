from invoke import task, Collection


# pty=True added so that the tasks understand they're being run in a terminal
# and keep their pretty colored output
@task
def watch_for_mypy(c):
    c.run(
        "watchmedo shell-command --drop --command='mypy tests qiskit_qcware' --recursive tests qiskit_qcware",
        pty=True)


@task
def mypy(c):
    c.run('mypy tests qiskit_qcware', pty=True)


@task
def watch_for_tests(c, test_path="tests"):
    c.run(
        f"watchmedo shell-command --drop --command='pytest -n auto {test_path}' --recursive tests qiskit_qcware",
        pty=True)


@task
def test(c, test_path="tests"):
    c.run(f'pytest -n auto {test_path}',
          pty=True)


watches = Collection("watch")
watches.add_task(watch_for_mypy, "mypy")
watches.add_task(watch_for_tests, "tests")

ns = Collection()
ns.add_collection(watches, "watch")
ns.add_task(test, 'test')
ns.add_task(mypy, 'mypy')
