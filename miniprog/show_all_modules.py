import pkg_resources

modules = [(dist.project_name, dist.version) for dist in pkg_resources.working_set]
print(modules)

with open("modules.txt", "w") as file:
    for module in modules:
        file.write(module[0] + "==" + str(module[1]) + "\n")