import apt
import sys

def remove_deb(package):
    #remove .deb packages
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[package]
    pkg.marked_delete
    resolver = apt.cache.ProblemResolver(cache)
    for pkg in cache.get_changes():
        if pkg.is_installed:
            resolver.remove(pkg)
        else:
            print (package + " not installed so not removed")
    try:
        cache.commit()
    except Exception as arg:
        print("Sorry, package removal failed [{err}]".format(err=str(arg)))


def install_deb(package):
    #install .deb packages
    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    pkg = cache[package]
    if pkg.is_installed:
        print("{package} already installed".format(package=package))
    else:
        pkg.mark_install()

        try:
            cache.commit()
        except Exception as arg:
            print("Sorry, package installation failed [{err}]".format(err=str(arg)))
