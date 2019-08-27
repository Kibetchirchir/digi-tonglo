import coverage

cov = coverage.Coverage()
cov.start()

# .. call your code ..

cov.stop()
cov.save()

cov.html_report()