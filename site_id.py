import sys
exec(open("./shell_template.py").read())
app_name = sys.argv[1] + ".herokuapp.com"
if 0 == len(Site.objects.filter(domain=app_name)):
    Site.objects.create(domain=app_name)
print(Site.objects.filter(domain=app_name)[0].id)
